import json
import fitz  # PyMuPDF
import zlib
import base64
from textwrap import wrap

# Parse nuclei JSON with multiple JSON objects per line
def parse_nuclei_json(json_file):
    data = []
    with open(json_file, 'r') as file:
        for line in file:
            data.append(json.loads(line.strip()))
    return data

# Add text with wrapping
def add_text(page, text, position, fontsize=12, fontname="helv", color=(0, 0, 0), wrap_width=90):
    wrapped_text = "\n".join(wrap(text, wrap_width))
    page.insert_text(position, wrapped_text, fontsize=fontsize, fontname=fontname, color=color)
    return wrapped_text.count('\n') + 1  # Return the number of lines for spacing

# Get severity color
def get_severity_color(severity):
    severity_colors = {
        "info": (0, 0, 1),          # Blue
        "low": (1, 1, 0),           # Yellow
        "medium": (1, 0.5, 0),      # Orange
        "high": (1, 0, 0),          # Red
        "critical": (0.5, 0, 0),    # Dark Red
        "unknown": (0.8, 0.8, 0.8)  # Light Grey
    }
    return severity_colors.get(severity.lower(), (0.8, 0.8, 0.8))

# Add header to each page
def add_header(doc, text):
    for page in doc:
        page.insert_text((72, 30), text, fontsize=12, fontname="helv", color=(0, 0, 0))

# Create summary page
def create_summary_page(doc, data):
    page = doc.new_page()
    summary_text = (
        "Summary\n"
        "The table below shows the numbers of issues identified in different categories. "
        "Issues are classified according to severity as High, Medium, Low, Information or False Positive. "
        "This reflects the likely impact of each issue for a typical organization. Issues are also classified according to confidence as Certain, Firm or Tentative. "
        "This reflects the inherent reliability of the technique that was used to identify the issue.\n"
    )
    add_text(page, summary_text, (72, 72), fontsize=12, fontname="helv", color=(0, 0, 0))
    
    severities = ["info", "low", "medium", "high", "critical", "unknown"]
    severity_counts = {severity: 0 for severity in severities}
    
    for item in data:
        severity = item['info'].get('severity', 'unknown').lower()
        severity_counts[severity] += 1
    
    table_text = "Severity Totals:\n\n" + "\n".join([f"{severity.capitalize()}: {count}" for severity, count in severity_counts.items()])
    add_text(page, table_text, (72, 200), fontsize=14, fontname="helv", color=(0, 0, 0))

# Create finding summary
def create_finding_summary(page, item, y_position):
    severity = item['info'].get('severity', 'unknown')
    severity_color = get_severity_color(severity)
    host = item.get('host', 'N/A')
    path = item.get('matched-at', 'N/A')

    page.draw_rect(fitz.Rect(120, y_position, 160, y_position + 12), color=severity_color, fill=severity_color)
    page.insert_text((72, y_position + 11), f"Severity: {severity}", fontsize=12, fontname="helv")
    y_position += 25
    
    page.insert_text((72, y_position), f"Host: {host}", fontsize=10, fontname="helv")
    y_position += 20
    
    page.insert_text((72, y_position), f"Path: {path}", fontsize=10, fontname="helv")
    y_position += 20

    matcher_name = item.get('matcher-name')
    if matcher_name:
        page.insert_text((72, y_position), f"Matcher Name: {matcher_name}", fontsize=12, fontname="helv")
        y_position += 20
    
    extractor_name = item.get('extractor-name')
    if extractor_name:
        page.insert_text((72, y_position), f"Extractor Name: {extractor_name}", fontsize=12, fontname="helv")
        y_position += 20
    
    extracted_results = item.get('extracted-results')
    if extracted_results:
        extracted_results_text = f"Extracted Results: {', '.join(extracted_results)}"
        lines = add_text(page, extracted_results_text, (72, y_position), fontsize=12, fontname="helv", color=(0, 0, 0))
        y_position += lines * 12
    
    return y_position

# to compress response text
def compress_and_encode(text):
    
    # Compress the text using Brotli
    compressed_data = zlib.compress(text[:2500].encode('utf-8'))
    # Encode the compressed data in base64
    encoded_data = base64.b64encode(compressed_data)
    return encoded_data.decode('utf-8')

# Create PDF report
def create_pdf_report(data, output_pdf):
    doc = fitz.open()
    create_summary_page(doc, data)
    y_position = 72
    page = doc.new_page()
    
    for item in data:
        if y_position > 680:
            page = doc.new_page()
            y_position = 72

        name = item['info'].get('name', 'N/A')
        
        page.insert_text((72, y_position), name, fontsize=16, fontname="helv", color=(0, 0.5, 0))
        y_position += 25
        
        y_position = create_finding_summary(page, item, y_position)
        
        description = item['info'].get('description')
        template = f"Template ID: {item.get('template-id', 'N/A')}\n"
        response = item.get('response', '')
        print(len(response))
        encoded_response = response if response else 'N/A'
        if len(response)>500:
            encoded_response = compress_and_encode(response) if response else 'N/A'
        
        responsetext = f"Response:\n{encoded_response}\n"
        if description:
            lines = add_text(page, f"Description: " + description, (72, y_position), fontsize=12, fontname="helv", color=(0, 0, 0))
            y_position += lines * 16  # Adjust y_position based on number of lines
        lines2 = add_text(page, template, (72, y_position), fontsize=12, fontname="helv", color=(0, 0, 0))
        y_position += lines2 * 16  # Adjust y_position based on number of lines
        lines3 = add_text(page, responsetext, (72, y_position), fontsize=10, fontname="helv", color=(0, 0, 0))
        y_position += lines3 * 16  # Adjust y_position based on number of lines

        remediation = item['info'].get('remediation')
        if remediation:
            lines = add_text(page, f"Remediation: {remediation}", (72, y_position), fontsize=12, fontname="helv", color=(0, 0, 0))
            y_position += lines * 14  # Adjust y_position based on number of lines
        
        page.draw_line((72, y_position), (500, y_position), color=(0, 0.5, 0))
        y_position += 20
        
    add_header(doc, "Scan Report")
    doc.save(output_pdf)

nuclei_json_file = "x.json"
output_pdf_file = "nuclei_report4.pdf"
nuclei_data = parse_nuclei_json(nuclei_json_file)
create_pdf_report(nuclei_data, output_pdf_file)
print(output_pdf_file)

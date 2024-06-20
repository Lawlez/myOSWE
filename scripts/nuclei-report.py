import json
import fitz  # PyMuPDF
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
        "info": (0, 0, 1),  # Blue
        "low": (1, 1, 0),  # Yellow
        "medium": (1, 0.5, 0),  # Orange
        "high": (1, 0, 0),  # Red
        "critical": (0.5, 0, 0),  # Dark Red
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
    
    table_text = "Severity Totals:\n" + "\n".join([f"{severity.capitalize()}: {count}" for severity, count in severity_counts.items()])
    add_text(page, table_text, (72, 200), fontsize=12, fontname="helv", color=(0, 0, 0))

# Create finding summary
def create_finding_summary(page, item, y_position):
    severity = item['info'].get('severity', 'unknown')
    severity_color = get_severity_color(severity)
    host = item.get('host', 'N/A')
    path = item.get('matched-at', 'N/A')

    page.draw_rect(fitz.Rect(72, y_position, 140, y_position + 20), color=severity_color, fill=severity_color)
    page.insert_text((150, y_position + 5), f"Severity: {severity}", fontsize=12, fontname="helv")
    y_position += 25
    
    page.insert_text((72, y_position), f"Host: {host}", fontsize=12, fontname="helv")
    y_position += 20
    
    page.insert_text((72, y_position), f"Path: {path}", fontsize=12, fontname="helv")
    y_position += 20
    
    return y_position

# Create PDF report
def create_pdf_report(data, output_pdf):
    doc = fitz.open()
    create_summary_page(doc, data)
    y_position = 72
    page = doc.new_page()
    
    for item in data:
        if y_position > 700:
            page = doc.new_page()
            y_position = 72

        name = item['info'].get('name', 'N/A')
        
        page.insert_text((72, y_position), name, fontsize=16, fontname="helv", color=(0, 0.5, 0))
        y_position += 25
        
        y_position = create_finding_summary(page, item, y_position)
        
        description = item['info'].get('description')
        if not description:
            description = f"Template ID: {item.get('template-id', 'N/A')}\n"
            response = item.get('response', '')
            encoded_response = base64.b64encode(response.encode()).decode() if response else 'N/A'
            description += f"Response (base64):\n{encoded_response}\n"
        
        lines = add_text(page, description, (72, y_position), fontsize=12, fontname="helv", color=(0, 0, 0))
        y_position += lines * 12  # Adjust y_position based on number of lines
        
        page.draw_line((72, y_position), (500, y_position), color=(0, 0.5, 0))
        y_position += 20
        
    add_header(doc, "Scan Report")
    doc.save(output_pdf)

nuclei_json_file = "x.json"
output_pdf_file = "nuclei_report2.pdf"
nuclei_data = parse_nuclei_json(nuclei_json_file)
create_pdf_report(nuclei_data, output_pdf_file)
print(output_pdf_file)

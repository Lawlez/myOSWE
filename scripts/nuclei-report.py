import json
import fitz  # PyMuPDF
import base64
#generate pdf report from nuclei json

def parse_nuclei_json(json_file):
    with open(json_file, 'r') as file:
        data = [json.loads(line) for line in file]
    return data

def add_text(page, text, position, fontsize=12, fontname="helv", color=(0, 0, 0), wrap_width=90):
    wrapped_text = ""
    lines = text.split("\n")
    for line in lines:
        while len(line) > wrap_width:
            split_index = line.rfind(" ", 0, wrap_width)
            if split_index == -1:
                split_index = wrap_width
            wrapped_text += line[:split_index] + "\n"
            line = line[split_index:]
        wrapped_text += line + "\n"
    page.insert_text(position, wrapped_text, fontsize=fontsize, fontname=fontname, color=color)

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

def add_header(doc, text):
    for page in doc:
        page.insert_text((72, 30), text, fontsize=12, fontname="helv", color=(0, 0, 0))

def create_summary_page(doc, data):
    page = doc.new_page()
    summary_text = "Summary\n"
    summary_text += "The table below shows the numbers of issues identified in different categories. "
    summary_text += "Issues are classified according to severity as High, Medium, Low, Information or False Positive. "
    summary_text += "This reflects the likely impact of each issue for a typical organization. Issues are also classified according to confidence as Certain, Firm or Tentative. "
    summary_text += "This reflects the inherent reliability of the technique that was used to identify the issue.\n"
    add_text(page, summary_text, (72, 72), fontsize=12, fontname="helv", color=(0, 0, 0))
    
    severities = ["info", "low", "medium", "high", "critical", "unknown"]
    severity_counts = {severity: 0 for severity in severities}
    
    for item in data:
        severity = item['info'].get('severity', 'unknown').lower()
        severity_counts[severity] += 1
    
    table_text = "Severity Totals:\n"
    for severity, count in severity_counts.items():
        table_text += f"{severity.capitalize()}: {count}\n"
    
    add_text(page, table_text, (72, 200), fontsize=12, fontname="helv", color=(0, 0, 0))

def create_finding_summary(page, item, y_position):
    severity = item['info'].get('severity', 'unknown')
    severity_color = get_severity_color(severity)
    host = item.get('host', 'N/A')
    path = item.get('matched-at', 'N/A')

    page.draw_rect(fitz.Rect(72, y_position, 140, y_position+20), color=severity_color, fill=severity_color)
    page.insert_text((150, y_position+5), f"Severity: {severity}", fontsize=12, fontname="helv")
    y_position += 25
    
    page.insert_text((72, y_position), f"Host: {host}", fontsize=12, fontname="helv")
    y_position += 20
    
    page.insert_text((72, y_position), f"Path: {path}", fontsize=12, fontname="helv")
    y_position += 20
    
    return y_position

def create_pdf_report(data, output_pdf):
    # Create a new PDF document
    doc = fitz.open()
    
    # Create summary page
    create_summary_page(doc, data)

    # Add findings
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
            description += f"Response (base64): {encoded_response}\n"
        
        add_text(page, description, (72, y_position), fontsize=12, fontname="helv", color=(0, 0, 0))
        y_position += 100
        
        # Add a page divider
        page.draw_line((72, y_position), (500, y_position), color=(0, 0.5, 0))
        y_position += 20
        
    # Add headers to each page
    add_header(doc, "TBK Scan Report from Cybertap")
    
    # Save the PDF
    doc.save(output_pdf)

nuclei_json_file = "tbk.json"
output_pdf_file = "nuclei_report.pdf"
nuclei_data = parse_nuclei_json(nuclei_json_file)
create_pdf_report(nuclei_data, output_pdf_file)
output_pdf_file

import json
import fitz  # PyMuPDF

#Generates simple PDF reports from nuclei json output.

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
        "critical": (0.5, 0, 0)  # Dark Red
    }
    return severity_colors.get(severity.lower(), (0, 0, 0))

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
    # Example of how to add a table would go here

def create_finding_summary(page, item, y_position):
    severity = item['info'].get('severity', 'N/A')
    severity_color = get_severity_color(severity)
    host = item.get('host', 'N/A')
    path = item.get('matched-at', 'N/A')

    page.draw_rect(fitz.Rect(72, y_position, 150, y_position+20), color=severity_color, fill=severity_color)
    add_text(page, "Severity: " + severity, (152, y_position), fontsize=12, fontname="helv")
    y_position += 20
    
    add_text(page, "Confidence: Certain", (72, y_position), fontsize=12, fontname="helv")
    y_position += 20
    
    add_text(page, "Host: " + host, (72, y_position), fontsize=12, fontname="helv")
    y_position += 20
    
    add_text(page, "Path: " + path, (72, y_position), fontsize=12, fontname="helv")
    y_position += 40
    
    return y_position

def create_pdf_report(data, output_pdf):
    # Create a new PDF document
    doc = fitz.open()
    
    # Create summary page
    create_summary_page(doc, data)

    # Add findings
    for item in data:
        page = doc.new_page()
        name = item['info'].get('name', 'N/A')
        
        add_text(page, name, (72, 72), fontsize=16, fontname="helv", color=(0, 0.5, 0))
        y_position = create_finding_summary(page, item, 100)
        
        info = f"Template ID: {item.get('template-id', 'N/A')}\n"
        info += f"Description: {item['info'].get('description', 'N/A')}\n"
        
        add_text(page, info, (72, y_position), fontsize=12, fontname="helv", color=(0, 0, 0))
        y_position += 100

        # Add a page divider
        page.draw_line((72, y_position), (500, y_position), color=(0, 0.5, 0))
        
    # Add headers to each page
    add_header(doc, "TBK Scan Report from Cybertap")
    
    # Save the PDF
    doc.save(output_pdf)

nuclei_json_file = "./tbk.json"
output_pdf_file = "./nuclei_report.pdf"
nuclei_data = parse_nuclei_json(nuclei_json_file)
create_pdf_report(nuclei_data, output_pdf_file)
output_pdf_file

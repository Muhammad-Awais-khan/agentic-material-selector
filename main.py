from orchestrator import MaterialSelectorOrchestrator
from dotenv import load_dotenv
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os
import subprocess
import platform

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main entry point for the Agentic Material Selector
    Coordinates multiple AI agents to evaluate construction materials
    """

    # Get user input for location
    city = input("Enter City: ")
    country = input("Enter Country: ")

    # Initialize the orchestrator
    orchestrator = MaterialSelectorOrchestrator()
    
    # Evaluate materials for a specific location
    print("=" * 80)
    print("AGENTIC MATERIAL SELECTOR")
    print("=" * 80)
    print("Generating comprehensive evaluation report...")
    print()
    
    # Run comprehensive material evaluation
    result = orchestrator.evaluate_materials(
        city=city,
        country=country,
    )
    
    # Create reports folder on C drive
    reports_folder = "C:\\MaterialReports"
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
        print(f"Created reports folder: {reports_folder}")
    
    # Generate PDF report in the reports folder
    pdf_filename = os.path.join(reports_folder, f"material_evaluation_{city.lower()}_{country.lower()}.pdf")
    generate_pdf(result, pdf_filename)
    
    # Automatically open the PDF
    open_pdf(pdf_filename)



def format_results(result):
    """
    Format the evaluation results in a human-readable plain text format
    """
    output = []
    
    # Location info
    location = result['location']
    output.append(f"LOCATION: {location['city']}, {location['country']}")
    output.append("")
    
    # Availability
    output.append("MATERIAL AVAILABILITY")
    output.append("-" * 30)
    availability = result['availability']
    
    if availability.get('easy_to_get'):
        output.append("EASY TO SOURCE LOCALLY:")
        for material in availability['easy_to_get']:
            output.append(f"   • {material}")
        output.append("")
    
    if availability.get('limited'):
        output.append("LIMITED AVAILABILITY:")
        for material in availability['limited']:
            output.append(f"   • {material}")
        output.append("")
    
    if availability.get('import_only'):
        output.append("IMPORT ONLY:")
        for material in availability['import_only']:
            output.append(f"   • {material}")
        output.append("")
    
    # Carbon Impact
    output.append("CARBON FOOTPRINT ANALYSIS")
    output.append("-" * 30)
    carbon = result['carbon_impact']
    for material, data in carbon.items():
        rating = data['rating']
        sustainability = "*" * rating  # Use asterisks instead of star emojis
        output.append(f"• {material}")
        output.append(f"   Footprint: {data['carbon_footprint']}")
        output.append(f"   Rating: {rating}/10 {sustainability}")
        output.append(f"   Notes: {data['notes']}")
        output.append("")
    
    # Cost Analysis
    output.append("COST ANALYSIS")
    output.append("-" * 30)
    cost = result['cost_analysis']
    for material, data in cost.items():
        output.append(f"• {material}")
        output.append(f"   Relative Cost: {data['relative_cost'].upper()}")
        if 'estimated_price_per_unit' in data:
            output.append(f"   Est. Price/Unit: ${data['estimated_price_per_unit']}")
        output.append(f"   Notes: {data['notes']}")
        output.append("")
    
    # Durability
    output.append("DURABILITY ANALYSIS")
    output.append("-" * 30)
    durability = result['durability']
    for material, data in durability.items():
        output.append(f"• {material}")
        output.append(f"   Lifespan: {data['lifespan_years']} years")
        output.append(f"   Maintenance: {data['maintenance'].upper()}")
        output.append(f"   Notes: {data['notes']}")
        output.append("")
    
    return "\n".join(output)

def generate_pdf(result, filename="material_evaluation_report.pdf"):
    """
    Generate a PDF report from the evaluation results
    """
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=HexColor('#2E86AB')
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=15,
        textColor=HexColor('#A23B72')
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.spaceAfter = 8
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=normal_style,
        leftIndent=20,
        bulletIndent=10
    )
    
    recommendation_style = ParagraphStyle(
        'Recommendation',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        textColor=HexColor('#F18F01'),
        alignment=1
    )
    
    story = []
    
    # Title
    story.append(Paragraph("AGENTIC MATERIAL SELECTOR", title_style))
    story.append(Paragraph("Comprehensive Evaluation Report", styles['Heading3']))
    story.append(Spacer(1, 0.25*inch))
    
    # Location
    location = result['location']
    story.append(Paragraph(f"LOCATION: {location['city']}, {location['country']}", styles['Heading4']))
    story.append(Spacer(1, 0.15*inch))
    
    # Availability Section
    story.append(Paragraph("MATERIAL AVAILABILITY", section_style))
    availability = result['availability']
    
    if availability.get('easy_to_get'):
        story.append(Paragraph("EASY TO SOURCE LOCALLY:", normal_style))
        for material in availability['easy_to_get']:
            story.append(Paragraph(f"• {material}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
    
    if availability.get('limited'):
        story.append(Paragraph("LIMITED AVAILABILITY:", normal_style))
        for material in availability['limited']:
            story.append(Paragraph(f"• {material}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
    
    if availability.get('import_only'):
        story.append(Paragraph("IMPORT ONLY:", normal_style))
        for material in availability['import_only']:
            story.append(Paragraph(f"• {material}", bullet_style))
    story.append(PageBreak())
    
    # Carbon Impact Section
    story.append(Paragraph("CARBON FOOTPRINT ANALYSIS", section_style))
    carbon = result['carbon_impact']
    for material, data in carbon.items():
        rating = data['rating']
        stars = "*" * rating  # Use asterisks instead of star emojis
        story.append(Paragraph(f"<b>{material}</b>", normal_style))
        story.append(Paragraph(f"Footprint: {data['carbon_footprint']}", bullet_style))
        story.append(Paragraph(f"Rating: {rating}/10 {stars}", bullet_style))
        story.append(Paragraph(f"Notes: {data['notes']}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
    story.append(PageBreak())
    
    # Cost Analysis Section
    story.append(Paragraph("COST ANALYSIS", section_style))
    cost = result['cost_analysis']
    for material, data in cost.items():
        story.append(Paragraph(f"<b>{material}</b>", normal_style))
        story.append(Paragraph(f"Relative Cost: {data['relative_cost'].upper()}", bullet_style))
        if 'estimated_price_per_unit' in data:
            story.append(Paragraph(f"Est. Price/Unit: ${data['estimated_price_per_unit']}", bullet_style))
        story.append(Paragraph(f"Notes: {data['notes']}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
    story.append(PageBreak())
    
    # Durability Section
    story.append(Paragraph("DURABILITY ANALYSIS", section_style))
    durability = result['durability']
    for material, data in durability.items():
        story.append(Paragraph(f"<b>{material}</b>", normal_style))
        story.append(Paragraph(f"Lifespan: {data['lifespan_years']} years", bullet_style))
        story.append(Paragraph(f"Maintenance: {data['maintenance'].upper()}", bullet_style))
        story.append(Paragraph(f"Notes: {data['notes']}", bullet_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Recommendation
    story.append(PageBreak())
    story.append(Paragraph("RECOMMENDATION", recommendation_style))
    story.append(Paragraph(result['recommendation'], normal_style))
    
    # Build PDF
    doc.build(story)
    return filename

def open_pdf(filename):
    """
    Automatically open the PDF file
    """
    try:
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filename])
        else:  # Linux
            subprocess.run(["xdg-open", filename])
        print(f"PDF report generated and opened: {filename}")
    except Exception as e:
        print(f"PDF generated successfully: {filename}")
        print(f"Could not auto-open PDF: {e}")


if __name__ == "__main__":
    main()
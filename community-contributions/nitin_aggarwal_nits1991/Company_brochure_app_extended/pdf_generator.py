"""
PDF Generator Module
====================

Generate PDF documents from markdown content.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
import markdown
from bs4 import BeautifulSoup


def markdown_to_pdf_content(md_text: str) -> list:
    """
    Convert markdown text to reportlab flowables.

    Args:
        md_text: Markdown formatted text

    Returns:
        List of reportlab flowables
    """
    # Convert markdown to HTML
    html = markdown.markdown(md_text, extensions=['extra', 'nl2br'])

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Setup styles
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1f77b4',
        spaceAfter=12,
        alignment=TA_CENTER
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#2ca02c',
        spaceAfter=10,
        spaceBefore=10
    ))

    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    ))

    # Build flowables
    flowables = []

    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol']):
        if element.name == 'h1':
            flowables.append(
                Paragraph(element.get_text(), styles['CustomTitle']))
            flowables.append(Spacer(1, 0.2*inch))
        elif element.name in ['h2', 'h3']:
            flowables.append(
                Paragraph(element.get_text(), styles['CustomHeading']))
            flowables.append(Spacer(1, 0.1*inch))
        elif element.name == 'p':
            flowables.append(
                Paragraph(element.get_text(), styles['CustomBody']))
        elif element.name in ['ul', 'ol']:
            for li in element.find_all('li'):
                flowables.append(
                    Paragraph(f"• {li.get_text()}", styles['CustomBody']))

    return flowables


def generate_pdf(content: str, title: str = "Document", company_name: str = "") -> bytes:
    """
    Generate PDF from markdown content.

    Args:
        content: Markdown formatted content
        title: Document title
        company_name: Company name for header

    Returns:
        PDF file as bytes
    """
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Container for flowables
    story = []

    # Styles
    styles = getSampleStyleSheet()

    # Add header
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=20,
        textColor='#1f77b4',
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    story.append(Paragraph(title, header_style))
    story.append(Spacer(1, 0.2*inch))

    # Add date
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor='#666666',
        alignment=TA_CENTER
    )

    story.append(
        Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", date_style))
    story.append(Spacer(1, 0.3*inch))

    # Add content
    try:
        content_flowables = markdown_to_pdf_content(content)
        story.extend(content_flowables)
    except Exception as e:
        # Fallback to plain text if markdown conversion fails
        body_style = styles['BodyText']
        for line in content.split('\n'):
            if line.strip():
                story.append(Paragraph(line, body_style))
                story.append(Spacer(1, 0.1*inch))

    # Build PDF
    doc.build(story)

    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def generate_simple_pdf(content: str, title: str = "Document") -> bytes:
    """
    Generate a simple PDF without markdown processing.

    Args:
        content: Plain text content
        title: Document title

    Returns:
        PDF file as bytes
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add title
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 0.3*inch))

    # Add content
    for line in content.split('\n'):
        if line.strip():
            story.append(Paragraph(line, styles['BodyText']))
            story.append(Spacer(1, 0.1*inch))

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes

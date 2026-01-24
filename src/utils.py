import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import os
from datetime import datetime

def export_chat_to_pdf(chat_messages, filename="neurovault_chat_export.pdf"):
    """Export chat conversation to PDF"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
    except ImportError:
        return "Please install reportlab: pip install reportlab", False
    
    try:
        # Create Downloads folder path
        downloads_path = Path.home() / "Downloads"
        downloads_path.mkdir(exist_ok=True)
        
        pdf_path = downloads_path / filename
        
        # Create PDF
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#5b8def',
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        timestamp_style = ParagraphStyle(
            'Timestamp',
            parent=styles['Normal'],
            fontSize=10,
            textColor='#6e7175',
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        user_style = ParagraphStyle(
            'User',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10,
            backColor='#e0e7ff'
        )
        
        ai_style = ParagraphStyle(
            'AI',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=15
        )
        
        # Title
        story.append(Paragraph("NeuroVault Chat Export", title_style))
        story.append(Paragraph(
            f"Exported on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
            timestamp_style
        ))
        story.append(Spacer(1, 0.3*inch))
        
        # Messages
        for msg_type, content in chat_messages:
            # Clean content
            clean_content = content.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
            
            if msg_type == 'user':
                story.append(Paragraph(f"<b>You:</b><br/>{clean_content}", user_style))
            else:
                story.append(Paragraph(f"<b>NeuroVault:</b><br/>{clean_content}", ai_style))
            story.append(Spacer(1, 0.15*inch))
        
        # Build PDF
        doc.build(story)
        return str(pdf_path), True
        
    except Exception as e:
        return f"Error: {str(e)}", False

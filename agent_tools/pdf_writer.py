"""
Academic Professional PDF Writer Tool

This module provides tools for generating professional academic PDF reports
with customizable templates and layouts.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, darkblue, darkgray
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import re


class AcademicPDFWriter:
    """
    Professional academic PDF report generator with multiple template options
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for academic reports with improved readability"""
        
        # Title style - More prominent and readable
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            spaceAfter=40,
            spaceBefore=20,
            alignment=TA_CENTER,
            textColor=HexColor('#1a365d'),
            fontName='Helvetica-Bold',
            leading=32
        ))
        
        # Subtitle style - Better hierarchy
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=25,
            spaceBefore=30,
            alignment=TA_LEFT,
            textColor=HexColor('#2d3748'),
            fontName='Helvetica-Bold',
            leading=22
        ))
        
        # Section header style - More readable
        self.styles.add(ParagraphStyle(
            name='CustomSectionHeader',
            parent=self.styles['Heading3'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=20,
            alignment=TA_LEFT,
            textColor=HexColor('#2d3748'),
            fontName='Helvetica-Bold',
            leading=20,
            borderWidth=0,
            borderColor=HexColor('#e2e8f0'),
            borderPadding=8
        ))
        
        # Subsection header style - New for better hierarchy
        self.styles.add(ParagraphStyle(
            name='CustomSubsectionHeader',
            parent=self.styles['Heading4'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=15,
            alignment=TA_LEFT,
            textColor=HexColor('#4a5568'),
            fontName='Helvetica-Bold',
            leading=18
        ))
        
        # Body text style - Improved readability
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=18,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Executive summary style - More prominent
        self.styles.add(ParagraphStyle(
            name='CustomExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=13,
            spaceAfter=10,
            spaceBefore=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=20,
            leftIndent=25,
            rightIndent=25,
            backColor=HexColor('#f7fafc'),
            borderColor=HexColor('#cbd5e0'),
            borderWidth=2,
            borderPadding=15
        ))
        
        # Key findings style - Highlighted
        self.styles.add(ParagraphStyle(
            name='CustomKeyFindings',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=18,
            leftIndent=15,
            rightIndent=15,
            backColor=HexColor('#edf2f7'),
            borderColor=HexColor('#e2e8f0'),
            borderWidth=1,
            borderPadding=10
        ))
        
        # Citation style - Better formatting
        self.styles.add(ParagraphStyle(
            name='CustomCitation',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            spaceBefore=5,
            alignment=TA_LEFT,
            fontName='Helvetica-Oblique',
            textColor=HexColor('#718096'),
            leftIndent=25,
            leading=14
        ))
        
        # Bullet point style - Improved spacing
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=18,
            leftIndent=25
        ))
        
        # Recommendation style - Highlighted
        self.styles.add(ParagraphStyle(
            name='CustomRecommendation',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leading=18,
            leftIndent=20,
            textColor=HexColor('#2d3748')
        ))
        
        # Table header style
        self.styles.add(ParagraphStyle(
            name='CustomTableHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=5,
            spaceBefore=5,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            textColor=HexColor('#ffffff'),
            leading=14
        ))
        
        # Table cell style
        self.styles.add(ParagraphStyle(
            name='CustomTableCell',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            spaceBefore=3,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=14
        ))
    
    def create_header_footer(self, canvas, doc):
        """Create professional header and footer with improved design"""
        canvas.saveState()
        
        # Header background
        canvas.setFillColor(HexColor('#f7fafc'))
        canvas.rect(0, 780, 612, 40, fill=1, stroke=0)
        
        # Header text
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(HexColor('#1a365d'))
        canvas.drawString(50, 795, "Strategic Intelligence Report")
        
        # Header line
        canvas.setStrokeColor(HexColor('#cbd5e0'))
        canvas.setLineWidth(1)
        canvas.line(50, 785, 562, 785)
        
        # Footer background
        canvas.setFillColor(HexColor('#f7fafc'))
        canvas.rect(0, 0, 612, 40, fill=1, stroke=0)
        
        # Footer content
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(HexColor('#4a5568'))
        canvas.drawString(50, 15, f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        canvas.drawRightString(562, 15, f"Page {doc.page}")
        
        # Footer line
        canvas.setStrokeColor(HexColor('#cbd5e0'))
        canvas.setLineWidth(1)
        canvas.line(50, 35, 562, 35)
        
        canvas.restoreState()
    
    def parse_content_sections(self, content: str) -> Dict[str, str]:
        """Parse content into structured sections"""
        sections = {
            'title': '',
            'executive_summary': '',
            'introduction': '',
            'key_findings': '',
            'analysis': '',
            'recommendations': '',
            'implementation': '',
            'conclusion': '',
            'references': ''
        }
        
        # Extract title (first line or after #)
        lines = content.split('\n')
        if lines:
            first_line = lines[0].strip()
            if first_line.startswith('#'):
                sections['title'] = first_line.replace('#', '').strip()
            else:
                sections['title'] = first_line
        
        # Extract sections based on headers
        current_section = 'introduction'
        current_content = []
        
        for line in lines[1:]:
            line = line.strip()
            
            if line.startswith('##'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                header = line.replace('##', '').strip().lower()
                if 'executive' in header or 'summary' in header:
                    current_section = 'executive_summary'
                elif 'introduction' in header or 'overview' in header:
                    current_section = 'introduction'
                elif 'finding' in header or 'insight' in header:
                    current_section = 'key_findings'
                elif 'analysis' in header or 'strategic' in header:
                    current_section = 'analysis'
                elif 'recommendation' in header or 'action' in header:
                    current_section = 'recommendations'
                elif 'implementation' in header or 'roadmap' in header:
                    current_section = 'implementation'
                elif 'conclusion' in header or 'summary' in header:
                    current_section = 'conclusion'
                elif 'reference' in header or 'citation' in header:
                    current_section = 'references'
                else:
                    current_section = 'analysis'
                
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def clean_html_content(self, content: str) -> str:
        """Clean HTML content for PDF generation"""
        # Replace HTML line breaks with newlines
        content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
        
        # Replace HTML bold tags
        content = re.sub(r'<b>(.*?)</b>', r'<b>\1</b>', content)
        content = re.sub(r'<strong>(.*?)</strong>', r'<b>\1</b>', content)
        
        # Replace HTML italic tags
        content = re.sub(r'<i>(.*?)</i>', r'<i>\1</i>', content)
        content = re.sub(r'<em>(.*?)</em>', r'<i>\1</i>', content)
        
        # Remove any remaining HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        return content
    
    def create_table_from_markdown(self, content: str) -> Table:
        """Convert markdown table to ReportLab Table"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not lines:
            return Spacer(1, 20)
        
        # Check if this looks like a table
        table_lines = []
        in_table = False
        
        for line in lines:
            if '|' in line and not line.startswith('---'):
                in_table = True
                table_lines.append(line)
            elif in_table and '|' not in line:
                break
        
        if not table_lines:
            # Not a table, return as regular content
            return None
        
        # Parse table
        table_data = []
        for line in table_lines:
            if line.startswith('|') and line.endswith('|'):
                # Remove leading and trailing pipes
                cells = [cell.strip() for cell in line[1:-1].split('|')]
                table_data.append(cells)
        
        if not table_data:
            return Spacer(1, 20)
        
        # Convert to ReportLab Table
        # Clean up cell content
        cleaned_data = []
        for row in table_data:
            cleaned_row = []
            for cell in row:
                # Clean HTML and markdown
                cell = self.clean_html_content(cell)
                cell = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', cell)
                cell = re.sub(r'\*(.*?)\*', r'<i>\1</i>', cell)
                cleaned_row.append(Paragraph(cell, self.styles['CustomBody']))
            cleaned_data.append(cleaned_row)
        
        # Create table with improved styling
        table = Table(cleaned_data)
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d3748')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
            ('TEXTCOLOR', (0, 1), (-1, -1), HexColor('#2d3748')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            
            # Alternating row colors (only apply if rows exist)
            # ('BACKGROUND', (0, 2), (-1, 2), HexColor('#f7fafc')),
            # ('BACKGROUND', (0, 4), (-1, 4), HexColor('#f7fafc')),
            # ('BACKGROUND', (0, 6), (-1, 6), HexColor('#f7fafc')),
            
            # Grid and borders
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, HexColor('#2d3748')),
            
            # Alignment and padding
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        return table
    
    def create_executive_summary_box(self, content: str) -> Table:
        """Create a highlighted executive summary box"""
        if not content:
            return Spacer(1, 20)
        
        # Clean up content
        content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
        content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)
        
        summary_para = Paragraph(content, self.styles['CustomExecutiveSummary'])
        
        # Create table with border
        data = [[summary_para]]
        table = Table(data, colWidths=[7*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#f8f9fa')),
            ('BORDER', (0, 0), (-1, -1), 1, HexColor('#dee2e6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 15),
        ]))
        
        return table
    
    def create_key_findings_table(self, content: str) -> Table:
        """Create a highlighted table for key findings"""
        if not content:
            return Spacer(1, 20)
        
        # Parse bullet points or numbered items
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        findings = []
        
        for i, line in enumerate(lines):
            # Remove markdown formatting
            line = re.sub(r'^\d+\.\s*', '', line)  # Remove numbers
            line = re.sub(r'^[-*]\s*', '', line)   # Remove bullets
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Bold
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)      # Italic
            
            if line:
                # Add numbering and highlight
                numbered_line = f"<b>{i+1}.</b> {line}"
                findings.append([Paragraph(numbered_line, self.styles['CustomKeyFindings'])])
        
        if not findings:
            return Spacer(1, 20)
        
        # Create table with better styling
        table = Table(findings, colWidths=[7*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#edf2f7')),
            ('BORDER', (0, 0), (-1, -1), 1, HexColor('#e2e8f0')),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, HexColor('#cbd5e0')),
        ]))
        
        return table
    
    def create_recommendations_section(self, content: str) -> List:
        """Create formatted recommendations section with improved styling"""
        if not content:
            return [Spacer(1, 20)]
        
        elements = []
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for i, line in enumerate(lines, 1):
            # Clean up formatting
            line = re.sub(r'^\d+\.\s*', '', line)
            line = re.sub(r'^[-*]\s*', '', line)
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
            
            if line:
                # Create recommendation with enhanced styling
                rec_text = f"<b>{i}.</b> {line}"
                para = Paragraph(rec_text, self.styles['CustomRecommendation'])
                elements.append(para)
                elements.append(Spacer(1, 12))
        
        return elements
    
    def create_references_section(self, content: str) -> List:
        """Create formatted references section"""
        if not content:
            return [Spacer(1, 20)]
        
        elements = []
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for line in lines:
            if line and not line.startswith('#'):
                # Clean up reference formatting
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
                
                para = Paragraph(line, self.styles['CustomCitation'])
                elements.append(para)
                elements.append(Spacer(1, 4))
        
        return elements
    
    def generate_pdf(self, content: str, filename: str = None, template: str = "academic") -> str:
        """
        Generate a professional PDF report
        
        Args:
            content: The report content (markdown format)
            filename: Output filename (optional)
            template: Template type ("academic", "executive", "research")
            
        Returns:
            Path to generated PDF file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"strategic_report_{timestamp}.pdf"
        
        # Ensure filename has .pdf extension
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Parse content into sections
        sections = self.parse_content_sections(content)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Title page
        if sections['title']:
            title_para = Paragraph(sections['title'], self.styles['CustomTitle'])
            story.append(title_para)
            story.append(Spacer(1, 30))
            
            # Add generation timestamp
            timestamp_para = Paragraph(
                f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                self.styles['CustomCitation']
            )
            story.append(timestamp_para)
            story.append(PageBreak())
        
        # Executive Summary (highlighted box)
        if sections['executive_summary']:
            story.append(Paragraph("Executive Summary", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            story.append(self.create_executive_summary_box(sections['executive_summary']))
            story.append(Spacer(1, 25))
        
        # Introduction
        if sections['introduction']:
            story.append(Paragraph("Introduction", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            
            # Clean HTML content
            clean_content = self.clean_html_content(sections['introduction'])
            clean_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_content)
            clean_content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_content)
            intro_para = Paragraph(clean_content, self.styles['CustomBody'])
            story.append(intro_para)
            story.append(Spacer(1, 25))
        
        # Key Findings
        if sections['key_findings']:
            story.append(Paragraph("Key Findings", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            story.append(self.create_key_findings_table(sections['key_findings']))
            story.append(Spacer(1, 25))
        
        # Analysis
        if sections['analysis']:
            story.append(Paragraph("Strategic Analysis", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            
            # Clean HTML content
            clean_content = self.clean_html_content(sections['analysis'])
            clean_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_content)
            clean_content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_content)
            analysis_para = Paragraph(clean_content, self.styles['CustomBody'])
            story.append(analysis_para)
            story.append(Spacer(1, 25))
        
        # Recommendations
        if sections['recommendations']:
            story.append(Paragraph("Recommendations", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            
            rec_elements = self.create_recommendations_section(sections['recommendations'])
            story.extend(rec_elements)
            story.append(Spacer(1, 25))
        
        # Implementation
        if sections['implementation']:
            story.append(Paragraph("Implementation Roadmap", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            
            # Check if this section contains a table
            table = self.create_table_from_markdown(sections['implementation'])
            if table:
                story.append(table)
                story.append(Spacer(1, 25))
            else:
                # Clean HTML content and create paragraph
                clean_content = self.clean_html_content(sections['implementation'])
                clean_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_content)
                clean_content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_content)
                impl_para = Paragraph(clean_content, self.styles['CustomBody'])
                story.append(impl_para)
                story.append(Spacer(1, 25))
        
        # Conclusion
        if sections['conclusion']:
            story.append(Paragraph("Conclusion", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            
            # Clean HTML content
            clean_content = self.clean_html_content(sections['conclusion'])
            clean_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_content)
            clean_content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_content)
            conclusion_para = Paragraph(clean_content, self.styles['CustomBody'])
            story.append(conclusion_para)
            story.append(Spacer(1, 25))
        
        # References
        if sections['references']:
            story.append(PageBreak())  # Start references on new page
            story.append(Paragraph("References", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 15))
            
            ref_elements = self.create_references_section(sections['references'])
            story.extend(ref_elements)
        
        # Build PDF with header/footer
        doc.build(story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return filename


def create_pdf_report(content: str, filename: str = None, template: str = "xhtml2pdf") -> str:
    """
    Create a professional PDF report from content using xhtml2pdf template
    
    Args:
        content: Report content in markdown format
        filename: Output filename (optional)
        template: Template type ("xhtml2pdf", "mockup", "professional", "academic", "executive", "research")
        
    Returns:
        Path to generated PDF file
    """
    if template == "xhtml2pdf":
        try:
            # Use the xhtml2pdf template system (best for exact mockup replication)
            from .xhtml2pdf_template import create_xhtml2pdf_report
            if filename is None:
                filename = f"xhtml2pdf_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return create_xhtml2pdf_report(content, filename)
        except ImportError:
            # Fallback to mockup template
            from .mockup_pdf_template import create_mockup_pdf_report
            if filename is None:
                filename = f"mockup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return create_mockup_pdf_report(content, filename)
    elif template == "mockup":
        try:
            # Use the exact mockup template system
            from .mockup_pdf_template import create_mockup_pdf_report
            if filename is None:
                filename = f"mockup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return create_mockup_pdf_report(content, filename)
        except ImportError:
            # Fallback to professional template
            from .pdf_templates import create_professional_pdf_report
            if filename is None:
                filename = f"professional_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return create_professional_pdf_report(content, filename)
    elif template == "professional":
        try:
            # Use the professional template system
            from .pdf_templates import create_professional_pdf_report
            if filename is None:
                filename = f"professional_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return create_professional_pdf_report(content, filename)
        except ImportError:
            # Fallback to original system if template import fails
            writer = AcademicPDFWriter()
            return writer.generate_pdf(content, filename, template)
    else:
        # Use original system for other templates
        writer = AcademicPDFWriter()
        return writer.generate_pdf(content, filename, template)


# Example usage and testing
if __name__ == "__main__":
    # Test content
    test_content = """
# Strategic Analysis: Digital Transformation in Higher Education

## Executive Summary

This comprehensive analysis examines the strategic implementation of digital transformation initiatives in higher education institutions. Our research reveals that institutions adopting comprehensive digital strategies achieve 23% higher student satisfaction rates and 18% operational cost reductions within 24 months.

## Key Findings

1. **Technology Integration**: 78% of surveyed institutions report improved operational efficiency through digital twin implementation
2. **Student Experience**: Digital platforms increase student engagement by 34% on average
3. **Cost Optimization**: Automated systems reduce administrative costs by 22%
4. **Competitive Advantage**: Early adopters gain 15% market share advantage

## Strategic Analysis

The digital transformation landscape in higher education presents both significant opportunities and challenges. Institutions must balance innovation with operational stability while ensuring faculty and student adoption.

## Recommendations

1. **Establish Digital Governance Framework** - Create cross-functional steering committee
2. **Pilot High-Impact Initiatives** - Start with student-facing services
3. **Invest in Change Management** - Comprehensive training and communication
4. **Measure and Iterate** - Implement KPI dashboards for continuous improvement

## Implementation Roadmap

- **Phase 1 (Months 1-3)**: Governance setup and pilot selection
- **Phase 2 (Months 4-9)**: Pilot implementation and testing
- **Phase 3 (Months 10-18)**: Full-scale rollout and optimization

## References

1. Smith, J. (2024). Digital Transformation in Higher Education. *Journal of Educational Technology*.
2. Johnson, M. (2024). Strategic Implementation of Digital Twins. *Academic Leadership Review*.
    """
    
    # Generate test PDF
    pdf_path = create_pdf_report(test_content, "test_report.pdf")
    print(f"PDF generated: {pdf_path}")

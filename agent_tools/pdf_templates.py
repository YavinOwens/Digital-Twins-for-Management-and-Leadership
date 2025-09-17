"""
Professional PDF Templates based on industry brochure design
Creates standardized, visually appealing PDF layouts
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from typing import List, Dict, Any, Optional
import re
import os

class ProfessionalPDFTemplate:
    """Professional PDF template system based on industry brochure design"""
    
    def __init__(self, filename="professional_report.pdf", page_size=A4):
        self.filename = filename
        self.page_size = page_size
        self.doc = SimpleDocTemplate(
            filename, 
            pagesize=page_size,
            rightMargin=0.75*inch, 
            leftMargin=0.75*inch,
            topMargin=1*inch, 
            bottomMargin=1*inch
        )
        self.styles = getSampleStyleSheet()
        self.setup_professional_styles()
        self.story = []
    
    def setup_professional_styles(self):
        """Setup professional styles based on brochure design"""
        
        # Brand Colors (from mockup)
        self.brand_red = HexColor('#DC2626')  # Primary red
        self.brand_dark_red = HexColor('#991B1B')  # Darker red
        self.brand_black = HexColor('#1F2937')  # Dark gray/black
        self.brand_light_gray = HexColor('#F9FAFB')  # Light background
        self.brand_medium_gray = HexColor('#6B7280')  # Medium gray
        self.brand_white = HexColor('#FFFFFF')
        
        # Cover Page Title
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            parent=self.styles['Heading1'],
            fontSize=36,
            spaceAfter=20,
            spaceBefore=0,
            alignment=TA_CENTER,
            textColor=self.brand_white,
            fontName='Helvetica-Bold',
            leading=42
        ))
        
        # Cover Subtitle
        self.styles.add(ParagraphStyle(
            name='CoverSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=30,
            spaceBefore=10,
            alignment=TA_CENTER,
            textColor=self.brand_white,
            fontName='Helvetica',
            leading=24
        ))
        
        # Section Headers (Red background)
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            spaceBefore=30,
            alignment=TA_LEFT,
            textColor=self.brand_white,
            fontName='Helvetica-Bold',
            leading=28,
            backColor=self.brand_red,
            borderPadding=15,
            leftIndent=20
        ))
        
        # Subsection Headers
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            spaceBefore=25,
            alignment=TA_LEFT,
            textColor=self.brand_red,
            fontName='Helvetica-Bold',
            leading=22
        ))
        
        # Body Text
        self.styles.add(ParagraphStyle(
            name='ProfessionalBodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=16,
            textColor=self.brand_black
        ))
        
        # Highlighted Text (for key points)
        self.styles.add(ParagraphStyle(
            name='HighlightText',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=6,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leading=18,
            textColor=self.brand_red,
            leftIndent=20
        ))
        
        # Quote/Testimonial Style
        self.styles.add(ParagraphStyle(
            name='QuoteText',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=15,
            spaceBefore=15,
            alignment=TA_LEFT,
            fontName='Helvetica-Oblique',
            leading=18,
            textColor=self.brand_black,
            leftIndent=30,
            rightIndent=30,
            backColor=self.brand_light_gray,
            borderColor=self.brand_red,
            borderWidth=1,
            borderPadding=15
        ))
        
        # Table Header
        self.styles.add(ParagraphStyle(
            name='TableHeader',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=5,
            spaceBefore=5,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            textColor=self.brand_white,
            leading=14
        ))
        
        # Table Cell
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=3,
            spaceBefore=3,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=14,
            textColor=self.brand_black
        ))
        
        # List Item
        self.styles.add(ParagraphStyle(
            name='ListItem',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            spaceBefore=6,
            alignment=TA_LEFT,
            fontName='Helvetica',
            leading=16,
            textColor=self.brand_black,
            leftIndent=25
        ))
        
        # Statistics/Number Style
        self.styles.add(ParagraphStyle(
            name='StatNumber',
            parent=self.styles['Normal'],
            fontSize=28,
            spaceAfter=5,
            spaceBefore=5,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            textColor=self.brand_red,
            leading=32
        ))
        
        # Stat Label
        self.styles.add(ParagraphStyle(
            name='StatLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            spaceBefore=5,
            alignment=TA_CENTER,
            fontName='Helvetica',
            textColor=self.brand_medium_gray,
            leading=12
        ))
    
    def create_cover_page(self, title: str, subtitle: str = "", company: str = "Strategic Intelligence Report") -> List:
        """Create professional cover page with red background"""
        elements = []
        
        # Red background section
        elements.append(Spacer(1, 2*inch))
        
        # Main title
        title_para = Paragraph(title, self.styles['CoverTitle'])
        elements.append(title_para)
        
        # Subtitle
        if subtitle:
            subtitle_para = Paragraph(subtitle, self.styles['CoverSubtitle'])
            elements.append(subtitle_para)
        
        # Company/Report type
        company_para = Paragraph(company, self.styles['CoverSubtitle'])
        elements.append(company_para)
        
        elements.append(Spacer(1, 2*inch))
        
        # Generation date
        date_para = Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y')}", 
            self.styles['CoverSubtitle']
        )
        elements.append(date_para)
        
        elements.append(PageBreak())
        return elements
    
    def create_table_of_contents(self, sections: List[str]) -> List:
        """Create professional table of contents"""
        elements = []
        
        # TOC Header
        toc_header = Paragraph("Table of Contents", self.styles['SectionHeader'])
        elements.append(toc_header)
        elements.append(Spacer(1, 20))
        
        # TOC Items
        toc_data = [['Section', 'Page']]
        for i, section in enumerate(sections, 1):
            toc_data.append([f"{i}. {section}", str(i + 2)])  # +2 for cover and TOC pages
        
        toc_table = Table(toc_data, colWidths=[5*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.brand_red),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.brand_white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.brand_white),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.brand_black),
            ('GRID', (0, 0), (-1, -1), 1, self.brand_light_gray),
        ]))
        
        elements.append(toc_table)
        elements.append(PageBreak())
        return elements
    
    def create_section_header(self, title: str) -> List:
        """Create red section header"""
        elements = []
        header_para = Paragraph(title, self.styles['SectionHeader'])
        elements.append(header_para)
        return elements
    
    def create_key_findings_section(self, findings: List[str]) -> List:
        """Create key findings with red bullet points"""
        elements = []
        
        # Section header
        elements.extend(self.create_section_header("Key Findings"))
        elements.append(Spacer(1, 15))
        
        # Findings list
        for i, finding in enumerate(findings, 1):
            # Clean finding text
            clean_finding = self.clean_html_content(finding)
            clean_finding = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_finding)
            clean_finding = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_finding)
            
            finding_text = f"<b>{i}.</b> {clean_finding}"
            finding_para = Paragraph(finding_text, self.styles['HighlightText'])
            elements.append(finding_para)
            elements.append(Spacer(1, 8))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def create_analysis_section(self, content: str) -> List:
        """Create strategic analysis section"""
        elements = []
        
        # Section header
        elements.extend(self.create_section_header("Strategic Analysis"))
        elements.append(Spacer(1, 15))
        
        # Clean and format content
        clean_content = self.clean_html_content(content)
        clean_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_content)
        clean_content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_content)
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in clean_content.split('\n\n') if p.strip()]
        
        for para_text in paragraphs:
            if para_text.startswith('**') and para_text.endswith('**'):
                # This is a subsection header
                header_text = para_text.replace('**', '').strip()
                header_para = Paragraph(header_text, self.styles['SubsectionHeader'])
                elements.append(header_para)
            else:
                # Regular paragraph
                para = Paragraph(para_text, self.styles['ProfessionalBodyText'])
                elements.append(para)
                elements.append(Spacer(1, 8))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def create_recommendations_section(self, recommendations: List[str]) -> List:
        """Create recommendations with numbered list"""
        elements = []
        
        # Section header
        elements.extend(self.create_section_header("Recommendations"))
        elements.append(Spacer(1, 15))
        
        # Recommendations list
        for i, rec in enumerate(recommendations, 1):
            # Clean recommendation text
            clean_rec = self.clean_html_content(rec)
            clean_rec = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_rec)
            clean_rec = re.sub(r'\*(.*?)\*', r'<i>\1</i>', clean_rec)
            
            rec_text = f"<b>{i}.</b> {clean_rec}"
            rec_para = Paragraph(rec_text, self.styles['ListItem'])
            elements.append(rec_para)
            elements.append(Spacer(1, 10))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def create_implementation_roadmap(self, roadmap_data: List[Dict]) -> List:
        """Create implementation roadmap table"""
        elements = []
        
        # Section header
        elements.extend(self.create_section_header("Implementation Roadmap"))
        elements.append(Spacer(1, 15))
        
        # Create table data
        table_data = [['Phase', 'Timeline', 'Key Milestones', 'Success Metrics']]
        
        for phase in roadmap_data:
            table_data.append([
                phase.get('phase', ''),
                phase.get('timeline', ''),
                phase.get('milestones', ''),
                phase.get('metrics', '')
            ])
        
        # Create table
        roadmap_table = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 2.8*inch, 2.8*inch])
        roadmap_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), self.brand_red),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.brand_white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, 0), 8),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), self.brand_white),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.brand_black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('PADDING', (0, 1), (-1, -1), 6),
            
            # Grid and borders
            ('GRID', (0, 0), (-1, -1), 1, self.brand_light_gray),
            ('LINEBELOW', (0, 0), (-1, 0), 2, self.brand_red),
        ]))
        
        elements.append(roadmap_table)
        elements.append(Spacer(1, 20))
        return elements
    
    def create_statistics_section(self, stats: List[Dict]) -> List:
        """Create statistics section with highlighted numbers"""
        elements = []
        
        # Section header
        elements.extend(self.create_section_header("Key Statistics"))
        elements.append(Spacer(1, 20))
        
        # Create statistics grid
        if len(stats) >= 4:
            # 2x2 grid
            stats_data = []
            for i in range(0, len(stats), 2):
                row = []
                for j in range(2):
                    if i + j < len(stats):
                        stat = stats[i + j]
                        stat_text = f"<para align='center'><font name='Helvetica-Bold' size='24' color='{self.brand_red.hexval()}'>{stat.get('value', '')}</font><br/><font name='Helvetica' size='10' color='{self.brand_medium_gray.hexval()}'>{stat.get('label', '')}</font></para>"
                        row.append(stat_text)
                    else:
                        row.append("")
                stats_data.append(row)
            
            stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
            stats_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 20),
                ('BACKGROUND', (0, 0), (-1, -1), self.brand_light_gray),
            ]))
            
            elements.append(stats_table)
        else:
            # Single column
            for stat in stats:
                stat_para = Paragraph(
                    f"<para align='center'><font name='Helvetica-Bold' size='28' color='{self.brand_red.hexval()}'>{stat.get('value', '')}</font><br/><font name='Helvetica' size='12' color='{self.brand_black.hexval()}'>{stat.get('label', '')}</font></para>",
                    self.styles['ProfessionalBodyText']
                )
                elements.append(stat_para)
                elements.append(Spacer(1, 15))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def create_references_section(self, references: List[str]) -> List:
        """Create references section"""
        elements = []
        
        # Section header
        elements.extend(self.create_section_header("References"))
        elements.append(Spacer(1, 15))
        
        # References list
        for i, ref in enumerate(references, 1):
            ref_text = f"{i}. {ref}"
            ref_para = Paragraph(ref_text, self.styles['ProfessionalBodyText'])
            elements.append(ref_para)
            elements.append(Spacer(1, 6))
        
        elements.append(Spacer(1, 20))
        return elements
    
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
    
    def create_header_footer(self, canvas, doc):
        """Create professional header and footer"""
        canvas.saveState()
        
        # Header
        canvas.setFillColor(self.brand_red)
        canvas.rect(0, doc.height + doc.topMargin - 30, doc.width + doc.leftMargin + doc.rightMargin, 30, fill=1, stroke=0)
        
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(self.brand_white)
        canvas.drawString(doc.leftMargin, doc.height + doc.topMargin - 20, "Strategic Intelligence Report")
        
        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(self.brand_medium_gray)
        canvas.drawString(doc.leftMargin, 30, f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        canvas.drawRightString(doc.width + doc.leftMargin, 30, f"Page {doc.page}")
        
        canvas.restoreState()
    
    def generate_professional_pdf(self, content_data: Dict[str, Any]) -> str:
        """Generate professional PDF using template system"""
        
        # Start building content
        self.story = []
        
        # Cover page
        title = content_data.get('title', 'Strategic Analysis Report')
        subtitle = content_data.get('subtitle', 'Comprehensive Intelligence Report')
        self.story.extend(self.create_cover_page(title, subtitle))
        
        # Table of contents
        sections = [
            "Executive Summary",
            "Key Findings", 
            "Strategic Analysis",
            "Recommendations",
            "Implementation Roadmap",
            "Key Statistics",
            "References"
        ]
        self.story.extend(self.create_table_of_contents(sections))
        
        # Executive Summary
        if content_data.get('executive_summary'):
            self.story.extend(self.create_section_header("Executive Summary"))
            self.story.append(Spacer(1, 15))
            
            clean_summary = self.clean_html_content(content_data['executive_summary'])
            summary_para = Paragraph(clean_summary, self.styles['ProfessionalBodyText'])
            self.story.append(summary_para)
            self.story.append(Spacer(1, 20))
        
        # Key Findings
        if content_data.get('key_findings'):
            findings = content_data['key_findings']
            if isinstance(findings, str):
                findings = [f.strip() for f in findings.split('\n') if f.strip()]
            self.story.extend(self.create_key_findings_section(findings))
        
        # Strategic Analysis
        if content_data.get('analysis'):
            self.story.extend(self.create_analysis_section(content_data['analysis']))
        
        # Recommendations
        if content_data.get('recommendations'):
            recommendations = content_data['recommendations']
            if isinstance(recommendations, str):
                recommendations = [r.strip() for r in recommendations.split('\n') if r.strip()]
            self.story.extend(self.create_recommendations_section(recommendations))
        
        # Implementation Roadmap
        if content_data.get('implementation'):
            # Parse implementation data into roadmap format
            roadmap_data = self.parse_roadmap_data(content_data['implementation'])
            self.story.extend(self.create_implementation_roadmap(roadmap_data))
        
        # Key Statistics
        if content_data.get('statistics'):
            self.story.extend(self.create_statistics_section(content_data['statistics']))
        
        # References
        if content_data.get('references'):
            references = content_data['references']
            if isinstance(references, str):
                references = [r.strip() for r in references.split('\n') if r.strip()]
            self.story.extend(self.create_references_section(references))
        
        # Build PDF
        self.doc.build(self.story, onFirstPage=self.create_header_footer, onLaterPages=self.create_header_footer)
        
        return self.filename
    
    def parse_roadmap_data(self, implementation_text: str) -> List[Dict]:
        """Parse implementation text into roadmap data structure"""
        roadmap_data = []
        
        # Look for table-like structure
        lines = [line.strip() for line in implementation_text.split('\n') if line.strip()]
        
        # Find table rows (containing |)
        table_rows = []
        for line in lines:
            if '|' in line and not line.startswith('---'):
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if len(cells) >= 4:  # Phase, Timeline, Milestones, Metrics
                    table_rows.append(cells)
        
        # Convert to roadmap data
        for row in table_rows[1:]:  # Skip header
            roadmap_data.append({
                'phase': row[0] if len(row) > 0 else '',
                'timeline': row[1] if len(row) > 1 else '',
                'milestones': row[2] if len(row) > 2 else '',
                'metrics': row[3] if len(row) > 3 else ''
            })
        
        return roadmap_data

def create_professional_pdf_report(content: str, filename: str = "professional_report.pdf") -> str:
    """Create professional PDF report using template system"""
    
    # Parse content into structured data
    content_data = parse_content_to_data_structure(content)
    
    # Create PDF using template
    template = ProfessionalPDFTemplate(filename)
    return template.generate_professional_pdf(content_data)

def parse_content_to_data_structure(content: str) -> Dict[str, Any]:
    """Parse markdown content into structured data for templates"""
    
    sections = {
        'title': '',
        'subtitle': '',
        'executive_summary': '',
        'key_findings': [],
        'analysis': '',
        'recommendations': [],
        'implementation': '',
        'statistics': [],
        'references': []
    }
    
    # Extract title
    lines = content.split('\n')
    if lines and lines[0].startswith('#'):
        sections['title'] = lines[0].replace('#', '').strip()
    
    # Parse sections
    current_section = None
    current_content = []
    
    for line in lines[1:]:
        line = line.strip()
        
        if line.startswith('##'):
            # Save previous section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Start new section
            header = line.replace('##', '').strip().lower()
            if 'executive' in header or 'summary' in header:
                current_section = 'executive_summary'
            elif 'finding' in header or 'insight' in header:
                current_section = 'key_findings'
            elif 'analysis' in header or 'strategic' in header:
                current_section = 'analysis'
            elif 'recommendation' in header or 'action' in header:
                current_section = 'recommendations'
            elif 'implementation' in header or 'roadmap' in header:
                current_section = 'implementation'
            elif 'reference' in header or 'citation' in header:
                current_section = 'references'
            else:
                current_section = 'analysis'
            
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    # Convert string sections to lists where needed
    if isinstance(sections['key_findings'], str):
        sections['key_findings'] = [f.strip() for f in sections['key_findings'].split('\n') if f.strip()]
    
    if isinstance(sections['recommendations'], str):
        sections['recommendations'] = [r.strip() for r in sections['recommendations'].split('\n') if r.strip()]
    
    if isinstance(sections['references'], str):
        sections['references'] = [ref.strip() for ref in sections['references'].split('\n') if ref.strip()]
    
    return sections

if __name__ == "__main__":
    # Test the template system
    test_content = """
# Strategic Analysis: Digital Transformation in Healthcare

## Executive Summary
This comprehensive analysis examines the strategic implementation of digital transformation initiatives in healthcare institutions, revealing significant opportunities for operational efficiency and patient care improvement.

## Key Findings
1. **Technology Integration**: 78% of surveyed institutions report improved operational efficiency
2. **Patient Experience**: Digital platforms increase patient engagement by 34%
3. **Cost Optimization**: Automated systems reduce administrative costs by 22%
4. **Competitive Advantage**: Early adopters gain 15% market share advantage

## Strategic Analysis
The digital transformation landscape presents both significant opportunities and challenges. Institutions must balance innovation with operational stability.

## Recommendations
1. **Establish Digital Governance Framework** - Create cross-functional steering committee
2. **Pilot High-Impact Initiatives** - Start with patient-facing services
3. **Invest in Change Management** - Comprehensive training and communication
4. **Measure and Iterate** - Implement KPI dashboards for continuous improvement

## Implementation Roadmap

| Phase | Timeline | Key Milestones | Success Metrics |
|-------|----------|----------------|-----------------|
| Phase 1 | Month 1-3 | Form Steering Committee | Governance charter |
| Phase 2 | Month 4-6 | Inventory systems | Data architecture |

## References
1. Smith, J. (2024). Digital Transformation in Healthcare.
2. Johnson, M. (2024). Strategic Implementation of Digital Twins.
"""
    
    pdf_path = create_professional_pdf_report(test_content, "test_professional_report.pdf")
    print(f"Professional PDF generated: {pdf_path}")

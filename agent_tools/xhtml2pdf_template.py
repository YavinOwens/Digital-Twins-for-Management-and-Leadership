"""
xhtml2pdf-based PDF Template for Exact Mockup Replication
Uses HTML/CSS for precise control over layout and styling
"""

from xhtml2pdf import pisa
from io import BytesIO
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

class XHTML2PDFTemplate:
    """xhtml2pdf-based template for exact mockup replication"""
    
    def __init__(self):
        self.brand_red = "#DC2626"
        self.brand_light_blue = "#8B9DC3"
        self.brand_black = "#1F2937"
        self.brand_white = "#FFFFFF"
        self.brand_light_gray = "#F8F9FA"
        self.brand_dark_gray = "#6B7280"
    
    def create_css_styles(self) -> str:
        """Create CSS styles matching professional report standards"""
        return f"""
        <style>
        @page {{
            size: A4;
            margin: 0.5in;
        }}
        
        body {{
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.0;
            color: {self.brand_black};
            margin: 0;
            padding: 0;
        }}
        
        .cover-page {{
            page-break-after: always;
            background-color: {self.brand_red};
            min-height: 100vh;
            padding: 2in;
            position: relative;
        }}
        
        .cover-title {{
            font-family: Arial, sans-serif;
            font-size: 24pt;
            font-weight: bold;
            color: {self.brand_white};
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .cover-subtitle {{
            font-family: Arial, sans-serif;
            font-size: 14pt;
            color: {self.brand_white};
            margin-bottom: 40px;
            opacity: 0.9;
        }}
        
        .cover-tagline {{
            background-color: {self.brand_red};
            color: {self.brand_white};
            padding: 15px 25px;
            font-family: Arial, sans-serif;
            font-size: 12pt;
            font-weight: bold;
            text-align: center;
            border: 2px solid {self.brand_white};
            margin-top: 2in;
            display: inline-block;
        }}
        
        .geometric-shape {{
            display: none;
        }}
        
        .toc-page {{
            page-break-after: always;
        }}
        
        .toc-header {{
            background-color: {self.brand_red};
            color: {self.brand_white};
            padding: 15px;
            font-family: Arial, sans-serif;
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 30px;
        }}
        
        .toc-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            border: 2px solid {self.brand_red};
        }}
        
        .toc-table th {{
            background-color: {self.brand_red};
            color: {self.brand_white};
            padding: 10px;
            text-align: left;
            font-family: Arial, sans-serif;
            font-size: 11pt;
            font-weight: bold;
            border: 1px solid {self.brand_white};
        }}
        
        .toc-table td {{
            padding: 8px 10px;
            border: 1px solid {self.brand_black};
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            background-color: {self.brand_white};
        }}
        
        .toc-table td:last-child {{
            text-align: right;
        }}
        
        .section-header {{
            background-color: {self.brand_red};
            color: {self.brand_white};
            padding: 12px 15px;
            font-family: Arial, sans-serif;
            font-size: 14pt;
            font-weight: bold;
            margin: 25px 0 15px 0;
        }}
        
        .subsection-header {{
            color: {self.brand_red};
            font-family: Arial, sans-serif;
            font-size: 12pt;
            font-weight: bold;
            margin: 20px 0 10px 0;
        }}
        
        .body-text {{
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.0;
            text-align: justify;
            margin-bottom: 15px;
        }}
        
        .key-findings {{
            color: {self.brand_red};
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            font-weight: bold;
            line-height: 1.0;
            margin: 8px 0;
            padding-left: 20px;
        }}
        
        .recommendations {{
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.0;
            margin: 8px 0;
            padding-left: 20px;
        }}
        
        .roadmap-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-family: 'Times New Roman', serif;
            border: 2px solid {self.brand_red};
        }}
        
        .roadmap-table th {{
            background-color: {self.brand_red};
            color: {self.brand_white};
            padding: 8px;
            text-align: center;
            font-family: Arial, sans-serif;
            font-size: 11pt;
            font-weight: bold;
            border: 1px solid {self.brand_white};
        }}
        
        .roadmap-table td {{
            padding: 6px 8px;
            border: 1px solid {self.brand_black};
            font-size: 10pt;
            vertical-align: top;
            background-color: {self.brand_white};
        }}
        
        .references {{
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.0;
            margin: 8px 0;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        .highlight-box {{
            background-color: {self.brand_light_gray};
            border-left: 4px solid {self.brand_red};
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
        }}
        
        .quote {{
            font-style: italic;
            margin: 15px 0;
            padding: 10px 20px;
            border-left: 3px solid {self.brand_red};
            background-color: {self.brand_light_gray};
        }}
        </style>
        """
    
    def create_cover_page(self, title: str, subtitle: str = "", tagline: str = "Precision. Performance. Progress.") -> str:
        """Create cover page HTML"""
        return f"""
        <div class="cover-page">
            <div class="geometric-shape triangle-red"></div>
            <div class="geometric-shape triangle-blue"></div>
            
            <h1 class="cover-title">{title}</h1>
            {f'<p class="cover-subtitle">{subtitle}</p>' if subtitle else ''}
            
            <div class="cover-tagline">{tagline}</div>
        </div>
        """
    
    def create_table_of_contents(self, sections: List[str]) -> str:
        """Create table of contents HTML"""
        toc_rows = ""
        for i, section in enumerate(sections, 1):
            toc_rows += f"""
            <tr>
                <td>{i}. {section}</td>
                <td>{i + 2}</td>
            </tr>
            """
        
        return f"""
        <div class="toc-page">
            <div class="toc-header">Table of Contents</div>
            <table class="toc-table">
                <thead>
                    <tr>
                        <th>Section</th>
                        <th>Page</th>
                    </tr>
                </thead>
                <tbody>
                    {toc_rows}
                </tbody>
            </table>
        </div>
        """
    
    def create_section_header(self, title: str) -> str:
        """Create section header HTML"""
        return f'<div class="section-header">{title}</div>'
    
    def create_key_findings(self, findings: List[str]) -> str:
        """Create key findings HTML"""
        findings_html = ""
        valid_findings = []
        
        # Filter out table headers and malformed entries
        for finding in findings:
            clean_finding = finding.strip()
            # Skip table headers and separators
            if (clean_finding.startswith('|') or 
                clean_finding.startswith('---') or 
                '|' in clean_finding and '---' in clean_finding or
                clean_finding.startswith('1.1#') or
                clean_finding.startswith('2.1---')):
                continue
            # Skip entries that look like table formatting
            if len(clean_finding) < 10 and ('|' in clean_finding or '-' in clean_finding):
                continue
            valid_findings.append(clean_finding)
        
        for i, finding in enumerate(valid_findings, 1):
            clean_finding = self.clean_html_content(finding)
            findings_html += f'<div class="key-findings"><strong>{i}.</strong> {clean_finding}</div>'
        
        return f"""
        {self.create_section_header("Key Findings")}
        {findings_html}
        """
    
    def create_analysis_section(self, content: str) -> str:
        """Create strategic analysis section HTML"""
        clean_content = self.clean_html_content(content)
        
        # Split into paragraphs and process
        paragraphs = [p.strip() for p in clean_content.split('\n\n') if p.strip()]
        content_html = ""
        
        for para in paragraphs:
            if para.startswith('**') and para.endswith('**'):
                # Subsection header
                header_text = para.replace('**', '').strip()
                content_html += f'<div class="subsection-header">{header_text}</div>'
            else:
                # Regular paragraph
                content_html += f'<div class="body-text">{para}</div>'
        
        return f"""
        {self.create_section_header("Strategic Analysis")}
        {content_html}
        """
    
    def create_recommendations(self, recommendations: List[str]) -> str:
        """Create recommendations HTML"""
        recs_html = ""
        for i, rec in enumerate(recommendations, 1):
            clean_rec = self.clean_html_content(rec)
            recs_html += f'<div class="recommendations"><strong>{i}.</strong> {clean_rec}</div>'
        
        return f"""
        {self.create_section_header("Recommendations")}
        {recs_html}
        """
    
    def create_implementation_roadmap(self, roadmap_data: List[Dict]) -> str:
        """Create implementation roadmap HTML"""
        table_rows = ""
        for phase in roadmap_data:
            table_rows += f"""
            <tr>
                <td>{phase.get('phase', '')}</td>
                <td>{phase.get('timeline', '')}</td>
                <td>{phase.get('milestones', '')}</td>
                <td>{phase.get('metrics', '')}</td>
            </tr>
            """
        
        return f"""
        {self.create_section_header("Implementation Roadmap")}
        <table class="roadmap-table">
            <thead>
                <tr>
                    <th>Phase</th>
                    <th>Timeline</th>
                    <th>Key Milestones</th>
                    <th>Success Metrics</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """
    
    def create_references(self, references: List[str]) -> str:
        """Create references HTML"""
        refs_html = ""
        for i, ref in enumerate(references, 1):
            refs_html += f'<div class="references">{i}. {ref}</div>'
        
        return f"""
        {self.create_section_header("References")}
        {refs_html}
        """
    
    def clean_html_content(self, content: str) -> str:
        """Clean HTML content for safe rendering"""
        # Remove invisible characters and special symbols
        content = re.sub(r'[\u00A0\u2000-\u200F\u2028-\u202F\u205F-\u206F\u3000\uFEFF]', ' ', content)
        content = re.sub(r'[^\x00-\x7F]+', ' ', content)  # Remove non-ASCII characters
        content = re.sub(r'[•▪▫◦‣⁃]', '•', content)  # Normalize bullet points
        content = re.sub(r'[–—]', '-', content)  # Normalize dashes
        
        # Remove table formatting artifacts
        content = re.sub(r'^\d+\.\d+\|.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\d+\.\d+---.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\|.*\|$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
        
        # Clean up numbering issues
        content = re.sub(r'^\d+\.\d+\|?\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\d+\.\d+---\s*', '', content, flags=re.MULTILINE)
        
        # Convert markdown to HTML
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        content = re.sub(r'<br\s*/?>', '<br/>', content, flags=re.IGNORECASE)
        
        # Remove any potentially problematic HTML except allowed tags
        content = re.sub(r'<[^>]+>', lambda m: m.group(0) if m.group(0) in ['<strong>', '</strong>', '<em>', '</em>', '<br/>'] else '', content)
        
        # Clean up extra whitespace
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        return content
    
    def generate_pdf(self, content_data: Dict[str, Any]) -> str:
        """Generate PDF using xhtml2pdf"""
        
        # Build HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            {self.create_css_styles()}
        </head>
        <body>
        """
        
        # Cover page
        title = content_data.get('title', 'Strategic Analysis Report')
        subtitle = content_data.get('subtitle', 'Solutions for a sustainable future')
        html_content += self.create_cover_page(title, subtitle)
        
        # Table of contents
        sections = [
            "Executive Summary",
            "Key Findings", 
            "Strategic Analysis",
            "Recommendations",
            "Implementation Roadmap",
            "References"
        ]
        html_content += self.create_table_of_contents(sections)
        
        # Executive Summary
        if content_data.get('executive_summary'):
            html_content += f"""
            {self.create_section_header("Executive Summary")}
            <div class="body-text">{self.clean_html_content(content_data['executive_summary'])}</div>
            """
        
        # Key Findings
        if content_data.get('key_findings'):
            findings = content_data['key_findings']
            if isinstance(findings, str):
                findings = [f.strip() for f in findings.split('\n') if f.strip()]
            html_content += self.create_key_findings(findings)
        
        # Strategic Analysis
        if content_data.get('analysis'):
            html_content += self.create_analysis_section(content_data['analysis'])
        
        # Recommendations
        if content_data.get('recommendations'):
            recommendations = content_data['recommendations']
            if isinstance(recommendations, str):
                recommendations = [r.strip() for r in recommendations.split('\n') if r.strip()]
            html_content += self.create_recommendations(recommendations)
        
        # Implementation Roadmap
        if content_data.get('implementation'):
            roadmap_data = self.parse_roadmap_data(content_data['implementation'])
            html_content += self.create_implementation_roadmap(roadmap_data)
        
        # References
        if content_data.get('references'):
            references = content_data['references']
            if isinstance(references, str):
                references = [ref.strip() for ref in references.split('\n') if ref.strip()]
            html_content += self.create_references(references)
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content
    
    def parse_roadmap_data(self, implementation_text: str) -> List[Dict]:
        """Parse implementation text into roadmap data structure"""
        roadmap_data = []
        
        lines = [line.strip() for line in implementation_text.split('\n') if line.strip()]
        table_rows = []
        
        for line in lines:
            if '|' in line and not line.startswith('---'):
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if len(cells) >= 4:
                    table_rows.append(cells)
        
        for row in table_rows[1:]:  # Skip header
            roadmap_data.append({
                'phase': row[0] if len(row) > 0 else '',
                'timeline': row[1] if len(row) > 1 else '',
                'milestones': row[2] if len(row) > 2 else '',
                'metrics': row[3] if len(row) > 3 else ''
            })
        
        return roadmap_data

def create_xhtml2pdf_report(content: str, filename: str = "xhtml2pdf_report.pdf") -> str:
    """Create PDF report using xhtml2pdf template"""
    
    # Parse content into structured data
    content_data = parse_content_to_xhtml_data(content)
    
    # Create template
    template = XHTML2PDFTemplate()
    
    # Generate HTML
    html_content = template.generate_pdf(content_data)
    
    # Convert to PDF
    with open(filename, 'wb') as result_file:
        pisa_status = pisa.CreatePDF(html_content, dest=result_file)
    
    if pisa_status.err:
        raise Exception(f"PDF generation failed: {pisa_status.err}")
    
    return filename

def parse_content_to_xhtml_data(content: str) -> Dict[str, Any]:
    """Parse markdown content into structured data for xhtml2pdf templates"""
    
    sections = {
        'title': '',
        'subtitle': '',
        'executive_summary': '',
        'key_findings': [],
        'analysis': '',
        'recommendations': [],
        'implementation': '',
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
    # Test the xhtml2pdf template system
    test_content = """
# Strategic Analysis: Digital Transformation in Healthcare

## Executive Summary
This comprehensive analysis examines the strategic implementation of digital transformation initiatives in healthcare institutions, revealing significant opportunities for operational efficiency and patient care improvement.

## Key Findings
1. **Technology Integration**: 78% of surveyed institutions report improved operational efficiency
2. **Patient Experience**: Digital platforms increase patient engagement by 34%
3. **Cost Optimization**: Automated systems reduce administrative costs by 22%

## Strategic Analysis
The digital transformation landscape presents both significant opportunities and challenges.

## Recommendations
1. **Establish Digital Governance Framework** - Create cross-functional steering committee
2. **Pilot High-Impact Initiatives** - Start with patient-facing services
3. **Invest in Change Management** - Comprehensive training and communication

## Implementation Roadmap

| Phase | Timeline | Key Milestones | Success Metrics |
|-------|----------|----------------|-----------------|
| Phase 1 | Month 1-3 | Form Steering Committee | Governance charter |
| Phase 2 | Month 4-6 | Inventory systems | Data architecture |

## References
1. Smith, J. (2024). Digital Transformation in Healthcare.
2. Johnson, M. (2024). Strategic Implementation of Digital Twins.
"""
    
    pdf_path = create_xhtml2pdf_report(test_content, "test_xhtml2pdf_report.pdf")
    print(f"xhtml2pdf PDF generated: {pdf_path}")

"""
PDF Report Generator
Creates professional PDF reports from analysis results
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import json
import os


class PDFReportGenerator:
    """Generates professional PDF reports"""
    
    def __init__(self, analysis_file, output_pdf):
        self.analysis_file = analysis_file
        self.output_pdf = output_pdf
        
        # Load analysis data
        with open(analysis_file, 'r', encoding='utf-8') as f:
            self.analysis = json.load(f)
        
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Info box style
        self.styles.add(ParagraphStyle(
            name='InfoBox',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            leftIndent=20,
            rightIndent=20,
            spaceAfter=12,
            borderColor=colors.HexColor('#3498db'),
            borderWidth=1,
            borderPadding=10,
            backColor=colors.HexColor('#ecf0f1')
        ))
    
    def add_cover_page(self):
        """Add cover page"""
        # Spacer to center content
        self.story.append(Spacer(1, 2*inch))
        
        # Main title
        title = Paragraph("Web Scraping Analysis Report", self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Subtitle with URL
        url = self.analysis.get('url', 'Unknown URL')
        subtitle = Paragraph(f"<font size=12>Analysis of: {url}</font>", self.styles['Normal'])
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Date
        analyzed_at = self.analysis.get('analyzed_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        date_text = Paragraph(f"<font size=10>Generated on: {analyzed_at}</font>", self.styles['Normal'])
        self.story.append(date_text)
        
        self.story.append(PageBreak())
    
    def add_executive_summary(self):
        """Add executive summary section"""
        self.story.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        stats = self.analysis.get('statistics', {})
        
        summary_data = [
            ["Metric", "Value"],
            ["Total Records", str(stats.get('total_rows', 'N/A'))],
            ["Total Columns", str(stats.get('total_columns', 'N/A'))],
            ["Data Size", stats.get('memory_usage', 'N/A')],
            ["Analysis Date", self.analysis.get('analyzed_at', 'N/A')]
        ]
        
        table = Table(summary_data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ecf0f1')])
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_column_analysis(self):
        """Add column-by-column analysis"""
        self.story.append(Paragraph("Column Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        stats = self.analysis.get('statistics', {})
        column_details = stats.get('column_details', {})
        
        for col_name, col_data in list(column_details.items())[:10]:  # First 10 columns
            # Column name
            col_title = Paragraph(f"<b>{col_name}</b>", self.styles['Normal'])
            self.story.append(col_title)
            
            # Column stats
            info_lines = [
                f"Type: {col_data.get('dtype', 'Unknown')}",
                f"Non-null: {col_data.get('non_null', 0)} ({col_data.get('non_null', 0) / stats.get('total_rows', 1) * 100:.1f}%)",
                f"Unique values: {col_data.get('unique', 0)}"
            ]
            
            # Add numeric stats if available
            if 'mean' in col_data and col_data['mean'] is not None:
                info_lines.append(f"Mean: {col_data['mean']:.2f}")
                info_lines.append(f"Range: {col_data.get('min', 0):.2f} to {col_data.get('max', 0):.2f}")
            
            # Add text stats if available
            if 'avg_length' in col_data:
                info_lines.append(f"Avg length: {col_data['avg_length']:.0f} characters")
            
            info_text = "<br/>".join(info_lines)
            info_para = Paragraph(info_text, self.styles['Normal'])
            self.story.append(info_para)
            self.story.append(Spacer(1, 0.15*inch))
    
    def add_insights(self):
        """Add insights section"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Key Insights", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        insights = self.analysis.get('insights', [])
        
        if not insights:
            self.story.append(Paragraph("No specific insights generated.", self.styles['Normal']))
        else:
            for i, insight in enumerate(insights, 1):
                # Insight icon based on type
                insight_type = insight.get('type', 'info')
                icon = "ℹ️" if insight_type == 'info' else "⚠️" if insight_type == 'warning' else "📊"
                
                text = f"{icon} {insight.get('message', 'No message')}"
                para = Paragraph(text, self.styles['Normal'])
                self.story.append(para)
                self.story.append(Spacer(1, 0.1*inch))
    
    def add_visualizations(self):
        """Add visualization charts"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Data Visualizations", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        charts = self.analysis.get('charts', [])
        
        if not charts:
            self.story.append(Paragraph("No visualizations available.", self.styles['Normal']))
            return
        
        for chart_path in charts:
            if os.path.exists(chart_path):
                try:
                    # Add chart title
                    chart_name = os.path.basename(chart_path).replace('.png', '').replace('_', ' ').title()
                    self.story.append(Paragraph(chart_name, self.styles['Heading3']))
                    self.story.append(Spacer(1, 0.1*inch))
                    
                    # Add image
                    img = Image(chart_path, width=6*inch, height=3.5*inch)
                    self.story.append(img)
                    self.story.append(Spacer(1, 0.3*inch))
                    
                except Exception as e:
                    self.story.append(Paragraph(f"Could not load chart: {chart_path}", self.styles['Normal']))
                    print(f"   ⚠️  Error adding chart {chart_path}: {e}")
    
    def add_footer(self):
        """Add footer information"""
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 2*inch))
        
        footer_text = f"""
        <para align=center>
        <font size=10>
        <b>Report Generated</b><br/>
        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/><br/>
        Generated by Intelligent Web Scraper<br/>
        © 2025 All Rights Reserved
        </font>
        </para>
        """
        
        self.story.append(Paragraph(footer_text, self.styles['Normal']))
    
    def generate_pdf(self):
        """Generate the complete PDF"""
        print(f"\n📄 Generating PDF report: {self.output_pdf}")
        
        # Create document
        doc = SimpleDocTemplate(
            self.output_pdf,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build content
        self.add_cover_page()
        self.add_executive_summary()
        self.add_column_analysis()
        self.add_insights()
        self.add_visualizations()
        self.add_footer()
        
        # Build PDF
        try:
            doc.build(self.story)
            print(f"   ✅ PDF generated successfully")
            print(f"   📄 Location: {self.output_pdf}")
            return self.output_pdf
        except Exception as e:
            print(f"   ❌ Error generating PDF: {e}")
            return None


def generate_pdf_report(analysis_json, output_pdf):
    """Convenience function"""
    generator = PDFReportGenerator(analysis_json, output_pdf)
    return generator.generate_pdf()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 2:
        analysis_file = sys.argv[1]
        output_file = sys.argv[2]
        generate_pdf_report(analysis_file, output_file)
    else:
        print("Usage: python pdf_generator.py <analysis.json> <output.pdf>")

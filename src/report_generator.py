from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import os
from .config import Config

class ReportGenerator:
    def __init__(self, logger, scraper):
        self.logger = logger
        self.scraper = scraper
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#444444'),
            spaceAfter=6
        )
    
    def generate_report(self, csv_filepath=None):
        """Generate a comprehensive PDF report"""
        stats = self.logger.get_stats()
        metadata = self.scraper.get_metadata()
        data = self.scraper.get_data()
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        domain = metadata.get('domain', 'unknown')
        clean_domain = domain.replace('.', '_')
        filename = f"report_{clean_domain}_{timestamp}.pdf"
        filepath = os.path.join(Config.REPORTS_DIR, filename)
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
            
            story = []
            
            # Title
            title = Paragraph("Web Scraping Report", self.title_style)
            story.append(title)
            story.append(Spacer(1, 0.2*inch))
            
            # Metadata Section
            story.append(Paragraph("Target Information", self.heading_style))
            
            meta_data = [
                ['URL:', metadata.get('url', 'N/A')],
                ['Page Title:', metadata.get('title', 'N/A')],
                ['Domain:', metadata.get('domain', 'N/A')],
                ['Scraped On:', stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            meta_table = Table(meta_data, colWidths=[1.5*inch, 5*inch])
            meta_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            story.append(meta_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Statistics Section
            story.append(Paragraph("Scraping Statistics", self.heading_style))
            
            duration_str = f"{stats['duration']:.2f} seconds"
            
            stats_data = [
                ['Pages Scraped:', str(stats['pages_scraped'])],
                ['Items Extracted:', str(stats['items_extracted'])],
                ['Duration:', duration_str],
                ['Warnings:', str(stats['warnings'])],
                ['Errors:', str(stats['errors'])],
                ['Status:', 'Completed Successfully' if stats['errors'] == 0 else 'Completed with Errors']
            ]
            
            stats_table = Table(stats_data, colWidths=[1.5*inch, 5*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Data Summary Section
            story.append(Paragraph("Data Summary", self.heading_style))
            
            if data:
                summary_text = f"Successfully extracted {len(data)} record(s) from the target webpage."
                story.append(Paragraph(summary_text, self.normal_style))
                story.append(Spacer(1, 0.1*inch))
                
                # Show column names
                if isinstance(data[0], dict):
                    columns = list(data[0].keys())
                    columns_text = f"<b>Columns extracted:</b> {', '.join(columns[:10])}"
                    if len(columns) > 10:
                        columns_text += f" ... and {len(columns) - 10} more"
                    story.append(Paragraph(columns_text, self.normal_style))
                
                # Sample data preview (first 5 records)
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph("Data Preview (First 5 Records)", self.heading_style))
                
                preview_data = data[:5]
                if preview_data and isinstance(preview_data[0], dict):
                    # Create table with first few columns
                    columns_to_show = list(preview_data[0].keys())[:5]
                    
                    table_data = [columns_to_show]
                    for record in preview_data:
                        row = [str(record.get(col, ''))[:50] for col in columns_to_show]
                        table_data.append(row)
                    
                    preview_table = Table(table_data, repeatRows=1)
                    preview_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
                    ]))
                    
                    story.append(preview_table)
            else:
                story.append(Paragraph("No data was extracted from the target page.", self.normal_style))
            
            story.append(Spacer(1, 0.3*inch))
            
            # Output Files Section
            story.append(Paragraph("Output Files", self.heading_style))
            
            output_info = []
            if csv_filepath:
                output_info.append(['CSV Data File:', os.path.basename(csv_filepath)])
            output_info.append(['Log File:', os.path.basename(self.logger.get_log_file())])
            output_info.append(['Report File:', filename])
            
            output_table = Table(output_info, colWidths=[1.5*inch, 5*inch])
            output_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            story.append(output_table)
            
            # Footer
            story.append(Spacer(1, 0.5*inch))
            footer_text = f"Report generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}"
            story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=self.styles['Normal'], 
                                                               fontSize=8, textColor=colors.grey, 
                                                               alignment=TA_CENTER)))
            
            # Build PDF
            doc.build(story)
            
            self.logger.info(f"Report generated: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to generate report: {str(e)}")
            return None

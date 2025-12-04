"""
Auto Scraper Workflow
Professional automated web scraping workflow:
1. Analyze HTML structure
2. Generate custom scraper
3. Run scraper to extract data
4. Analyze data and create visualizations
5. Generate professional PDF report
"""

import sys
import os
from datetime import datetime
import subprocess

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from intelligent_analyzer import IntelligentAnalyzer
from scraper_generator import ScraperGenerator
from data_analyzer import DataAnalyzer
from pdf_generator import PDFReportGenerator


class AutoScraperWorkflow:
    """Complete automated scraping workflow"""
    
    def __init__(self, url, output_dir=None):
        self.url = url
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), '..', 'outputs')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate base filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        domain = url.split('/')[2].replace('.', '_')
        self.base_name = f"{domain}_{timestamp}"
        
        # File paths
        self.analysis_file = os.path.join(self.output_dir, f'{self.base_name}_analysis.json')
        self.scraper_file = os.path.join(self.output_dir, f'{self.base_name}_scraper.py')
        self.data_file = None  # Will be set by scraper
        self.data_analysis_file = os.path.join(self.output_dir, f'{self.base_name}_data_analysis.json')
        self.pdf_report = os.path.join(self.output_dir, f'{self.base_name}_report.pdf')
        
        self.results = {
            'url': url,
            'started_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'steps': [],
            'files_generated': []
        }
    
    def log_step(self, step_name, status, details=None):
        """Log a workflow step"""
        step = {
            'name': step_name,
            'status': status,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'details': details or {}
        }
        self.results['steps'].append(step)
    
    def print_header(self):
        """Print workflow header"""
        print("\n" + "=" * 100)
        print("🤖 INTELLIGENT WEB SCRAPER WORKFLOW")
        print("=" * 100)
        print(f"\n🌐 Target URL: {self.url}")
        print(f"📁 Output Directory: {self.output_dir}")
        print(f"🕐 Started: {self.results['started_at']}")
        print("\n" + "=" * 100)
    
    def step1_analyze_html(self):
        """Step 1: Analyze HTML structure"""
        print("\n" + "🔹" * 50)
        print("STEP 1: ANALYZING HTML STRUCTURE")
        print("🔹" * 50)
        
        try:
            analyzer = IntelligentAnalyzer(self.url)
            analysis = analyzer.run_full_analysis(self.analysis_file)
            
            if analysis:
                self.log_step('html_analysis', 'success', {
                    'analysis_file': self.analysis_file,
                    'total_elements': analysis['structure'].get('total_elements', 0)
                })
                self.results['files_generated'].append(self.analysis_file)
                return True
            else:
                self.log_step('html_analysis', 'failed', {'error': 'Could not analyze page'})
                return False
        
        except Exception as e:
            self.log_step('html_analysis', 'failed', {'error': str(e)})
            print(f"\n❌ Error in Step 1: {e}")
            return False
    
    def step2_generate_scraper(self):
        """Step 2: Generate custom scraper"""
        print("\n" + "🔹" * 50)
        print("STEP 2: GENERATING CUSTOM SCRAPER")
        print("🔹" * 50)
        
        try:
            generator = ScraperGenerator(self.analysis_file)
            scraper_path = generator.generate_full_scraper(self.scraper_file)
            
            if scraper_path and os.path.exists(scraper_path):
                self.log_step('scraper_generation', 'success', {
                    'scraper_file': self.scraper_file
                })
                self.results['files_generated'].append(self.scraper_file)
                return True
            else:
                self.log_step('scraper_generation', 'failed', {'error': 'Scraper file not created'})
                return False
        
        except Exception as e:
            self.log_step('scraper_generation', 'failed', {'error': str(e)})
            print(f"\n❌ Error in Step 2: {e}")
            return False
    
    def step3_run_scraper(self):
        """Step 3: Run the generated scraper"""
        print("\n" + "🔹" * 50)
        print("STEP 3: RUNNING SCRAPER TO EXTRACT DATA")
        print("🔹" * 50)
        
        try:
            # Get Python path from venv
            venv_python = os.path.join(os.path.dirname(__file__), '..', '.venv', 'Scripts', 'python.exe')
            
            if not os.path.exists(venv_python):
                venv_python = 'python'  # Fallback to system python
            
            # Run the scraper
            result = subprocess.run(
                [venv_python, self.scraper_file],
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            print(result.stdout)
            
            # Find the generated CSV file (check even if return code != 0, as data might have been saved)
            import glob
            csv_files = glob.glob(os.path.join(self.output_dir, 'scraped_*.csv'))
            if csv_files:
                # Get the most recent one
                self.data_file = max(csv_files, key=os.path.getmtime)
                
                self.log_step('scraper_execution', 'success', {
                    'data_file': self.data_file,
                    'output': result.stdout[:500]
                })
                self.results['files_generated'].append(self.data_file)
                return True
            
            if result.returncode == 0:
                self.log_step('scraper_execution', 'warning', {
                    'message': 'Scraper ran but no CSV file found',
                    'output': result.stdout[:500]
                })
                return False
            else:
                self.log_step('scraper_execution', 'failed', {
                    'error': result.stderr[:500],
                    'return_code': result.returncode
                })
                print(f"\n❌ Scraper failed with error:\n{result.stderr}")
                return False
        
        except Exception as e:
            self.log_step('scraper_execution', 'failed', {'error': str(e)})
            print(f"\n❌ Error in Step 3: {e}")
            return False
    
    def step4_analyze_data(self):
        """Step 4: Analyze scraped data"""
        print("\n" + "🔹" * 50)
        print("STEP 4: ANALYZING SCRAPED DATA")
        print("🔹" * 50)
        
        if not self.data_file or not os.path.exists(self.data_file):
            print("⚠️  No data file to analyze")
            self.log_step('data_analysis', 'skipped', {'reason': 'No data file'})
            return False
        
        try:
            analyzer = DataAnalyzer(self.data_file)
            analysis = analyzer.run_full_analysis(self.data_analysis_file)
            
            if analysis:
                self.log_step('data_analysis', 'success', {
                    'analysis_file': self.data_analysis_file,
                    'charts_created': len(analysis.get('charts', []))
                })
                self.results['files_generated'].append(self.data_analysis_file)
                
                # Add chart files
                for chart in analysis.get('charts', []):
                    self.results['files_generated'].append(chart)
                
                return True
            else:
                self.log_step('data_analysis', 'failed', {'error': 'Analysis returned None'})
                return False
        
        except Exception as e:
            self.log_step('data_analysis', 'failed', {'error': str(e)})
            print(f"\n❌ Error in Step 4: {e}")
            return False
    
    def step5_generate_pdf(self):
        """Step 5: Generate PDF report"""
        print("\n" + "🔹" * 50)
        print("STEP 5: GENERATING PDF REPORT")
        print("🔹" * 50)
        
        if not os.path.exists(self.data_analysis_file):
            print("⚠️  No analysis file to generate PDF from")
            self.log_step('pdf_generation', 'skipped', {'reason': 'No analysis file'})
            return False
        
        try:
            generator = PDFReportGenerator(self.data_analysis_file, self.pdf_report)
            pdf_path = generator.generate_pdf()
            
            if pdf_path and os.path.exists(pdf_path):
                self.log_step('pdf_generation', 'success', {
                    'pdf_file': self.pdf_report
                })
                self.results['files_generated'].append(self.pdf_report)
                return True
            else:
                self.log_step('pdf_generation', 'failed', {'error': 'PDF file not created'})
                return False
        
        except Exception as e:
            self.log_step('pdf_generation', 'failed', {'error': str(e)})
            print(f"\n❌ Error in Step 5: {e}")
            return False
    
    def print_summary(self):
        """Print workflow summary"""
        print("\n" + "=" * 100)
        print("✅ WORKFLOW COMPLETE")
        print("=" * 100)
        
        # Step summary
        print("\n📊 Steps Summary:")
        for step in self.results['steps']:
            status_icon = "✅" if step['status'] == 'success' else "⚠️" if step['status'] == 'warning' else "❌"
            print(f"   {status_icon} {step['name']}: {step['status']}")
        
        # Files generated
        print(f"\n📁 Files Generated ({len(self.results['files_generated'])}):")
        for file_path in self.results['files_generated']:
            file_size = os.path.getsize(file_path) / 1024 if os.path.exists(file_path) else 0
            print(f"   📄 {os.path.basename(file_path)} ({file_size:.1f} KB)")
        
        # Final PDF location
        if os.path.exists(self.pdf_report):
            print(f"\n🎉 FINAL REPORT:")
            print(f"   📄 {self.pdf_report}")
            print(f"\n💡 To view the report:")
            print(f"   start {self.pdf_report}")
        
        print("\n" + "=" * 100 + "\n")
    
    def run(self):
        """Run complete workflow"""
        self.print_header()
        
        # Execute all steps
        steps = [
            self.step1_analyze_html,
            self.step2_generate_scraper,
            self.step3_run_scraper,
            self.step4_analyze_data,
            self.step5_generate_pdf
        ]
        
        for step_func in steps:
            success = step_func()
            if not success and step_func != self.step3_run_scraper:
                # Continue even if scraper fails (might still have some data)
                print(f"\n⚠️  Step failed but continuing...")
        
        # Save workflow results
        results_file = os.path.join(self.output_dir, f'{self.base_name}_workflow.json')
        import json
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.results['files_generated'].append(results_file)
        
        # Print summary
        self.print_summary()
        
        # Auto-open PDF if it exists
        if os.path.exists(self.pdf_report):
            try:
                subprocess.run(['start', self.pdf_report], shell=True)
            except:
                pass
        
        return self.results


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python auto_scraper_workflow.py <url> [output_directory]")
        print("\nExample:")
        print("  python auto_scraper_workflow.py https://example.com")
        print("  python auto_scraper_workflow.py https://example.com F:/Scrapper/outputs")
        return
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    workflow = AutoScraperWorkflow(url, output_dir)
    workflow.run()


if __name__ == '__main__':
    main()

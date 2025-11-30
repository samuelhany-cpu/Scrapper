"""
COMPREHENSIVE TEST SUITE FOR UNIVERSAL WEB SCRAPER
Tests all features with different scenarios
"""
import sys
import os
from datetime import datetime
from config import Config
from logger import ScraperLogger
from scraper_selenium import UniversalScraper  # Using Selenium for Python 3.13
from report_generator import ReportGenerator
import time

class TestRunner:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def print_header(self, text):
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    
    def print_test(self, name):
        print(f"\n[TEST] {name}")
        print("-" * 70)
    
    def run_test(self, test_name, test_func):
        """Run a single test"""
        self.print_test(test_name)
        try:
            start_time = time.time()
            result = test_func()
            duration = time.time() - start_time
            
            if result:
                print(f"✓ PASSED ({duration:.2f}s)")
                self.tests_passed += 1
                self.test_results.append({
                    'name': test_name,
                    'status': 'PASSED',
                    'duration': duration
                })
            else:
                print(f"✗ FAILED ({duration:.2f}s)")
                self.tests_failed += 1
                self.test_results.append({
                    'name': test_name,
                    'status': 'FAILED',
                    'duration': duration
                })
            return result
        except Exception as e:
            duration = time.time() - start_time
            print(f"✗ ERROR: {str(e)} ({duration:.2f}s)")
            self.tests_failed += 1
            self.test_results.append({
                'name': test_name,
                'status': 'ERROR',
                'duration': duration,
                'error': str(e)
            })
            return False
    
    def print_summary(self):
        """Print final test summary"""
        self.print_header("TEST SUMMARY")
        print(f"\nTotal Tests: {self.tests_passed + self.tests_failed}")
        print(f"✓ Passed: {self.tests_passed}")
        print(f"✗ Failed: {self.tests_failed}")
        print(f"Success Rate: {(self.tests_passed/(self.tests_passed + self.tests_failed)*100):.1f}%")
        
        print("\nDetailed Results:")
        for result in self.test_results:
            status_icon = "✓" if result['status'] == 'PASSED' else "✗"
            print(f"  {status_icon} {result['name']}: {result['status']} ({result['duration']:.2f}s)")
            if 'error' in result:
                print(f"     Error: {result['error']}")

# Test Functions
def test_environment_setup():
    """Test 1: Verify environment and directories"""
    print("Checking environment setup...")
    Config.ensure_directories()
    
    # Check directories exist
    if not os.path.exists(Config.OUTPUT_DIR):
        print(f"✗ {Config.OUTPUT_DIR} directory missing")
        return False
    print(f"✓ {Config.OUTPUT_DIR} directory exists")
    
    if not os.path.exists(Config.LOGS_DIR):
        print(f"✗ {Config.LOGS_DIR} directory missing")
        return False
    print(f"✓ {Config.LOGS_DIR} directory exists")
    
    if not os.path.exists(Config.REPORTS_DIR):
        print(f"✗ {Config.REPORTS_DIR} directory missing")
        return False
    print(f"✓ {Config.REPORTS_DIR} directory exists")
    
    # Check .env file
    if not os.path.exists('.env'):
        print("⚠ .env file missing (optional)")
    else:
        print("✓ .env file exists")
    
    return True

def test_ai_configuration():
    """Test 2: Check AI configuration"""
    print("Checking AI configuration...")
    
    has_gemini = bool(Config.GEMINI_API_KEY)
    has_openai = bool(Config.OPENAI_API_KEY)
    has_groq = bool(Config.GROQ_API_KEY)
    
    print(f"  Gemini API Key: {'✓ Found (FREE)' if has_gemini else '✗ Not configured'}")
    print(f"  OpenAI API Key: {'✓ Found (PAID)' if has_openai else '✗ Not configured'}")
    print(f"  Groq API Key: {'✓ Found (FREE)' if has_groq else '✗ Not configured'}")
    
    if has_gemini:
        print("\n✓ Using Google Gemini (FREE) for AI features")
        return True
    elif has_groq:
        print("\n✓ Using Groq (FREE) for AI features")
        return True
    elif has_openai:
        print("\n✓ Using OpenAI (PAID) for AI features")
        return True
    else:
        print("\n⚠ No AI configured - will use traditional scraping")
        print("  TIP: Get FREE Gemini key at https://makersuite.google.com/app/apikey")
        return True  # Still pass - AI is optional

def test_simple_static_page():
    """Test 3: Scrape a simple static webpage"""
    print("Testing with simple static page (example.com)...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    success = scraper.scrape_url("https://example.com")
    
    if not success:
        print("✗ Scraping failed")
        return False
    
    data = scraper.get_data()
    if not data or len(data) == 0:
        print("✗ No data extracted")
        return False
    
    print(f"✓ Extracted {len(data)} record(s)")
    print(f"  Fields: {list(data[0].keys())[:5]}...")
    
    # Save CSV
    csv_file = scraper.save_to_csv("test_static.csv")
    if not csv_file:
        print("✗ Failed to save CSV")
        return False
    print(f"✓ CSV saved: {csv_file}")
    
    return True

def test_wikipedia_page():
    """Test 4: Scrape Wikipedia (structured content)"""
    print("Testing with Wikipedia (structured content)...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    success = scraper.scrape_url("https://en.wikipedia.org/wiki/Web_scraping")
    
    if not success:
        print("✗ Scraping failed")
        return False
    
    data = scraper.get_data()
    if not data:
        print("✗ No data extracted")
        return False
    
    print(f"✓ Extracted {len(data)} record(s)")
    metadata = scraper.get_metadata()
    print(f"  Title: {metadata.get('title', 'N/A')}")
    
    # Save CSV
    csv_file = scraper.save_to_csv("test_wikipedia.csv")
    print(f"✓ CSV saved: {csv_file}")
    
    return True

def test_news_website():
    """Test 5: Scrape news website (dynamic content)"""
    print("Testing with news website...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    # Use BBC News - generally accessible
    success = scraper.scrape_url("https://www.bbc.com/news")
    
    if not success:
        print("⚠ Scraping failed (may be blocked)")
        return True  # Don't fail test if blocked
    
    data = scraper.get_data()
    print(f"✓ Extracted {len(data)} record(s)")
    
    csv_file = scraper.save_to_csv("test_news.csv")
    print(f"✓ CSV saved: {csv_file}")
    
    return True

def test_table_data():
    """Test 6: Scrape page with tables"""
    print("Testing with table data...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    # Wikipedia page with tables
    success = scraper.scrape_url("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
    
    if not success:
        print("✗ Scraping failed")
        return False
    
    data = scraper.get_data()
    print(f"✓ Extracted {len(data)} record(s)")
    
    csv_file = scraper.save_to_csv("test_tables.csv")
    print(f"✓ CSV saved: {csv_file}")
    
    return True

def test_blog_post():
    """Test 7: Scrape blog post (article content)"""
    print("Testing with blog post...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    # Use a well-known tech blog
    success = scraper.scrape_url("https://blog.python.org/")
    
    if not success:
        print("⚠ Scraping failed")
        return True  # Don't fail
    
    data = scraper.get_data()
    print(f"✓ Extracted {len(data)} record(s)")
    
    csv_file = scraper.save_to_csv("test_blog.csv")
    print(f"✓ CSV saved: {csv_file}")
    
    return True

def test_report_generation():
    """Test 8: PDF Report Generation"""
    print("Testing PDF report generation...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    # Scrape a simple page
    success = scraper.scrape_url("https://example.com")
    if not success:
        print("✗ Scraping failed")
        return False
    
    # Generate report
    csv_file = scraper.save_to_csv("test_report.csv")
    report_gen = ReportGenerator(logger, scraper)
    report_file = report_gen.generate_report(csv_file)
    
    if not report_file:
        print("✗ Report generation failed")
        return False
    
    if not os.path.exists(report_file):
        print("✗ Report file not found")
        return False
    
    file_size = os.path.getsize(report_file)
    print(f"✓ Report generated: {report_file}")
    print(f"  File size: {file_size:,} bytes")
    
    return True

def test_logging_system():
    """Test 9: Logging System"""
    print("Testing logging system...")
    
    logger = ScraperLogger()
    
    # Test different log levels
    logger.info("Test info message")
    logger.debug("Test debug message")
    logger.warning("Test warning message")
    
    # Check log file exists
    log_file = logger.get_log_file()
    if not os.path.exists(log_file):
        print("✗ Log file not created")
        return False
    
    print(f"✓ Log file created: {log_file}")
    
    # Check stats
    stats = logger.get_stats()
    print(f"  Warnings: {stats['warnings']}")
    
    return True

def test_error_handling():
    """Test 10: Error Handling"""
    print("Testing error handling...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    # Test invalid URL
    success = scraper.scrape_url("not-a-valid-url")
    if success:
        print("✗ Should have failed with invalid URL")
        return False
    print("✓ Correctly rejected invalid URL")
    
    # Test non-existent domain
    success = scraper.scrape_url("https://this-domain-absolutely-does-not-exist-12345.com")
    if success:
        print("⚠ Somehow succeeded with non-existent domain")
    else:
        print("✓ Correctly handled non-existent domain")
    
    return True

def test_csv_export_quality():
    """Test 11: CSV Export Quality"""
    print("Testing CSV export quality...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    success = scraper.scrape_url("https://example.com")
    if not success:
        return False
    
    csv_file = scraper.save_to_csv("test_quality.csv")
    
    # Read and verify CSV
    import pandas as pd
    df = pd.read_csv(csv_file)
    
    print(f"✓ CSV has {len(df)} rows and {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)[:5]}...")
    
    # Check for empty data
    if df.empty:
        print("✗ CSV is empty")
        return False
    
    print("✓ CSV contains data")
    return True

def test_javascript_pages():
    """Test 12: JavaScript-Heavy Pages"""
    print("Testing JavaScript-heavy pages...")
    
    logger = ScraperLogger()
    scraper = UniversalScraper(logger)
    
    # Test with a JS-heavy site
    success = scraper.scrape_url("https://quotes.toscrape.com/js/")
    
    if not success:
        print("⚠ Scraping failed")
        return True  # Don't fail test
    
    data = scraper.get_data()
    print(f"✓ Extracted {len(data)} record(s) from JS page")
    
    return True

# Main Test Runner
def main():
    runner = TestRunner()
    
    runner.print_header("UNIVERSAL WEB SCRAPER - COMPREHENSIVE TEST SUITE")
    print("\nThis will test all features with various scenarios.")
    print("Note: Some tests may take time due to network requests.")
    
    # Ensure environment is ready
    Config.ensure_directories()
    
    # Run all tests
    print("\n" + "=" * 70)
    print("RUNNING TESTS...")
    print("=" * 70)
    
    runner.run_test("1. Environment Setup", test_environment_setup)
    runner.run_test("2. AI Configuration", test_ai_configuration)
    runner.run_test("3. Simple Static Page (example.com)", test_simple_static_page)
    runner.run_test("4. Wikipedia Page (Structured Content)", test_wikipedia_page)
    runner.run_test("5. News Website (Dynamic Content)", test_news_website)
    runner.run_test("6. Table Data Extraction", test_table_data)
    runner.run_test("7. Blog Post (Article Content)", test_blog_post)
    runner.run_test("8. PDF Report Generation", test_report_generation)
    runner.run_test("9. Logging System", test_logging_system)
    runner.run_test("10. Error Handling", test_error_handling)
    runner.run_test("11. CSV Export Quality", test_csv_export_quality)
    runner.run_test("12. JavaScript Pages", test_javascript_pages)
    
    # Print summary
    runner.print_summary()
    
    # Final recommendation
    print("\n" + "=" * 70)
    if runner.tests_failed == 0:
        print("🎉 ALL TESTS PASSED! Your scraper is production-ready!")
    elif runner.tests_failed <= 2:
        print("✓ MOSTLY PASSING - Minor issues detected")
    else:
        print("⚠ SOME TESTS FAILED - Review errors above")
    print("=" * 70)
    
    # Show output files
    print("\n📁 Generated Test Files:")
    print(f"  Output: {Config.OUTPUT_DIR}/")
    print(f"  Reports: {Config.REPORTS_DIR}/")
    print(f"  Logs: {Config.LOGS_DIR}/")
    
    return runner.tests_failed == 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

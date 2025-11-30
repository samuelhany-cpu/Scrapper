"""
Quick test script to verify the scraper works without errors
"""
from config import Config
from logger import ScraperLogger
from scraper_sync import UniversalScraper
from report_generator import ReportGenerator

def test_scraper():
    """Test scraping a simple page"""
    print("Testing Universal Web Scraper...")
    print("-" * 50)
    
    # Test URL - a simple, reliable test page
    test_url = "https://example.com"
    
    # Create logger
    logger = ScraperLogger()
    logger.info("Starting test scraping...")
    
    # Create scraper
    scraper = UniversalScraper(logger)
    
    # Run scraping
    print(f"\nScraping test URL: {test_url}")
    success = scraper.scrape_url(test_url)
    
    if success:
        print("\n✓ Scraping completed successfully!")
        
        # Get data
        data = scraper.get_data()
        print(f"✓ Extracted {len(data)} record(s)")
        
        # Save to CSV
        csv_file = scraper.save_to_csv("test_output.csv")
        if csv_file:
            print(f"✓ CSV saved to: {csv_file}")
        
        # Generate report
        report_gen = ReportGenerator(logger, scraper)
        report_file = report_gen.generate_report(csv_file)
        if report_file:
            print(f"✓ Report generated: {report_file}")
        
        # Show stats
        stats = logger.get_stats()
        print(f"\nStatistics:")
        print(f"  - Pages scraped: {stats['pages_scraped']}")
        print(f"  - Items extracted: {stats['items_extracted']}")
        print(f"  - Duration: {stats['duration']:.2f} seconds")
        print(f"  - Errors: {stats['errors']}")
        print(f"  - Warnings: {stats['warnings']}")
        
        print("\n" + "=" * 50)
        print("All tests passed! The scraper is working correctly.")
        print("=" * 50)
        
    else:
        print("\n✗ Scraping failed. Check the logs for details.")
        return False
    
    return True

if __name__ == "__main__":
    # Ensure directories exist
    Config.ensure_directories()
    
    # Run test
    result = test_scraper()
    
    if result:
        print("\nYou can now use the web interface by running:")
        print("  run.bat")
        print("\nOr manually:")
        print("  .venv\\Scripts\\streamlit run app.py")
    else:
        print("\nPlease check the logs directory for error details.")

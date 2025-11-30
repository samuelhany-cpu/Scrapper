"""
Test the Adaptive Smart Scraper
"""
from config import Config
from logger import ScraperLogger
from adaptive_scraper import AdaptiveSmartScraper
import json

def test_adaptive_scraper():
    print("=" * 70)
    print("TESTING ADAPTIVE SMART SCRAPER")
    print("=" * 70)
    
    Config.ensure_directories()
    
    # Test URLs with different structures
    test_cases = [
        {
            'name': 'Simple Static Page',
            'url': 'https://example.com',
            'expected_pattern': 'general_webpage'
        },
        {
            'name': 'Wikipedia (Tables & Lists)',
            'url': 'https://en.wikipedia.org/wiki/List_of_countries_by_population',
            'expected_pattern': 'tabular_data'
        },
        {
            'name': 'News Site',
            'url': 'https://news.ycombinator.com',
            'expected_pattern': 'blog_listing'
        }
    ]
    
    for idx, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {idx}: {test['name']}")
        print(f"URL: {test['url']}")
        print('='*70)
        
        logger = ScraperLogger()
        scraper = AdaptiveSmartScraper(logger)
        
        success = scraper.scrape_url(test['url'])
        
        if success:
            print(f"\n✅ SUCCESS!")
            
            # Get results
            data = scraper.get_data()
            metadata = scraper.get_metadata()
            analysis = scraper.get_structure_analysis()
            
            print(f"\n📊 Results:")
            print(f"   Items extracted: {len(data)}")
            print(f"   Page title: {metadata.get('title', 'N/A')}")
            
            print(f"\n🧠 Structure Analysis:")
            structure = analysis['structure']
            print(f"   Domain: {structure.get('domain')}")
            print(f"   Tables: {structure.get('table_count')}")
            print(f"   Lists: {structure.get('list_count')}")
            print(f"   Articles: {structure.get('article_count')}")
            print(f"   Detected patterns: {structure.get('patterns')}")
            
            print(f"\n🎯 Strategy:")
            strategy = analysis['strategy']
            print(f"   Type: {strategy.get('type')}")
            print(f"   Methods: {strategy.get('extraction_methods')}")
            
            # Save data
            csv_file = scraper.save_to_csv(f"test_adaptive_{idx}.csv")
            print(f"\n💾 Saved to: {csv_file}")
            
            # Show sample data
            if data:
                print(f"\n📋 Sample Data (first record):")
                first_item = data[0]
                for key, value in list(first_item.items())[:5]:
                    value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"   {key}: {value_str}")
        else:
            print(f"\n❌ FAILED!")
        
        print(f"\n{'-'*70}\n")
    
    print("\n" + "=" * 70)
    print("TESTING COMPLETE!")
    print("=" * 70)
    print(f"\nCheck output/ directory for CSV files")
    print(f"Check logs/ directory for detailed logs")

if __name__ == "__main__":
    test_adaptive_scraper()

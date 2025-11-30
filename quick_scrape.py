"""Quick CLI for scraping websites with adaptive scraper (requests-only version)"""
import sys
import requests
from bs4 import BeautifulSoup
from adaptive_scraper import AdaptiveSmartScraper
from logger import ScraperLogger
import pandas as pd
import os
from datetime import datetime
import re
from config import Config

def scrape_with_requests(url):
    """Scrape using requests (faster, no browser needed)"""
    # Initialize
    logger = ScraperLogger('adaptive_quick')
    scraper = AdaptiveSmartScraper(logger)
    
    print(f"\n🔗 Scraping: {url}")
    print("⚡ Using quick mode (requests)...\n")
    
    # Fetch page
    headers = {'User-Agent': Config.USER_AGENT}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    # Parse
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Analyze and extract
    print("📊 Analyzing structure...")
    structure = scraper.analyze_structure(soup, url)
    strategy = scraper.determine_strategy(structure)
    
    print(f"🎯 Strategy: {strategy['type']}")
    print("⚙️  Extracting data...\n")
    
    data = scraper.adaptive_extract(soup, url, strategy)
    
    if not data:
        print("❌ No data extracted!")
        return None
    
    # Save to CSV
    domain = structure.get('domain', 'scraped')
    clean_domain = re.sub(r'[^\w\-_]', '_', domain)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{clean_domain}_{timestamp}.csv"
    filepath = os.path.join(Config.OUTPUT_DIR, filename)
    
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    # Results
    print(f"✅ Scraping completed successfully!")
    print(f"   📊 Extracted {len(data)} items")
    print(f"   📁 Saved to: {filepath}")
    print(f"   🧠 Strategy: {strategy['type']}\n")
    
    return filepath

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_scrape.py <url>")
        print("\nExample:")
        print('  python quick_scrape.py "https://www.yallakora.com/match-center"')
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        scrape_with_requests(url)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

"""
Auto-generated scraper for quotes.toscrape.com
Generated on: 2025-12-04 23:05:57
Source URL: http://quotes.toscrape.com
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time
from urllib.parse import urljoin



class QuotesToscrapeComScraper:
    """Auto-generated scraper for quotes.toscrape.com"""
    
    def __init__(self, base_url="http://quotes.toscrape.com"):
        self.base_url = base_url
        self.domain = "quotes.toscrape.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.data = []
    
    def fetch_page(self, url=None):
        """Fetch a page and return BeautifulSoup object"""
        url = url or self.base_url
        
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"   Success ({len(response.content)} bytes)")
            
            # Respectful delay
            time.sleep(1)
            
            return soup
        
        except Exception as e:
            print(f"   Error: {e}")
            return None


    def extract_data(self, soup):
        """Extract data from page based on learned patterns"""
        if not soup:
            return []
        
        items = []
        
        # Generic extraction (no specific pattern detected)
        
        # Try to find article-like content
        articles = soup.find_all(['article', 'div'], class_=True)
        
        for article in articles[:50]:  # Limit to first 50
            text = article.get_text(strip=True)
            if len(text) > 50:  # Meaningful content
                data = {
                    'content': text,
                    'classes': article.get('class', []),
                    'id': article.get('id', ''),
                }
                
                # Try to find title
                title = article.find(['h1', 'h2', 'h3'])
                if title:
                    data['title'] = title.get_text(strip=True)
                
                # Try to find links
                link = article.find('a', href=True)
                if link:
                    data['link'] = urljoin(self.base_url, link['href'])
                
                items.append(data)

        return items


    def scrape(self, url=None):
        """Main scraping method"""
        print("\n" + "=" * 100)
        print(f"Starting scrape of {self.domain}")
        print("=" * 100)
        
        soup = self.fetch_page(url)
        if not soup:
            print("❌ Failed to fetch page")
            return []
        
        items = self.extract_data(soup)
        self.data.extend(items)
        
        print(f"\nExtracted {len(items)} items")
        
        return items
    
    def save_to_csv(self, filename=None):
        """Save scraped data to CSV"""
        if not self.data:
            print("No data to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'scraped_{self.domain.replace(".", "_")}_{timestamp}.csv'
        
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\nSaved {len(self.data)} items to: {filename}")
        return filename
    
    def save_to_json(self, filename=None):
        """Save scraped data to JSON"""
        if not self.data:
            print("No data to save")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'scraped_{self.domain.replace(".", "_")}_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.data)} items to: {filename}")
        return filename
    
    def get_summary(self):
        """Get summary statistics"""
        if not self.data:
            return {"total_items": 0}
        
        df = pd.DataFrame(self.data)
        
        summary = {
            "total_items": len(self.data),
            "columns": list(df.columns),
            "sample_data": self.data[:3] if len(self.data) >= 3 else self.data
        }
        
        return summary



def main():
    """Main execution"""
    scraper = QuotesToscrapeComScraper()
    
    # Scrape the page
    items = scraper.scrape()
    
    if items:
        # Save results
        csv_file = scraper.save_to_csv()
        json_file = scraper.save_to_json()
        
        # Print summary
        print("\n" + "=" * 100)
        print("SCRAPING SUMMARY")
        print("=" * 100)
        summary = scraper.get_summary()
        print(f"Total items: {summary['total_items']}")
        print(f"Columns: {', '.join(summary['columns'])}")
        print("=" * 100)
        
        return csv_file
    else:
        print("\n⚠️  No data extracted")
        return None


if __name__ == '__main__':
    main()

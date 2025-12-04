"""
Dynamic Scraper Generator
Automatically generates custom scraper scripts based on HTML analysis results
"""

import json
import os
from datetime import datetime


class ScraperGenerator:
    """Generates custom scraper code based on analysis"""
    
    def __init__(self, analysis_data):
        if isinstance(analysis_data, str):
            # Load from file
            with open(analysis_data, 'r', encoding='utf-8') as f:
                self.analysis = json.load(f)
        else:
            self.analysis = analysis_data
        
        self.url = self.analysis['url']
        self.domain = self.analysis['domain']
        self.strategy = self.analysis.get('scraping_strategy', {})
    
    def generate_imports(self):
        """Generate import statements"""
        return '''"""
Auto-generated scraper for {domain}
Generated on: {timestamp}
Source URL: {url}
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
import time
from urllib.parse import urljoin
'''.format(
            domain=self.domain,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            url=self.url
        )
    
    def generate_scraper_class(self):
        """Generate the main scraper class"""
        class_name = ''.join(word.capitalize() for word in self.domain.replace('.', '_').replace('-', '_').split('_'))
        
        code = f'''

class {class_name}Scraper:
    """Auto-generated scraper for {self.domain}"""
    
    def __init__(self, base_url="{self.url}"):
        self.base_url = base_url
        self.domain = "{self.domain}"
        self.session = requests.Session()
        self.session.headers.update({{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }})
        self.data = []
    
    def fetch_page(self, url=None):
        """Fetch a page and return BeautifulSoup object"""
        url = url or self.base_url
        
        try:
            print(f"Fetching: {{url}}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"   Success ({{len(response.content)}} bytes)")
            
            # Respectful delay
            time.sleep(1)
            
            return soup
        
        except Exception as e:
            print(f"   Error: {{e}}")
            return None
'''
        
        return code
    
    def generate_extraction_methods(self):
        """Generate data extraction methods based on strategy"""
        code = '''
    def extract_data(self, soup):
        """Extract data from page based on learned patterns"""
        if not soup:
            return []
        
        items = []
        
'''
        
        # Generate based on strategy
        selectors = self.strategy.get('selectors', [])
        
        if selectors:
            for selector_info in selectors:
                selector = selector_info.get('selector', '')
                selector_type = selector_info.get('type', 'unknown')
                
                if selector_type == 'list_items':
                    code += f'''        # Extract list items
        list_items = soup.select("{selector}")
        print(f"   Found {{len(list_items)}} items")
        
        for item in list_items:
            data = {{}}
            
            # Extract text content
            data['text'] = item.get_text(strip=True)
            
            # Extract links
            link = item.find('a', href=True)
            if link:
                data['link'] = urljoin(self.base_url, link['href'])
                data['link_text'] = link.get_text(strip=True)
            
            # Extract any images
            img = item.find('img', src=True)
            if img:
                data['image'] = urljoin(self.base_url, img['src'])
                data['image_alt'] = img.get('alt', '')
            
            # Extract any data attributes
            for attr, value in item.attrs.items():
                if attr.startswith('data-'):
                    data[attr] = value
            
            if data:
                items.append(data)
'''
                
                elif selector_type == 'repeated_items':
                    code += f'''        # Extract repeated items
        repeated_items = soup.select("{selector}")
        print(f"   Found {{len(repeated_items)}} repeated items")
        
        for item in repeated_items:
            data = {{}}
            
            # Extract main text
            data['content'] = item.get_text(strip=True)
            
            # Extract title (common patterns)
            title = item.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if title:
                data['title'] = title.get_text(strip=True)
            
            # Extract links
            links = item.find_all('a', href=True)
            if links:
                data['links'] = [urljoin(self.base_url, link['href']) for link in links]
            
            # Extract classes (might contain metadata)
            data['classes'] = item.get('class', [])
            
            if data.get('content'):
                items.append(data)
'''
        
        else:
            # Generic extraction
            code += '''        # Generic extraction (no specific pattern detected)
        
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
'''
        
        code += '''
        return items
'''
        
        return code
    
    def generate_scrape_method(self):
        """Generate main scrape method"""
        code = '''
    def scrape(self, url=None):
        """Main scraping method"""
        print("\\n" + "=" * 100)
        print(f"Starting scrape of {self.domain}")
        print("=" * 100)
        
        soup = self.fetch_page(url)
        if not soup:
            print("❌ Failed to fetch page")
            return []
        
        items = self.extract_data(soup)
        self.data.extend(items)
        
        print(f"\\nExtracted {len(items)} items")
        
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
        
        print(f"\\nSaved {len(self.data)} items to: {filename}")
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
'''
        
        return code
    
    def generate_main(self):
        """Generate main execution block"""
        class_name = ''.join(word.capitalize() for word in self.domain.replace('.', '_').replace('-', '_').split('_'))
        
        code = f'''

def main():
    """Main execution"""
    scraper = {class_name}Scraper()
    
    # Scrape the page
    items = scraper.scrape()
    
    if items:
        # Save results
        csv_file = scraper.save_to_csv()
        json_file = scraper.save_to_json()
        
        # Print summary
        print("\\n" + "=" * 100)
        print("SCRAPING SUMMARY")
        print("=" * 100)
        summary = scraper.get_summary()
        print(f"Total items: {{summary['total_items']}}")
        print(f"Columns: {{', '.join(summary['columns'])}}")
        print("=" * 100)
        
        return csv_file
    else:
        print("\\n⚠️  No data extracted")
        return None


if __name__ == '__main__':
    main()
'''
        
        return code
    
    def generate_full_scraper(self, output_path):
        """Generate complete scraper script"""
        print(f"\n🔧 Generating custom scraper for {self.domain}...")
        
        code_parts = [
            self.generate_imports(),
            self.generate_scraper_class(),
            self.generate_extraction_methods(),
            self.generate_scrape_method(),
            self.generate_main()
        ]
        
        full_code = '\n'.join(code_parts)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_code)
        
        print(f"✅ Generated scraper: {output_path}")
        return output_path


def generate_scraper(analysis_file, output_file):
    """Convenience function"""
    generator = ScraperGenerator(analysis_file)
    return generator.generate_full_scraper(output_file)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 2:
        analysis_file = sys.argv[1]
        output_file = sys.argv[2]
        generate_scraper(analysis_file, output_file)
    else:
        print("Usage: python scraper_generator.py <analysis.json> <output_scraper.py>")

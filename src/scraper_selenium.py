"""
Universal Web Scraper - Using Selenium (Python 3.13 compatible)
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
import validators
from .config import Config
from .logger import ScraperLogger
from .ai_analyzer import AIContentAnalyzer
import re
import os
import time

class UniversalScraper:
    def __init__(self, logger):
        self.logger = logger
        self.ai_analyzer = AIContentAnalyzer(logger)
        self.scraped_data = []
        self.page_metadata = {}
        
    def scrape_url(self, url):
        """Main scraping method - Using Selenium"""
        self.logger.info(f"Starting scrape of: {url}")
        
        if not validators.url(url):
            self.logger.error(f"Invalid URL: {url}")
            return False
        
        driver = None
        try:
            # Setup Firefox options
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager
            
            firefox_options = FirefoxOptions()
            firefox_options.add_argument('--headless')
            firefox_options.set_preference('general.useragent.override', Config.USER_AGENT)
            firefox_options.set_preference('dom.webdriver.enabled', False)
            firefox_options.set_preference('useAutomationExtension', False)
            
            self.logger.debug("Launching Firefox browser...")
            
            # Initialize Firefox driver
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            driver.set_page_load_timeout(Config.REQUEST_TIMEOUT)
            driver.set_window_size(1920, 1080)
            
            # Navigate to URL
            self.logger.info(f"Loading page: {url}")
            driver.get(url)
            
            # Wait for page load
            time.sleep(Config.WAIT_FOR_LOAD / 1000)  # Convert ms to seconds
            
            # Get page info
            page_title = driver.title
            html_content = driver.page_source
            
            self.logger.info(f"Page loaded: {page_title}")
            self.logger.increment_pages()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Store metadata
            self.page_metadata = {
                'url': url,
                'title': page_title,
                'domain': urlparse(url).netloc
            }
            
            # AI-powered analysis
            if self.ai_analyzer.is_available():
                self.logger.info("Performing AI analysis of page structure...")
                analysis = self.ai_analyzer.analyze_page_structure(html_content, url)
                
                if analysis:
                    self.logger.info(f"Identified content type: {analysis.get('content_type', 'Unknown')}")
                    self.logger.debug(f"Recommended columns: {analysis.get('recommended_columns', [])}")
                    
                    # AI-powered extraction
                    self.logger.info("Extracting data using AI...")
                    extracted = self.ai_analyzer.extract_structured_data(
                        html_content, 
                        schema_hint=analysis.get('recommended_columns')
                    )
                    
                    if extracted and 'data' in extracted:
                        self.scraped_data = extracted['data']
                        self.logger.info(f"AI extracted {len(self.scraped_data)} items")
                        self.logger.increment_items(len(self.scraped_data))
                    
                    # Store metadata from AI
                    if extracted and 'metadata' in extracted:
                        self.page_metadata.update(extracted['metadata'])
            
            # Fallback: Traditional scraping if AI fails or is unavailable
            if not self.scraped_data:
                self.logger.info("Using traditional scraping methods...")
                self.scraped_data = self._fallback_scrape(soup, url)
                self.logger.increment_items(len(self.scraped_data))
            
            self.logger.info(f"Scraping completed. Total items: {len(self.scraped_data)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Scraping failed: {str(e)}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False
        finally:
            if driver:
                driver.quit()
    
    def _fallback_scrape(self, soup, url):
        """Traditional scraping fallback when AI is not available"""
        data = []
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract text content
        text_content = soup.get_text(separator='\n', strip=True)
        
        # Find all links
        links = []
        for link in soup.find_all('a', href=True):
            href = urljoin(url, link['href'])
            link_text = link.get_text(strip=True)
            if link_text and validators.url(href):
                links.append({'text': link_text, 'url': href})
        
        # Find all images
        images = []
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            alt_text = img.get('alt', '')
            images.append({'url': img_url, 'alt': alt_text})
        
        # Find all headings
        headings = []
        for i in range(1, 7):
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text(strip=True)
                })
        
        # Find all tables
        tables = []
        for table in soup.find_all('table'):
            table_data = []
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            
            for row in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]
                if cells:
                    table_data.append(cells)
            
            if table_data:
                tables.append({'headers': headers, 'rows': table_data})
        
        # Find all lists
        lists = []
        for ul in soup.find_all(['ul', 'ol']):
            items = [li.get_text(strip=True) for li in ul.find_all('li', recursive=False)]
            if items:
                lists.append({'type': ul.name, 'items': items})
        
        # Extract meta tags
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property', '')
            content = meta.get('content', '')
            if name and content:
                meta_tags[name] = content
        
        # Compile all data
        self.logger.debug(f"Found: {len(links)} links, {len(images)} images, {len(headings)} headings, {len(tables)} tables")
        
        # Create structured output
        if tables:
            # If tables found, prioritize table data
            for idx, table in enumerate(tables):
                for row_idx, row in enumerate(table['rows']):
                    item = {'table_index': idx, 'row_index': row_idx}
                    if table['headers']:
                        for col_idx, cell in enumerate(row):
                            header = table['headers'][col_idx] if col_idx < len(table['headers']) else f'column_{col_idx}'
                            item[header] = cell
                    else:
                        for col_idx, cell in enumerate(row):
                            item[f'column_{col_idx}'] = cell
                    data.append(item)
        else:
            # Create a comprehensive data structure
            main_data = {
                'url': url,
                'title': self.page_metadata.get('title', ''),
                'main_content': text_content[:1000] if text_content else '',
                'num_links': len(links),
                'num_images': len(images),
                'num_headings': len(headings),
                'meta_description': meta_tags.get('description', ''),
                'meta_keywords': meta_tags.get('keywords', '')
            }
            
            # Add top headings
            for idx, heading in enumerate(headings[:5]):
                main_data[f'heading_{idx+1}'] = heading['text']
            
            # Add top links
            for idx, link in enumerate(links[:10]):
                main_data[f'link_{idx+1}_text'] = link['text']
                main_data[f'link_{idx+1}_url'] = link['url']
            
            data.append(main_data)
        
        return data
    
    def save_to_csv(self, filename=None):
        """Save scraped data to CSV"""
        if not self.scraped_data:
            self.logger.warning("No data to save")
            return None
        
        if filename is None:
            domain = self.page_metadata.get('domain', 'scraped')
            clean_domain = re.sub(r'[^\w\-_]', '_', domain)
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{clean_domain}_{timestamp}.csv"
        
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        try:
            df = pd.DataFrame(self.scraped_data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            self.logger.info(f"Data saved to: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save CSV: {str(e)}")
            return None
    
    def get_data(self):
        """Return scraped data"""
        return self.scraped_data
    
    def get_metadata(self):
        """Return page metadata"""
        return self.page_metadata

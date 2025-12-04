"""
Adaptive Smart Scraper with AI Structure Analysis
Automatically analyzes and adapts to any website structure
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
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
import json

class AdaptiveSmartScraper:
    """
    Intelligent scraper that analyzes website structure and adapts extraction strategy
    """
    def __init__(self, logger):
        self.logger = logger
        self.ai_analyzer = AIContentAnalyzer(logger)
        self.scraped_data = []
        self.page_metadata = {}
        self.website_structure = {}
        self.extraction_strategy = None
        
    def analyze_structure(self, soup, url):
        """
        Deeply analyze website structure to determine optimal extraction strategy
        """
        self.logger.info("🔍 Analyzing website structure...")
        
        structure = {
            'url': url,
            'soup': soup,  # Add soup for universal domain detection
            'domain': urlparse(url).netloc,
            'has_tables': len(soup.find_all('table')) > 0,
            'table_count': len(soup.find_all('table')),
            'has_lists': len(soup.find_all(['ul', 'ol'])) > 0,
            'list_count': len(soup.find_all(['ul', 'ol'])),
            'has_articles': len(soup.find_all('article')) > 0,
            'article_count': len(soup.find_all('article')),
            'has_cards': len(soup.find_all(class_=re.compile('card|item|product'))) > 0,
            'card_count': len(soup.find_all(class_=re.compile('card|item|product'))),
            'heading_count': sum(len(soup.find_all(f'h{i}')) for i in range(1, 7)),
            'link_count': len(soup.find_all('a', href=True)),
            'image_count': len(soup.find_all('img')),
            'form_count': len(soup.find_all('form')),
            'video_count': len(soup.find_all('video')),
        }
        
        # Detect common patterns
        structure['patterns'] = []
        
        if structure['has_tables'] and structure['table_count'] > 0:
            structure['patterns'].append('tabular_data')
            
        if structure['has_articles'] and structure['article_count'] > 1:
            structure['patterns'].append('blog_listing')
            
        if structure['has_cards'] and structure['card_count'] > 3:
            structure['patterns'].append('product_listing')
            
        if structure['heading_count'] > 5 and structure['has_lists']:
            structure['patterns'].append('documentation')
            
        # Check for e-commerce indicators
        price_indicators = soup.find_all(class_=re.compile('price|cost|amount', re.I))
        if len(price_indicators) > 0:
            structure['patterns'].append('ecommerce')
            structure['has_prices'] = True
        
        # Check for news/article indicators
        date_indicators = soup.find_all(class_=re.compile('date|time|published', re.I))
        if len(date_indicators) > 0:
            structure['patterns'].append('news_article')
            structure['has_dates'] = True
        
        self.website_structure = structure
        
        # Log findings
        self.logger.info(f"   Domain: {structure['domain']}")
        self.logger.info(f"   Detected patterns: {', '.join(structure['patterns']) if structure['patterns'] else 'general_webpage'}")
        self.logger.info(f"   Tables: {structure['table_count']}, Lists: {structure['list_count']}, Articles: {structure['article_count']}")
        
        return structure
    
    def determine_strategy(self, structure):
        """
        Universal strategy determination using 100+ domain patterns
        Supports sports, e-commerce, news, social media, education, and more
        """
        self.logger.info("🎯 Determining extraction strategy...")
        
        # Import universal domain detection
        from domain_patterns import detect_domain_type
        
        # Get URL and soup from structure
        url = structure.get('url', '')
        soup = structure.get('soup')  # Will add this to structure
        
        # Detect domain type with confidence score
        domain_type, confidence, pattern_name = detect_domain_type(url, soup)
        
        self.logger.info(f"   🎯 Detected: {domain_type} (confidence: {confidence}%, pattern: {pattern_name})")
        
        strategy = {
            'type': domain_type,
            'confidence': confidence,
            'pattern_name': pattern_name,
            'priority_elements': [],
            'extraction_methods': []
        }
        
        # Map domain types to extraction strategies
        strategy_map = {
            # Sports
            'sports_matches': {
                'priority_elements': ['div[class*="match"]', 'div.liItem', 'li[class*="match"]'],
                'methods': ['extract_sports_matches', 'parse_match_data']
            },
            'sports_news': {
                'priority_elements': ['article', 'div[class*="post"]', 'div[class*="story"]'],
                'methods': ['extract_articles', 'extract_sports_news']
            },
            
            # E-commerce
            'ecommerce_products': {
                'priority_elements': ['div[class*="product"]', 'div[class*="item"]', 'div[data-component-type="s-search-result"]'],
                'methods': ['extract_products', 'find_prices', 'extract_images']
            },
            'fashion_products': {
                'priority_elements': ['div[class*="product"]', 'article[class*="product"]'],
                'methods': ['extract_fashion_products', 'extract_sizes', 'extract_colors']
            },
            
            # News & Media
            'news_articles': {
                'priority_elements': ['article', 'div[class*="article"]', 'div[class*="story"]'],
                'methods': ['extract_articles', 'find_dates', 'extract_authors']
            },
            'tech_news': {
                'priority_elements': ['article', 'div[class*="post"]', 'div[class*="entry"]'],
                'methods': ['extract_tech_articles', 'extract_code_snippets']
            },
            
            # Social Media
            'social_media': {
                'priority_elements': ['div[class*="post"]', 'div[class*="tweet"]', 'div[class*="feed"]'],
                'methods': ['extract_posts', 'extract_comments', 'extract_media']
            },
            
            # Entertainment
            'streaming_content': {
                'priority_elements': ['div[class*="title"]', 'div[class*="card"]', 'a[class*="title"]'],
                'methods': ['extract_titles', 'extract_metadata']
            },
            'movie_reviews': {
                'priority_elements': ['div[class*="review"]', 'div[class*="rating"]'],
                'methods': ['extract_reviews', 'extract_ratings', 'extract_cast']
            },
            
            # Education
            'educational_courses': {
                'priority_elements': ['div[class*="course"]', 'div[class*="class"]'],
                'methods': ['extract_courses', 'extract_instructors', 'extract_duration']
            },
            'academic_papers': {
                'priority_elements': ['div[class*="paper"]', 'div[class*="result"]'],
                'methods': ['extract_papers', 'extract_citations', 'extract_authors']
            },
            
            # Jobs
            'job_listings': {
                'priority_elements': ['div[class*="job"]', 'li[class*="job"]', 'div[class*="position"]'],
                'methods': ['extract_jobs', 'extract_salary', 'extract_requirements']
            },
            
            # Real Estate
            'real_estate_listings': {
                'priority_elements': ['div[class*="property"]', 'li[class*="listing"]'],
                'methods': ['extract_properties', 'extract_price', 'extract_details']
            },
            
            # Travel
            'travel_listings': {
                'priority_elements': ['div[class*="hotel"]', 'div[class*="flight"]'],
                'methods': ['extract_hotels', 'extract_flights', 'extract_prices']
            },
            
            # Food
            'recipe_content': {
                'priority_elements': ['div[class*="recipe"]', 'div[class*="ingredient"]'],
                'methods': ['extract_recipes', 'extract_ingredients', 'extract_instructions']
            },
            'restaurant_menus': {
                'priority_elements': ['div[class*="menu"]', 'div[class*="dish"]'],
                'methods': ['extract_menu_items', 'extract_prices']
            },
            
            # Finance
            'financial_data': {
                'priority_elements': ['table', 'div[class*="quote"]', 'div[class*="stock"]'],
                'methods': ['extract_stocks', 'extract_prices', 'extract_tables']
            },
            'crypto_prices': {
                'priority_elements': ['div[class*="coin"]', 'table[class*="price"]'],
                'methods': ['extract_crypto', 'extract_prices', 'extract_market_cap']
            },
            
            # Health
            'medical_info': {
                'priority_elements': ['article', 'div[class*="content"]'],
                'methods': ['extract_medical_content', 'extract_symptoms']
            },
            'fitness_tracking': {
                'priority_elements': ['div[class*="workout"]', 'div[class*="exercise"]'],
                'methods': ['extract_workouts', 'extract_exercises']
            },
            
            # Technology
            'developer_content': {
                'priority_elements': ['div[class*="repo"]', 'pre', 'code'],
                'methods': ['extract_code', 'extract_repos', 'extract_documentation']
            },
            'documentation': {
                'priority_elements': ['article', 'div[class*="doc"]', 'div[class*="api"]'],
                'methods': ['extract_docs', 'extract_code_examples']
            },
            
            # Forums
            'forum_threads': {
                'priority_elements': ['div[class*="thread"]', 'div[class*="post"]'],
                'methods': ['extract_threads', 'extract_posts', 'extract_replies']
            },
            
            # Weather
            'weather_data': {
                'priority_elements': ['div[class*="weather"]', 'div[class*="forecast"]'],
                'methods': ['extract_weather', 'extract_forecast', 'extract_temperature']
            },
            
            # Government
            'government_data': {
                'priority_elements': ['table', 'div[class*="document"]'],
                'methods': ['extract_tables', 'extract_documents']
            },
            
            # Automotive
            'vehicle_listings': {
                'priority_elements': ['div[class*="vehicle"]', 'div[class*="car"]'],
                'methods': ['extract_vehicles', 'extract_specs', 'extract_price']
            },
            
            # Gaming
            'gaming_content': {
                'priority_elements': ['div[class*="game"]', 'div[class*="review"]'],
                'methods': ['extract_games', 'extract_reviews', 'extract_scores']
            },
            
            # Business
            'business_data': {
                'priority_elements': ['div[class*="company"]', 'div[class*="profile"]'],
                'methods': ['extract_companies', 'extract_metrics']
            },
            
            # HTML Structure types
            'tabular_data': {
                'priority_elements': ['table', 'tr', 'td', 'th'],
                'methods': ['parse_tables', 'extract_table_data']
            },
            'list_content': {
                'priority_elements': ['ul', 'ol', 'li'],
                'methods': ['extract_lists', 'parse_list_items']
            },
            'image_gallery': {
                'priority_elements': ['img', 'div[class*="gallery"]'],
                'methods': ['extract_images', 'extract_captions']
            },
            'video_content': {
                'priority_elements': ['video', 'iframe'],
                'methods': ['extract_videos', 'extract_metadata']
            },
            
            # Fallback
            'general_content': {
                'priority_elements': ['article', 'div', 'section', 'main'],
                'methods': ['extract_all_content']
            }
        }
        
        # Apply strategy configuration
        if domain_type in strategy_map:
            strategy['priority_elements'] = strategy_map[domain_type]['priority_elements']
            strategy['extraction_methods'] = strategy_map[domain_type]['methods']
        else:
            # Fallback to general
            strategy['priority_elements'] = strategy_map['general_content']['priority_elements']
            strategy['extraction_methods'] = strategy_map['general_content']['methods']
        
        self.extraction_strategy = strategy
        self.logger.info(f"   Strategy: {strategy['type']}")
        self.logger.info(f"   Methods: {', '.join(strategy['extraction_methods'])}")
        
        return strategy
    
    def adaptive_extract(self, soup, url, strategy):
        """
        Extract data using the determined strategy
        """
        self.logger.info("📊 Extracting data with adaptive strategy...")
        
        data = []
        
        if strategy['type'] == 'sports_matches':
            data = self._extract_sports_matches(soup, url)
        
        elif strategy['type'] == 'table_focused':
            data = self._extract_table_focused(soup, url)
            
        elif strategy['type'] == 'product_listing':
            data = self._extract_product_listing(soup, url)
            
        elif strategy['type'] == 'article_content':
            data = self._extract_article_content(soup, url)
            
        elif strategy['type'] == 'list_based':
            data = self._extract_list_based(soup, url)
            
        else:
            data = self._extract_general_content(soup, url)
        
        self.logger.info(f"   Extracted {len(data)} items using {strategy['type']} strategy")
        
        return data
    
    def _extract_table_focused(self, soup, url):
        """Extract data from table-heavy pages"""
        data = []
        tables = soup.find_all('table')
        
        for table_idx, table in enumerate(tables):
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            
            for row in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in row.find_all('td')]
                if cells:
                    item = {'table_index': table_idx, 'source_url': url}
                    if headers and len(headers) == len(cells):
                        for header, cell in zip(headers, cells):
                            item[header] = cell
                    else:
                        for idx, cell in enumerate(cells):
                            item[f'column_{idx}'] = cell
                    data.append(item)
        
        return data if data else self._extract_general_content(soup, url)
    
    def _extract_product_listing(self, soup, url):
        """Extract e-commerce/product data"""
        data = []
        
        # Find product containers
        products = soup.find_all(class_=re.compile('product|item|card', re.I))
        
        for idx, product in enumerate(products[:50]):  # Limit to 50 products
            item = {'product_index': idx, 'source_url': url}
            
            # Extract title
            title = product.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile('title|name|heading', re.I))
            if title:
                item['title'] = title.get_text(strip=True)
            
            # Extract price
            price = product.find(class_=re.compile('price|cost|amount', re.I))
            if price:
                item['price'] = price.get_text(strip=True)
            
            # Extract description
            desc = product.find(class_=re.compile('description|summary|excerpt', re.I))
            if desc:
                item['description'] = desc.get_text(strip=True)[:200]
            
            # Extract image
            img = product.find('img')
            if img and img.get('src'):
                item['image_url'] = urljoin(url, img.get('src'))
            
            # Extract link
            link = product.find('a', href=True)
            if link:
                item['product_url'] = urljoin(url, link['href'])
            
            if len(item) > 2:  # Has more than just index and source
                data.append(item)
        
        return data if data else self._extract_general_content(soup, url)
    
    def _extract_article_content(self, soup, url):
        """Extract blog/news article data"""
        data = []
        
        articles = soup.find_all('article')
        if not articles:
            articles = soup.find_all(class_=re.compile('post|entry|article', re.I))
        
        for idx, article in enumerate(articles[:30]):  # Limit to 30 articles
            item = {'article_index': idx, 'source_url': url}
            
            # Extract title
            title = article.find(['h1', 'h2', 'h3'])
            if title:
                item['title'] = title.get_text(strip=True)
            
            # Extract date
            date_elem = article.find(class_=re.compile('date|time|published', re.I))
            if date_elem:
                item['date'] = date_elem.get_text(strip=True)
            
            # Extract author
            author = article.find(class_=re.compile('author|by|writer', re.I))
            if author:
                item['author'] = author.get_text(strip=True)
            
            # Extract content preview
            content = article.find(['p', 'div'], class_=re.compile('content|excerpt|summary', re.I))
            if content:
                item['content_preview'] = content.get_text(strip=True)[:300]
            
            # Extract link
            link = article.find('a', href=True)
            if link:
                item['article_url'] = urljoin(url, link['href'])
            
            if len(item) > 2:
                data.append(item)
        
        return data if data else self._extract_general_content(soup, url)
    
    def _extract_list_based(self, soup, url):
        """Extract list-based data"""
        data = []
        
        lists = soup.find_all(['ul', 'ol'])
        
        for list_idx, ul in enumerate(lists):
            items = ul.find_all('li', recursive=False)
            for item_idx, li in enumerate(items):
                item = {
                    'list_index': list_idx,
                    'item_index': item_idx,
                    'text': li.get_text(strip=True),
                    'source_url': url
                }
                
                # Extract link if present
                link = li.find('a', href=True)
                if link:
                    item['link_url'] = urljoin(url, link['href'])
                    item['link_text'] = link.get_text(strip=True)
                
                data.append(item)
        
        return data if data else self._extract_general_content(soup, url)
    
    def _extract_sports_matches(self, soup, url):
        """Extract sports match data (supports Arabic and English sports sites)"""
        self.logger.info("⚽ Extracting sports match data...")
        data = []
        
        # Remove navigation calendars and unwanted elements  
        for elem in soup.find_all(class_=re.compile('calendar|date-nav', re.I)):
            if elem.find_parent('nav') or len(elem.find_all('a')) > 5:
                elem.decompose()
        
        # Find match containers with multiple patterns
        match_containers = []
        
        # Pattern 1: div.liItem (yallakora.com style)
        match_containers.extend(soup.find_all('div', class_='liItem'))
        
        # Pattern 2: div/li with class containing "match-item", "fixture", etc
        if not match_containers:
            match_containers.extend(soup.find_all(['div', 'li'], class_=re.compile(r'match-item|matchItem|fixture', re.I)))
        
        # Pattern 3: Links to match details
        if not match_containers:
            match_containers.extend(soup.find_all('a', href=re.compile(r'/match/\d+/', re.I)))
        
        self.logger.info(f"   Found {len(match_containers)} potential match containers")
        
        seen_matches = set()  # Prevent duplicates
        match_count = 0
        
        for idx, container in enumerate(match_containers[:50]):  # Limit to 50 matches
            try:
                item = {'match_index': match_count, 'source_url': url}
                
                # Extract match time
                time_elem = container.find('span', class_='time') or \
                           container.find(class_=re.compile('time|hour|clock', re.I))
                if time_elem:
                    time_text = time_elem.get_text(strip=True)
                    if time_text and len(time_text) < 20 and ':' in time_text:
                        item['match_time'] = time_text
                
                # Extract team names - specific selectors for yallakora.com
                team_a = container.find('div', class_='teamA')
                team_b = container.find('div', class_='teamB')
                
                if team_a and team_b:
                    # Yallakora.com structure
                    team_a_name = team_a.find('p')
                    team_b_name = team_b.find('p')
                    
                    if team_a_name:
                        home_team = team_a_name.get_text(strip=True)
                        if home_team and len(home_team) < 100:
                            item['home_team'] = home_team
                    
                    if team_b_name:
                        away_team = team_b_name.get_text(strip=True)
                        if away_team and len(away_team) < 100:
                            item['away_team'] = away_team
                else:
                    # Generic team extraction
                    team_elems = container.find_all(class_=re.compile('team', re.I))
                    teams = []
                    for team in team_elems[:2]:
                        # Try to find team name in <p>, <span>, or direct text
                        team_name_elem = team.find(['p', 'span', 'h3'])
                        if team_name_elem:
                            team_name = team_name_elem.get_text(strip=True)
                        else:
                            team_name = team.get_text(strip=True)
                        
                        if team_name and len(team_name) < 100:
                            # Clean up team name (remove scores, times, etc.)
                            team_name = re.sub(r'---?\d+:\d+', '', team_name).strip()
                            team_name = re.sub(r'\d+\s*-\s*\d+', '', team_name).strip()
                            if team_name and team_name not in teams:
                                teams.append(team_name)
                    
                    if len(teams) >= 2:
                        item['home_team'] = teams[0]
                        item['away_team'] = teams[1]
                    elif len(teams) == 1:
                        item['team'] = teams[0]
                
                # Extract match status
                status_elem = container.find('div', class_='matchStatus')
                if status_elem:
                    status_span = status_elem.find('span')
                    if status_span:
                        status_text = status_span.get_text(strip=True)
                        if status_text and len(status_text) < 50:
                            item['status'] = status_text
                
                # Extract score
                score_elems = container.find_all('span', class_='score')
                if len(score_elems) >= 2:
                    score_a = score_elems[0].get_text(strip=True)
                    score_b = score_elems[1].get_text(strip=True)
                    if score_a != '-' and score_b != '-':
                        item['score'] = f"{score_a} - {score_b}"
                
                # Extract round/stage info
                date_elem = container.find('div', class_='date')
                if date_elem:
                    round_text = date_elem.get_text(strip=True)
                    if round_text and len(round_text) < 100:
                        item['round'] = round_text
                
                # Extract channel
                channel_elem = container.find('div', class_='channel')
                if channel_elem:
                    channel_text = channel_elem.get_text(strip=True)
                    if channel_text and len(channel_text) < 100:
                        item['channel'] = channel_text
                
                # Extract match URL
                link = container.find('a', href=True) if container.name != 'a' else container
                if link and link.get('href'):
                    match_url = urljoin(url, link['href'])
                    if '/match/' in match_url:
                        item['match_url'] = match_url
                
                # Extract competition from parent matchCard
                parent_card = container.find_parent(class_=lambda x: x and 'matchCard' in ' '.join(x) if isinstance(x, list) else 'matchCard' in x if x else False)
                if parent_card:
                    tour_title = parent_card.find('h2')
                    if tour_title:
                        comp_name = tour_title.get_text(strip=True)
                        if comp_name and len(comp_name) < 100:
                            item['competition'] = comp_name
                
                # Create unique identifier
                match_id = f"{item.get('home_team', '')}_{item.get('away_team', '')}_{item.get('match_time', '')}"
                
                # Only add if has teams and not duplicate
                if (match_id not in seen_matches and 
                    ('home_team' in item and 'away_team' in item) or 'team' in item):
                    data.append(item)
                    seen_matches.add(match_id)
                    match_count += 1
                    
            except Exception as e:
                self.logger.debug(f"Error extracting match {idx}: {str(e)}")
                continue
        
        self.logger.info(f"   ✅ Extracted {len(data)} unique matches")
        
        return data if data else self._extract_general_content(soup, url)
    
    def _extract_general_content(self, soup, url):
        """General extraction fallback"""
        # Remove unwanted elements
        for elem in soup(['script', 'style', 'nav', 'footer', 'header']):
            elem.decompose()
        
        data = [{
            'url': url,
            'title': soup.title.string if soup.title else '',
            'main_content': soup.get_text(separator='\n', strip=True)[:2000],
            'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])[:10]],
            'links': [{'text': a.get_text(strip=True), 'url': urljoin(url, a['href'])} 
                     for a in soup.find_all('a', href=True)[:20]],
            'images': [urljoin(url, img['src']) for img in soup.find_all('img', src=True)[:10]]
        }]
        
        return data
    
    def _check_auth_required(self, html_content, url):
        """Check if page requires authentication"""
        html_lower = html_content.lower()
        domain = urlparse(url).netloc.lower()
        
        # Check for common authentication indicators
        auth_indicators = [
            'login required',
            'sign in to continue',
            'authentication required',
            'please log in',
            'must be logged in',
            'login to view',
            'signin-wrapper',
            'login-form',
            'auth-required'
        ]
        
        # Check for social media login walls
        social_auth_sites = ['twitter.com', 'x.com', 'facebook.com', 'instagram.com', 'linkedin.com']
        if any(site in domain for site in social_auth_sites):
            if 'login' in html_lower or 'sign in' in html_lower or 'log in' in html_lower:
                return True
        
        # Check HTML content
        if any(indicator in html_lower for indicator in auth_indicators):
            return True
        
        # Check if content is very minimal (often blocked pages)
        if len(html_content.strip()) < 500:
            return True
            
        return False
    
    def scrape_url(self, url):
        """Main scraping method with adaptive intelligence"""
        self.logger.info(f"🚀 Starting adaptive smart scrape of: {url}")
        
        if not validators.url(url):
            self.logger.error(f"Invalid URL: {url}")
            return False
        
        driver = None
        try:
            # Setup Firefox
            firefox_options = Options()
            firefox_options.add_argument('--headless')
            firefox_options.set_preference('general.useragent.override', Config.USER_AGENT)
            
            self.logger.debug("Launching Firefox browser...")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            driver.set_page_load_timeout(Config.REQUEST_TIMEOUT)
            
            # Navigate with timeout handling
            self.logger.info(f"📡 Loading page: {url}")
            
            try:
                driver.get(url)
            except Exception as nav_error:
                # Check if page partially loaded
                if "timeout" in str(nav_error).lower():
                    self.logger.warning(f"⚠️ Page load timeout, but continuing with partial content...")
                else:
                    raise
            
            time.sleep(Config.WAIT_FOR_LOAD / 1000)
            
            page_title = driver.title
            html_content = driver.page_source
            
            # Check for authentication/login walls
            if self._check_auth_required(html_content, url):
                self.logger.error("🔒 This site requires authentication/login. Cannot scrape protected content.")
                self.logger.error(f"   Detected: Login page or authentication wall")
                return False
            
            self.logger.info(f"✅ Page loaded: {page_title}")
            self.logger.increment_pages()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Store metadata
            self.page_metadata = {
                'url': url,
                'title': page_title,
                'domain': urlparse(url).netloc
            }
            
            # STEP 1: Analyze Structure
            structure = self.analyze_structure(soup, url)
            
            # STEP 2: Determine Strategy
            strategy = self.determine_strategy(structure)
            
            # STEP 3: Try AI-Enhanced Extraction First
            if self.ai_analyzer.is_available():
                self.logger.info("🤖 Using AI-enhanced extraction...")
                analysis = self.ai_analyzer.analyze_page_structure(html_content, url)
                
                if analysis:
                    self.logger.info(f"   AI detected: {analysis.get('content_type', 'Unknown')}")
                    extracted = self.ai_analyzer.extract_structured_data(html_content, analysis.get('recommended_columns'))
                    
                    if extracted and 'data' in extracted and extracted['data']:
                        self.scraped_data = extracted['data']
                        self.logger.info(f"   AI extracted {len(self.scraped_data)} items")
                        self.logger.increment_items(len(self.scraped_data))
                        
                        if 'metadata' in extracted:
                            self.page_metadata.update(extracted['metadata'])
            
            # STEP 4: Use Adaptive Strategy if AI didn't extract enough
            if not self.scraped_data or len(self.scraped_data) == 0:
                self.scraped_data = self.adaptive_extract(soup, url, strategy)
                self.logger.increment_items(len(self.scraped_data))
            
            self.logger.info(f"✅ Scraping completed. Total items: {len(self.scraped_data)}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Scraping failed: {str(e)}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False
        finally:
            if driver:
                driver.quit()
    
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
            self.logger.info(f"💾 Data saved to: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to save CSV: {str(e)}")
            return None
    
    def get_data(self):
        return self.scraped_data
    
    def get_metadata(self):
        return self.page_metadata
    
    def get_structure_analysis(self):
        """Return the website structure analysis"""
        return {
            'structure': self.website_structure,
            'strategy': self.extraction_strategy
        }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python adaptive_scraper.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Initialize logger and scraper
    from logger import ScraperLogger
    logger = ScraperLogger('adaptive_cli')
    scraper = AdaptiveSmartScraper(logger)
    
    # Scrape the URL
    print(f"\n🔗 Scraping: {url}\n")
    success = scraper.scrape_url(url)
    
    if not success:
        print(f"\n❌ Scraping failed!")
        sys.exit(1)
    
    # Save to CSV
    csv_path = scraper.save_to_csv()
    data = scraper.get_data()
    strategy = scraper.extraction_strategy
    
    result = {
        'success': success,
        'data': data,
        'csv_path': csv_path,
        'strategy': strategy.get('type', 'unknown') if strategy else 'unknown'
    }
    
    # Display results
    print(f"\n✅ Scraping completed successfully!")
    print(f"   📊 Extracted {len(result['data'])} items")
    print(f"   📁 Saved to: {result['csv_path']}")
    print(f"   🧠 Strategy used: {result['strategy']}\n")

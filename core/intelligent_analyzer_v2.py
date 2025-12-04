"""
Enhanced Intelligent HTML Analyzer V2.0
Advanced webpage analysis with multiple scenarios and pattern recognition
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
from collections import Counter, defaultdict
import json
import re
from datetime import datetime
import time
from core.professional_logger import get_logger


class IntelligentAnalyzerV2:
    """Advanced HTML analyzer with comprehensive pattern detection"""
    
    # Supported website patterns
    PATTERNS = {
        'e-commerce': ['product', 'price', 'cart', 'shop', 'buy'],
        'blog': ['article', 'post', 'author', 'comment', 'blog'],
        'news': ['news', 'headline', 'story', 'breaking'],
        'social': ['profile', 'tweet', 'post', 'share', 'like'],
        'directory': ['listing', 'directory', 'catalog', 'index'],
        'forum': ['thread', 'reply', 'forum', 'topic', 'discussion'],
        'documentation': ['doc', 'api', 'reference', 'guide'],
        'job_board': ['job', 'career', 'position', 'hiring'],
        'real_estate': ['property', 'listing', 'estate', 'rent', 'sale'],
        'event': ['event', 'calendar', 'schedule', 'conference']
    }
    
    def __init__(self, url, timeout=30, logger=None):
        """
        Initialize analyzer
        
        Args:
            url: Target URL to analyze
            timeout: Request timeout in seconds
            logger: Logger instance
        """
        self.url = url
        self.timeout = timeout
        self.logger = logger or get_logger()
        
        self.domain = urlparse(url).netloc
        self.soup = None
        self.response = None
        
        self.analysis = {
            'metadata': {
                'url': url,
                'domain': self.domain,
                'analyzed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'analyzer_version': '2.0'
            },
            'structure': {},
            'content_patterns': {},
            'semantic_analysis': {},
            'data_structures': {},
            'scraping_strategy': {},
            'technical_details': {}
        }
        
        self.logger.info(f"Initialized analyzer for {url}")
    
    def fetch_page(self):
        """Fetch webpage with advanced error handling"""
        self.logger.log_step(1, "Fetching webpage", "START")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        try:
            start_time = time.time()
            self.response = requests.get(
                self.url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            duration = time.time() - start_time
            
            self.response.raise_for_status()
            
            # Parse with lxml for better performance
            self.soup = BeautifulSoup(self.response.text, 'lxml')
            
            # Log fetch details
            self.logger.log_url_fetch(
                self.url,
                self.response.status_code,
                duration,
                len(self.response.content)
            )
            
            # Store technical details
            self.analysis['technical_details']['status_code'] = self.response.status_code
            self.analysis['technical_details']['content_length'] = len(self.response.content)
            self.analysis['technical_details']['content_type'] = self.response.headers.get('Content-Type', '')
            self.analysis['technical_details']['server'] = self.response.headers.get('Server', 'Unknown')
            self.analysis['technical_details']['load_time_ms'] = round(duration * 1000, 2)
            
            # Check for redirects
            if self.response.history:
                self.analysis['technical_details']['redirects'] = len(self.response.history)
                self.analysis['technical_details']['final_url'] = self.response.url
                self.logger.warning(f"URL redirected {len(self.response.history)} times")
            
            self.logger.log_step(1, "Fetching webpage", "SUCCESS")
            return True
            
        except requests.Timeout:
            self.logger.error(f"Timeout while fetching {self.url}")
            return False
        except requests.ConnectionError as e:
            self.logger.error(f"Connection error: {str(e)}")
            return False
        except requests.HTTPError as e:
            self.logger.error(f"HTTP error {e.response.status_code}: {str(e)}")
            return False
        except Exception as e:
            self.logger.exception(f"Unexpected error fetching page: {str(e)}")
            return False
    
    def analyze_structure(self):
        """Comprehensive HTML structure analysis"""
        self.logger.log_step(2, "Analyzing HTML structure", "START")
        
        # Basic element counting
        all_tags = [tag.name for tag in self.soup.find_all()]
        tag_counts = Counter(all_tags)
        
        self.analysis['structure']['total_elements'] = len(all_tags)
        self.analysis['structure']['unique_tags'] = len(tag_counts)
        self.analysis['structure']['tag_distribution'] = dict(tag_counts.most_common(30))
        
        # Depth analysis
        max_depth = self._calculate_dom_depth()
        self.analysis['structure']['max_dom_depth'] = max_depth
        
        # Identify main content
        main_content = self._identify_main_content()
        if main_content:
            self.analysis['structure']['main_content'] = {
                'tag': main_content.name,
                'classes': main_content.get('class', []),
                'id': main_content.get('id', ''),
                'child_count': len(list(main_content.children))
            }
        
        # Analyze semantic HTML5 usage
        self._analyze_semantic_html()
        
        # Analyze headings hierarchy
        self._analyze_headings()
        
        # Analyze forms
        self._analyze_forms()
        
        # Analyze tables
        self._analyze_tables()
        
        self.logger.log_metric("Total Elements", len(all_tags))
        self.logger.log_metric("DOM Depth", max_depth, "levels")
        self.logger.log_step(2, "Analyzing HTML structure", "SUCCESS")
    
    def _calculate_dom_depth(self):
        """Calculate maximum DOM tree depth"""
        def get_depth(element, current_depth=0):
            if not element or not hasattr(element, 'children'):
                return current_depth
            
            max_child_depth = current_depth
            for child in element.children:
                if hasattr(child, 'name'):
                    child_depth = get_depth(child, current_depth + 1)
                    max_child_depth = max(max_child_depth, child_depth)
            
            return max_child_depth
        
        return get_depth(self.soup.body if self.soup.body else self.soup)
    
    def _analyze_semantic_html(self):
        """Analyze semantic HTML5 element usage"""
        semantic_tags = ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']
        semantic_usage = {}
        
        for tag in semantic_tags:
            elements = self.soup.find_all(tag)
            if elements:
                semantic_usage[tag] = len(elements)
        
        self.analysis['structure']['semantic_html5'] = semantic_usage
        self.analysis['structure']['uses_semantic_html'] = len(semantic_usage) > 0
    
    def _analyze_headings(self):
        """Analyze heading hierarchy and structure"""
        headings = []
        
        for level in range(1, 7):
            h_tags = self.soup.find_all(f'h{level}')
            for h_tag in h_tags:
                headings.append({
                    'level': level,
                    'text': h_tag.get_text(strip=True)[:100],
                    'classes': h_tag.get('class', [])
                })
        
        self.analysis['structure']['headings'] = {
            'total': len(headings),
            'by_level': Counter([h['level'] for h in headings]),
            'hierarchy': headings[:20]  # Top 20
        }
    
    def _analyze_forms(self):
        """Analyze forms on the page"""
        forms = self.soup.find_all('form')
        form_data = []
        
        for form in forms:
            inputs = form.find_all(['input', 'select', 'textarea'])
            form_data.append({
                'action': form.get('action', ''),
                'method': form.get('method', 'get').upper(),
                'field_count': len(inputs),
                'field_types': Counter([inp.get('type', 'text') for inp in form.find_all('input')])
            })
        
        self.analysis['structure']['forms'] = {
            'total': len(forms),
            'details': form_data
        }
    
    def _analyze_tables(self):
        """Analyze table structures"""
        tables = self.soup.find_all('table')
        table_data = []
        
        for table in tables:
            rows = table.find_all('tr')
            headers = table.find_all('th')
            
            table_data.append({
                'row_count': len(rows),
                'header_count': len(headers),
                'classes': table.get('class', []),
                'has_thead': bool(table.find('thead')),
                'has_tbody': bool(table.find('tbody'))
            })
        
        self.analysis['structure']['tables'] = {
            'total': len(tables),
            'details': table_data
        }
    
    def _identify_main_content(self):
        """Identify main content container with advanced heuristics"""
        candidates = []
        
        # Semantic tags (highest priority)
        for tag in ['main', 'article']:
            elements = self.soup.find_all(tag)
            for elem in elements:
                candidates.append(('semantic', elem, len(elem.get_text(strip=True))))
        
        # Common class patterns
        content_patterns = [
            r'content', r'main', r'body', r'article', r'post',
            r'entry', r'container', r'wrapper', r'page-content'
        ]
        
        for pattern in content_patterns:
            elements = self.soup.find_all(class_=re.compile(pattern, re.I))
            for elem in elements:
                text_length = len(elem.get_text(strip=True))
                if text_length > 500:  # Minimum content threshold
                    candidates.append(('class', elem, text_length))
        
        # Common ID patterns
        for pattern in content_patterns:
            elem = self.soup.find(id=re.compile(pattern, re.I))
            if elem:
                text_length = len(elem.get_text(strip=True))
                if text_length > 500:
                    candidates.append(('id', elem, text_length))
        
        # Return best candidate (prefer semantic, then longest content)
        if candidates:
            candidates.sort(key=lambda x: (x[0] == 'semantic', x[2]), reverse=True)
            return candidates[0][1]
        
        return None
    
    def analyze_content_patterns(self):
        """Identify repeating content patterns with advanced detection"""
        self.logger.log_step(3, "Analyzing content patterns", "START")
        
        # Find repeating class patterns
        class_patterns = self._find_class_patterns()
        self.analysis['content_patterns']['repeating_classes'] = class_patterns
        
        # Find list structures
        list_patterns = self._find_list_patterns_advanced()
        self.analysis['content_patterns']['list_patterns'] = list_patterns
        
        # Find card/tile patterns
        card_patterns = self._find_card_patterns()
        self.analysis['content_patterns']['card_patterns'] = card_patterns
        
        # Find table patterns
        table_patterns = self._find_table_patterns()
        self.analysis['content_patterns']['table_patterns'] = table_patterns
        
        # Find text content blocks
        text_blocks = self._find_text_blocks_advanced()
        self.analysis['content_patterns']['text_blocks'] = text_blocks
        
        self.logger.log_metric("List Patterns", len(list_patterns))
        self.logger.log_metric("Card Patterns", len(card_patterns))
        self.logger.log_step(3, "Analyzing content patterns", "SUCCESS")
    
    def _find_class_patterns(self):
        """Find repeating class name patterns"""
        class_counter = Counter()
        
        for elem in self.soup.find_all(class_=True):
            classes = elem.get('class', [])
            for cls in classes:
                class_counter[cls] += 1
        
        # Filter: appear 4+ times but not too common (not layout classes)
        repeating = {
            cls: count for cls, count in class_counter.items()
            if 4 <= count <= 1000
        }
        
        return dict(sorted(repeating.items(), key=lambda x: x[1], reverse=True)[:30])
    
    def _find_list_patterns_advanced(self):
        """Advanced list pattern detection"""
        patterns = []
        
        # Traditional lists
        for list_tag in self.soup.find_all(['ul', 'ol']):
            items = list_tag.find_all('li', recursive=False)
            if len(items) >= 3:
                sample = items[0]
                patterns.append({
                    'type': 'traditional_list',
                    'tag': list_tag.name,
                    'item_count': len(items),
                    'item_tag': 'li',
                    'item_classes': sample.get('class', []),
                    'has_links': bool(sample.find('a')),
                    'has_images': bool(sample.find('img')),
                    'avg_text_length': sum(len(item.get_text(strip=True)) for item in items) // len(items)
                })
        
        # Div-based lists (modern patterns)
        div_patterns = self._detect_div_lists()
        patterns.extend(div_patterns)
        
        # Grid/flex layouts
        grid_patterns = self._detect_grid_layouts()
        patterns.extend(grid_patterns)
        
        return patterns[:15]
    
    def _detect_div_lists(self):
        """Detect div-based repeating structures"""
        patterns = []
        class_groups = defaultdict(list)
        
        for div in self.soup.find_all('div', class_=True):
            class_sig = ' '.join(sorted(div.get('class', [])))
            if class_sig:
                class_groups[class_sig].append(div)
        
        for class_sig, divs in class_groups.items():
            if len(divs) >= 5:
                sample = divs[0]
                patterns.append({
                    'type': 'div_list',
                    'item_count': len(divs),
                    'item_classes': class_sig.split(),
                    'has_links': bool(sample.find('a')),
                    'has_images': bool(sample.find('img')),
                    'has_headings': bool(sample.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
                    'avg_text_length': sum(len(d.get_text(strip=True)) for d in divs) // len(divs)
                })
        
        return sorted(patterns, key=lambda x: x['item_count'], reverse=True)[:10]
    
    def _detect_grid_layouts(self):
        """Detect CSS grid or flexbox layouts"""
        patterns = []
        
        # Look for containers with display: grid or flex (via class names)
        grid_keywords = ['grid', 'flex', 'row', 'col', 'column']
        
        for container in self.soup.find_all(['div', 'section', 'ul']):
            classes = ' '.join(container.get('class', [])).lower()
            
            if any(keyword in classes for keyword in grid_keywords):
                children = container.find_all(recursive=False)
                
                if len(children) >= 4:
                    patterns.append({
                        'type': 'grid_layout',
                        'container_classes': container.get('class', []),
                        'item_count': len(children),
                        'child_tags': Counter([child.name for child in children])
                    })
        
        return patterns[:5]
    
    def _find_card_patterns(self):
        """Detect card/tile UI patterns"""
        card_patterns = []
        card_keywords = ['card', 'tile', 'box', 'item', 'panel']
        
        for keyword in card_keywords:
            elements = self.soup.find_all(class_=re.compile(keyword, re.I))
            
            if len(elements) >= 3:
                sample = elements[0]
                
                # Analyze card structure
                has_image = bool(sample.find('img'))
                has_heading = bool(sample.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
                has_link = bool(sample.find('a'))
                has_button = bool(sample.find('button'))
                
                card_patterns.append({
                    'keyword': keyword,
                    'count': len(elements),
                    'structure': {
                        'has_image': has_image,
                        'has_heading': has_heading,
                        'has_link': has_link,
                        'has_button': has_button
                    },
                    'classes': sample.get('class', [])
                })
        
        return sorted(card_patterns, key=lambda x: x['count'], reverse=True)[:5]
    
    def _find_table_patterns(self):
        """Analyze data table patterns"""
        patterns = []
        
        for table in self.soup.find_all('table'):
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            rows = table.find_all('tr')
            
            if len(rows) > 1:
                patterns.append({
                    'type': 'data_table',
                    'row_count': len(rows),
                    'column_count': len(headers) if headers else len(rows[0].find_all(['td', 'th'])),
                    'headers': headers[:10],
                    'has_headers': bool(headers),
                    'classes': table.get('class', [])
                })
        
        return patterns
    
    def _find_text_blocks_advanced(self):
        """Find significant text content with context"""
        blocks = []
        
        for tag in ['p', 'div', 'span', 'article', 'section']:
            elements = self.soup.find_all(tag)
            
            for elem in elements:
                text = elem.get_text(strip=True)
                
                if len(text) > 100:
                    # Analyze text characteristics
                    word_count = len(text.split())
                    has_links = bool(elem.find('a'))
                    has_emphasis = bool(elem.find(['strong', 'em', 'b', 'i']))
                    
                    blocks.append({
                        'tag': tag,
                        'classes': elem.get('class', []),
                        'id': elem.get('id', ''),
                        'text_length': len(text),
                        'word_count': word_count,
                        'has_links': has_links,
                        'has_emphasis': has_emphasis,
                        'preview': text[:200]
                    })
        
        blocks.sort(key=lambda x: x['text_length'], reverse=True)
        return blocks[:15]
    
    def analyze_links(self):
        """Comprehensive link analysis"""
        self.logger.log_step(4, "Analyzing links", "START")
        
        all_links = self.soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        anchor_links = []
        javascript_links = []
        
        for link in all_links:
            href = link.get('href', '')
            
            if href.startswith('#'):
                anchor_links.append(href)
            elif href.startswith('javascript:'):
                javascript_links.append(href)
            else:
                full_url = urljoin(self.url, href)
                
                if urlparse(full_url).netloc == self.domain:
                    internal_links.append(full_url)
                else:
                    external_links.append(full_url)
        
        self.analysis['structure']['links'] = {
            'total': len(all_links),
            'internal': len(internal_links),
            'external': len(external_links),
            'anchors': len(anchor_links),
            'javascript': len(javascript_links),
            'sample_internal': list(set(internal_links))[:15],
            'sample_external': list(set(external_links))[:10]
        }
        
        self.logger.log_metric("Total Links", len(all_links))
        self.logger.log_metric("Internal Links", len(internal_links))
        self.logger.log_step(4, "Analyzing links", "SUCCESS")
    
    def analyze_media(self):
        """Analyze images and media elements"""
        self.logger.info("Analyzing media elements")
        
        # Images
        images = self.soup.find_all('img')
        img_data = {
            'total': len(images),
            'with_alt': len([img for img in images if img.get('alt')]),
            'lazy_loaded': len([img for img in images if 'lazy' in img.get('loading', '').lower()]),
            'formats': Counter([img.get('src', '').split('.')[-1].lower() for img in images if img.get('src')])
        }
        
        # Videos
        videos = self.soup.find_all('video')
        iframes = self.soup.find_all('iframe', src=re.compile(r'youtube|vimeo', re.I))
        
        video_data = {
            'native_video': len(videos),
            'embedded_video': len(iframes)
        }
        
        # Audio
        audio = self.soup.find_all('audio')
        
        self.analysis['structure']['media'] = {
            'images': img_data,
            'video': video_data,
            'audio': len(audio)
        }
    
    def analyze_data_attributes(self):
        """Analyze data-* attributes for structured data"""
        self.logger.info("Analyzing data attributes")
        
        data_attrs = defaultdict(list)
        
        for elem in self.soup.find_all():
            for attr, value in elem.attrs.items():
                if attr.startswith('data-'):
                    data_attrs[attr].append({
                        'tag': elem.name,
                        'value': str(value)[:100]
                    })
        
        attr_summary = {
            attr: {
                'count': len(values),
                'sample_values': [v['value'] for v in values[:3]]
            }
            for attr, values in data_attrs.items()
        }
        
        self.analysis['data_structures']['data_attributes'] = dict(
            sorted(attr_summary.items(), key=lambda x: x[1]['count'], reverse=True)[:20]
        )
    
    def analyze_structured_data(self):
        """Analyze JSON-LD and microdata"""
        self.logger.info("Analyzing structured data")
        
        structured_data = {
            'json_ld': [],
            'microdata': [],
            'opengraph': {},
            'twitter_cards': {}
        }
        
        # JSON-LD
        json_ld_scripts = self.soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                structured_data['json_ld'].append(data)
            except:
                pass
        
        # Open Graph
        og_tags = self.soup.find_all('meta', property=re.compile(r'^og:'))
        for tag in og_tags:
            prop = tag.get('property', '')
            content = tag.get('content', '')
            structured_data['opengraph'][prop] = content
        
        # Twitter Cards
        twitter_tags = self.soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
        for tag in twitter_tags:
            name = tag.get('name', '')
            content = tag.get('content', '')
            structured_data['twitter_cards'][name] = content
        
        self.analysis['data_structures']['structured_data'] = structured_data
    
    def detect_website_type(self):
        """Detect website type based on patterns"""
        self.logger.info("Detecting website type")
        
        # Analyze page content for keywords
        page_text = self.soup.get_text().lower()
        class_text = ' '.join([
            ' '.join(elem.get('class', []))
            for elem in self.soup.find_all(class_=True)
        ]).lower()
        
        scores = {}
        
        for site_type, keywords in self.PATTERNS.items():
            score = 0
            for keyword in keywords:
                score += page_text.count(keyword) * 2
                score += class_text.count(keyword) * 5
            scores[site_type] = score
        
        # Get top 3 matches
        sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        detected_types = [t for t, s in sorted_types[:3] if s > 0]
        
        self.analysis['semantic_analysis']['detected_types'] = detected_types
        self.analysis['semantic_analysis']['type_scores'] = dict(sorted_types[:5])
        
        return detected_types[0] if detected_types else 'generic'
    
    def analyze_pagination(self):
        """Detect pagination patterns"""
        self.logger.info("Analyzing pagination")
        
        pagination_data = {
            'detected': False,
            'type': None,
            'patterns': []
        }
        
        # Look for pagination keywords
        pagination_keywords = [
            'next', 'prev', 'previous', 'page', 'pagination',
            'more', 'load more', 'show more'
        ]
        
        for keyword in pagination_keywords:
            links = self.soup.find_all('a', string=re.compile(keyword, re.I))
            buttons = self.soup.find_all('button', string=re.compile(keyword, re.I))
            
            if links or buttons:
                pagination_data['detected'] = True
                pagination_data['patterns'].append({
                    'keyword': keyword,
                    'links': len(links),
                    'buttons': len(buttons)
                })
        
        # Look for numbered pagination
        numbered_links = []
        for link in self.soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if text.isdigit() and ('page' in href.lower() or 'p=' in href.lower()):
                numbered_links.append(href)
        
        if numbered_links:
            pagination_data['type'] = 'numbered'
            pagination_data['sample_urls'] = numbered_links[:5]
        elif pagination_data['detected']:
            pagination_data['type'] = 'next_prev'
        
        self.analysis['semantic_analysis']['pagination'] = pagination_data
    
    def analyze_ajax_patterns(self):
        """Detect AJAX/dynamic content patterns"""
        self.logger.info("Analyzing AJAX patterns")
        
        ajax_indicators = {
            'infinite_scroll': False,
            'lazy_loading': False,
            'dynamic_forms': False,
            'spa_framework': None
        }
        
        # Check for infinite scroll indicators
        infinite_scroll_classes = ['infinite', 'scroll', 'lazy-load']
        for cls in infinite_scroll_classes:
            if self.soup.find(class_=re.compile(cls, re.I)):
                ajax_indicators['infinite_scroll'] = True
                break
        
        # Check for SPA frameworks
        scripts = self.soup.find_all('script', src=True)
        for script in scripts:
            src = script.get('src', '').lower()
            
            if 'react' in src:
                ajax_indicators['spa_framework'] = 'React'
            elif 'vue' in src:
                ajax_indicators['spa_framework'] = 'Vue.js'
            elif 'angular' in src:
                ajax_indicators['spa_framework'] = 'Angular'
        
        self.analysis['technical_details']['ajax_patterns'] = ajax_indicators
    
    def generate_scraping_strategy(self):
        """Generate comprehensive scraping strategy"""
        self.logger.log_step(5, "Generating scraping strategy", "START")
        
        strategy = {
            'recommended_approach': 'unknown',
            'complexity': 'low',
            'selectors': [],
            'extraction_rules': [],
            'pagination_strategy': None,
            'challenges': [],
            'recommendations': []
        }
        
        # Determine approach based on patterns
        list_patterns = self.analysis['content_patterns'].get('list_patterns', [])
        card_patterns = self.analysis['content_patterns'].get('card_patterns', [])
        table_patterns = self.analysis['content_patterns'].get('table_patterns', [])
        
        if table_patterns:
            strategy['recommended_approach'] = 'table_extraction'
            strategy['complexity'] = 'low'
            strategy['selectors'].append({
                'type': 'table',
                'selector': 'table',
                'description': 'Extract structured data from HTML tables'
            })
        
        elif list_patterns:
            best_pattern = list_patterns[0]
            strategy['recommended_approach'] = 'list_extraction'
            strategy['complexity'] = 'medium'
            
            if best_pattern['type'] == 'traditional_list':
                strategy['selectors'].append({
                    'type': 'list_items',
                    'selector': f"{best_pattern['tag']} > li",
                    'count': best_pattern['item_count']
                })
            else:
                classes = '.'.join(best_pattern['item_classes'])
                strategy['selectors'].append({
                    'type': 'repeated_elements',
                    'selector': f".{classes}",
                    'count': best_pattern['item_count']
                })
        
        elif card_patterns:
            best_card = card_patterns[0]
            strategy['recommended_approach'] = 'card_extraction'
            strategy['complexity'] = 'medium'
            
            classes = '.'.join(best_card['classes'])
            strategy['selectors'].append({
                'type': 'card_elements',
                'selector': f".{classes}",
                'count': best_card['count']
            })
        
        # Check for AJAX/dynamic content
        if self.analysis['technical_details'].get('ajax_patterns', {}).get('spa_framework'):
            strategy['complexity'] = 'high'
            strategy['challenges'].append('SPA framework detected - may require JavaScript rendering')
            strategy['recommendations'].append('Consider using Selenium or Playwright')
        
        # Pagination strategy
        pagination = self.analysis['semantic_analysis'].get('pagination', {})
        if pagination.get('detected'):
            strategy['pagination_strategy'] = {
                'type': pagination.get('type', 'unknown'),
                'recommendation': 'Implement pagination crawling for complete data collection'
            }
        
        # Additional recommendations
        if self.analysis['structure'].get('forms', {}).get('total', 0) > 0:
            strategy['challenges'].append('Forms detected - may require authentication')
        
        if self.analysis['structure']['links'].get('javascript', 0) > 10:
            strategy['challenges'].append('Many JavaScript links - may need browser automation')
        
        self.analysis['scraping_strategy'] = strategy
        
        self.logger.log_step(5, "Generating scraping strategy", "SUCCESS")
        self.logger.info(f"Strategy: {strategy['recommended_approach']} (complexity: {strategy['complexity']})")
    
    def save_analysis(self, output_path):
        """Save comprehensive analysis to JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis, f, indent=2, ensure_ascii=False)
            
            self.logger.log_file_operation("SAVE", output_path, True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save analysis: {str(e)}")
            return False
    
    def run_full_analysis(self, output_path=None):
        """Execute complete analysis workflow"""
        self.logger.info("Starting comprehensive analysis")
        
        try:
            # Step 1: Fetch
            if not self.fetch_page():
                return None
            
            # Step 2: Structure
            self.analyze_structure()
            
            # Step 3: Content patterns
            self.analyze_content_patterns()
            
            # Step 4: Links
            self.analyze_links()
            
            # Step 5: Media
            self.analyze_media()
            
            # Step 6: Data attributes
            self.analyze_data_attributes()
            
            # Step 7: Structured data
            self.analyze_structured_data()
            
            # Step 8: Website type
            self.detect_website_type()
            
            # Step 9: Pagination
            self.analyze_pagination()
            
            # Step 10: AJAX patterns
            self.analyze_ajax_patterns()
            
            # Step 11: Strategy
            self.generate_scraping_strategy()
            
            # Save if path provided
            if output_path:
                self.save_analysis(output_path)
            
            self.logger.info("Analysis completed successfully")
            return self.analysis
            
        except Exception as e:
            self.logger.exception(f"Analysis failed: {str(e)}")
            return None


def analyze_url(url, output_path=None, logger=None):
    """Convenience function for quick analysis"""
    analyzer = IntelligentAnalyzerV2(url, logger=logger)
    return analyzer.run_full_analysis(output_path)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
        analyze_url(url, output)
    else:
        print("Usage: python intelligent_analyzer_v2.py <url> [output.json]")

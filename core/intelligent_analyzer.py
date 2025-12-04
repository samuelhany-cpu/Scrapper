"""
Intelligent HTML Analyzer
Automatically analyzes any webpage to learn its structure, class names, and scraping patterns
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import Counter
import json
import re
from datetime import datetime


class IntelligentAnalyzer:
    """Analyzes HTML pages to understand structure and generate scraping strategies"""
    
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.soup = None
        self.analysis = {
            'url': url,
            'domain': self.domain,
            'analyzed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'structure': {},
            'content_patterns': {},
            'scraping_strategy': {}
        }
    
    def fetch_page(self):
        """Fetch the HTML page with proper headers"""
        print(f"\n[FETCH] Target: {self.url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()
            # Use lxml-xml parser for better parsing
            self.soup = BeautifulSoup(response.text, 'lxml')
            print(f"   Page fetched successfully ({len(response.content)} bytes)")
            return True
        except Exception as e:
            print(f"   Error fetching page: {e}")
            return False
    
    def analyze_structure(self):
        """Analyze the overall HTML structure"""
        print("\n[ANALYSIS] HTML structure...")
        
        # Count all tags
        all_tags = [tag.name for tag in self.soup.find_all()]
        tag_counts = Counter(all_tags)
        
        self.analysis['structure']['total_elements'] = len(all_tags)
        self.analysis['structure']['unique_tags'] = len(tag_counts)
        self.analysis['structure']['tag_distribution'] = dict(tag_counts.most_common(20))
        
        # Find main content area (common patterns)
        main_content = self._identify_main_content()
        if main_content:
            self.analysis['structure']['main_content_tag'] = main_content.name
            self.analysis['structure']['main_content_classes'] = main_content.get('class', [])
            self.analysis['structure']['main_content_id'] = main_content.get('id', '')
        
        print(f"   Total elements: {len(all_tags)}")
        print(f"   Unique tags: {len(tag_counts)}")
        print(f"   Most common: {tag_counts.most_common(5)}")
    
    def _identify_main_content(self):
        """Identify the main content container using heuristics"""
        # Common main content selectors
        candidates = []
        
        # Look for semantic HTML5 tags
        for tag in ['main', 'article', 'section']:
            elements = self.soup.find_all(tag)
            candidates.extend(elements)
        
        # Look for common class names
        common_classes = ['content', 'main', 'body', 'article', 'post', 'entry', 'container']
        for cls in common_classes:
            elements = self.soup.find_all(class_=re.compile(cls, re.I))
            candidates.extend(elements)
        
        # Look for common IDs
        common_ids = ['content', 'main', 'body', 'article', 'post']
        for id_name in common_ids:
            element = self.soup.find(id=re.compile(id_name, re.I))
            if element:
                candidates.append(element)
        
        # Return the element with most content
        if candidates:
            return max(candidates, key=lambda x: len(x.get_text(strip=True)))
        
        return None
    
    def analyze_content_patterns(self):
        """Identify repeating content patterns (lists, cards, articles, etc.)"""
        print("\n[ANALYSIS] Content patterns...")
        
        patterns = []
        
        # Find repeating class patterns
        all_elements = self.soup.find_all(class_=True)
        class_counter = Counter()
        
        for elem in all_elements:
            classes = elem.get('class', [])
            for cls in classes:
                class_counter[cls] += 1
        
        # Classes that appear multiple times might be list items
        repeating_classes = {cls: count for cls, count in class_counter.items() 
                            if count > 3 and count < 1000}  # Filter noise
        
        self.analysis['content_patterns']['repeating_classes'] = dict(
            sorted(repeating_classes.items(), key=lambda x: x[1], reverse=True)[:20]
        )
        
        # Identify list-like structures
        lists = self._find_list_patterns()
        self.analysis['content_patterns']['list_patterns'] = lists
        
        # Identify text content blocks
        text_blocks = self._find_text_blocks()
        self.analysis['content_patterns']['text_blocks'] = text_blocks
        
        print(f"   Found {len(repeating_classes)} repeating class patterns")
        print(f"   Found {len(lists)} list-like structures")
        print(f"   Found {len(text_blocks)} significant text blocks")
    
    def _find_list_patterns(self):
        """Find list-like repeating structures"""
        patterns = []
        
        # Check ul/ol lists
        for list_tag in self.soup.find_all(['ul', 'ol']):
            items = list_tag.find_all('li', recursive=False)
            if len(items) >= 3:
                sample_item = items[0]
                patterns.append({
                    'type': 'list',
                    'tag': list_tag.name,
                    'item_count': len(items),
                    'item_tag': 'li',
                    'item_classes': sample_item.get('class', []),
                    'sample_text': sample_item.get_text(strip=True)[:100]
                })
        
        # Check div-based lists (common in modern sites)
        all_divs = self.soup.find_all('div', class_=True)
        class_counts = Counter()
        
        for div in all_divs:
            classes = ' '.join(div.get('class', []))
            if classes:
                class_counts[classes] += 1
        
        for classes, count in class_counts.items():
            if count >= 5:  # At least 5 similar items
                sample = self.soup.find('div', class_=classes.split())
                if sample:
                    patterns.append({
                        'type': 'div_list',
                        'tag': 'div',
                        'item_count': count,
                        'item_classes': classes.split(),
                        'sample_text': sample.get_text(strip=True)[:100]
                    })
        
        return patterns[:10]  # Top 10 patterns
    
    def _find_text_blocks(self):
        """Find significant text content blocks"""
        blocks = []
        
        for tag in ['p', 'div', 'span', 'article', 'section']:
            elements = self.soup.find_all(tag)
            for elem in elements:
                text = elem.get_text(strip=True)
                if len(text) > 100:  # Significant text
                    blocks.append({
                        'tag': tag,
                        'classes': elem.get('class', []),
                        'id': elem.get('id', ''),
                        'text_length': len(text),
                        'preview': text[:200]
                    })
        
        # Sort by text length and return top 10
        blocks.sort(key=lambda x: x['text_length'], reverse=True)
        return blocks[:10]
    
    def analyze_links(self):
        """Analyze links on the page"""
        print("\n[ANALYSIS] Links...")
        
        all_links = self.soup.find_all('a', href=True)
        
        internal_links = []
        external_links = []
        
        for link in all_links:
            href = link.get('href', '')
            full_url = urljoin(self.url, href)
            
            if urlparse(full_url).netloc == self.domain:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)
        
        self.analysis['structure']['total_links'] = len(all_links)
        self.analysis['structure']['internal_links'] = len(internal_links)
        self.analysis['structure']['external_links'] = len(external_links)
        self.analysis['structure']['sample_internal_links'] = internal_links[:10]
        
        print(f"   Total links: {len(all_links)}")
        print(f"   Internal: {len(internal_links)}")
        print(f"   External: {len(external_links)}")
    
    def analyze_data_attributes(self):
        """Find elements with data attributes (often contain structured data)"""
        print("\n[ANALYSIS] Data attributes...")
        
        data_attrs = {}
        
        for elem in self.soup.find_all():
            for attr, value in elem.attrs.items():
                if attr.startswith('data-'):
                    if attr not in data_attrs:
                        data_attrs[attr] = []
                    data_attrs[attr].append({
                        'tag': elem.name,
                        'value': str(value)[:100]
                    })
        
        # Summarize
        data_summary = {attr: len(values) for attr, values in data_attrs.items()}
        self.analysis['structure']['data_attributes'] = dict(
            sorted(data_summary.items(), key=lambda x: x[1], reverse=True)[:20]
        )
        
        print(f"   Found {len(data_attrs)} unique data-* attributes")
    
    def generate_scraping_strategy(self):
        """Generate recommended scraping strategy based on analysis"""
        print("\n[STRATEGY] Generating scraping strategy...")
        
        strategy = {
            'recommended_approach': '',
            'selectors': [],
            'extraction_rules': [],
            'pagination': None
        }
        
        # Determine best approach
        if self.analysis['content_patterns']['list_patterns']:
            strategy['recommended_approach'] = 'list_extraction'
            
            # Get the most promising list pattern
            best_pattern = self.analysis['content_patterns']['list_patterns'][0]
            
            if best_pattern['type'] == 'list':
                strategy['selectors'].append({
                    'type': 'list_items',
                    'selector': f"{best_pattern['tag']} > li",
                    'description': f"Extract all list items from {best_pattern['tag']}"
                })
            else:
                class_selector = '.'.join(best_pattern['item_classes'])
                strategy['selectors'].append({
                    'type': 'repeated_items',
                    'selector': f"div.{class_selector}",
                    'description': f"Extract all repeated items with class {class_selector}"
                })
        
        # Add text extraction rules
        if self.analysis['content_patterns']['text_blocks']:
            strategy['extraction_rules'].append({
                'type': 'text_content',
                'description': 'Extract main text blocks',
                'method': 'get_text()'
            })
        
        # Check for pagination
        pagination_keywords = ['next', 'page', 'more', 'pagination', 'prev', 'previous']
        nav_links = self.soup.find_all('a', string=re.compile('|'.join(pagination_keywords), re.I))
        
        if nav_links:
            strategy['pagination'] = {
                'detected': True,
                'links_found': len(nav_links),
                'suggestion': 'Follow pagination links to scrape multiple pages'
            }
        
        self.analysis['scraping_strategy'] = strategy
        print(f"   Strategy: {strategy['recommended_approach']}")
    
    def save_analysis(self, output_path):
        """Save analysis to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis, f, indent=2, ensure_ascii=False)
        print(f"\n[SAVE] Analysis saved to: {output_path}")
    
    def print_summary(self):
        """Print a human-readable summary"""
        print("\n" + "=" * 100)
        print("ANALYSIS SUMMARY")
        print("=" * 100)
        
        print(f"\nURL: {self.url}")
        print(f"Domain: {self.domain}")
        
        print(f"\nStructure:")
        print(f"   Total Elements: {self.analysis['structure'].get('total_elements', 0)}")
        print(f"   Unique Tags: {self.analysis['structure'].get('unique_tags', 0)}")
        print(f"   Total Links: {self.analysis['structure'].get('total_links', 0)}")
        
        print(f"\nContent Patterns:")
        patterns = self.analysis['content_patterns'].get('list_patterns', [])
        print(f"   Repeating Structures: {len(patterns)}")
        if patterns:
            print(f"   Best Pattern: {patterns[0].get('type')} with {patterns[0].get('item_count')} items")
        
        print(f"\nRecommended Scraping Strategy:")
        strategy = self.analysis['scraping_strategy']
        print(f"   Approach: {strategy.get('recommended_approach', 'custom')}")
        print(f"   Selectors: {len(strategy.get('selectors', []))}")
        
        print("\n" + "=" * 100)
    
    def run_full_analysis(self, output_path=None):
        """Run complete analysis workflow"""
        if not self.fetch_page():
            return None
        
        self.analyze_structure()
        self.analyze_content_patterns()
        self.analyze_links()
        self.analyze_data_attributes()
        self.generate_scraping_strategy()
        
        if output_path:
            self.save_analysis(output_path)
        
        self.print_summary()
        
        return self.analysis


def analyze_url(url, output_path=None):
    """Convenience function to analyze a URL"""
    analyzer = IntelligentAnalyzer(url)
    return analyzer.run_full_analysis(output_path)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else None
        analyze_url(url, output)
    else:
        print("Usage: python intelligent_analyzer.py <url> [output.json]")
        print("\nExample:")
        print("  python intelligent_analyzer.py https://example.com analysis.json")

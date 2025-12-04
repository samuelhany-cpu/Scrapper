import logging
import os
from datetime import datetime
from .config import Config

class ScraperLogger:
    def __init__(self, session_id=None):
        Config.ensure_directories()
        
        if session_id is None:
            session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        self.session_id = session_id
        self.log_file = os.path.join(Config.LOGS_DIR, f'scraper_{session_id}.log')
        
        # Create logger
        self.logger = logging.getLogger(f'scraper_{session_id}')
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # File handler - detailed logging
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler - important messages only
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.stats = {
            'start_time': datetime.now(),
            'pages_scraped': 0,
            'items_extracted': 0,
            'errors': 0,
            'warnings': 0
        }
    
    def info(self, message):
        self.logger.info(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def warning(self, message):
        self.stats['warnings'] += 1
        self.logger.warning(message)
    
    def error(self, message):
        self.stats['errors'] += 1
        self.logger.error(message)
    
    def critical(self, message):
        self.stats['errors'] += 1
        self.logger.critical(message)
    
    def increment_pages(self):
        self.stats['pages_scraped'] += 1
    
    def increment_items(self, count=1):
        self.stats['items_extracted'] += count
    
    def get_stats(self):
        self.stats['end_time'] = datetime.now()
        self.stats['duration'] = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        return self.stats
    
    def get_log_file(self):
        return self.log_file

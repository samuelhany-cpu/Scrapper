"""
Professional Logging System for Intelligent Web Scraper
Structured logging with multiple handlers and formatters
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
import json


class ScraperLogger:
    """Professional logging system with structured output"""
    
    def __init__(self, name='intelligent_scraper', log_dir='logs'):
        """
        Initialize logger with multiple handlers
        
        Args:
            name: Logger name
            log_dir: Directory for log files
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Setup handlers
        self._setup_file_handler()
        self._setup_console_handler()
        self._setup_error_handler()
        
        # Statistics
        self.stats = {
            'start_time': datetime.now(),
            'end_time': None,
            'errors': 0,
            'warnings': 0,
            'info': 0,
            'debug': 0
        }
    
    def _setup_file_handler(self):
        """Setup rotating file handler for all logs"""
        log_file = self.log_dir / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Detailed format for file
        file_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)-8s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(file_handler)
    
    def _setup_console_handler(self):
        """Setup console handler for INFO and above"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Simple format for console
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(console_handler)
    
    def _setup_error_handler(self):
        """Setup separate handler for errors"""
        error_file = self.log_dir / f"{self.name}_errors_{datetime.now().strftime('%Y%m%d')}.log"
        
        error_handler = RotatingFileHandler(
            error_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        error_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s\n'
            'File: %(pathname)s:%(lineno)d\n'
            'Function: %(funcName)s\n'
            '---',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        
        self.logger.addHandler(error_handler)
    
    def debug(self, message, **kwargs):
        """Log debug message"""
        self.stats['debug'] += 1
        self.logger.debug(self._format_message(message, kwargs))
    
    def info(self, message, **kwargs):
        """Log info message"""
        self.stats['info'] += 1
        self.logger.info(self._format_message(message, kwargs))
    
    def warning(self, message, **kwargs):
        """Log warning message"""
        self.stats['warnings'] += 1
        self.logger.warning(self._format_message(message, kwargs))
    
    def error(self, message, **kwargs):
        """Log error message"""
        self.stats['errors'] += 1
        self.logger.error(self._format_message(message, kwargs))
    
    def critical(self, message, **kwargs):
        """Log critical message"""
        self.stats['errors'] += 1
        self.logger.critical(self._format_message(message, kwargs))
    
    def exception(self, message, **kwargs):
        """Log exception with traceback"""
        self.stats['errors'] += 1
        self.logger.exception(self._format_message(message, kwargs))
    
    def _format_message(self, message, metadata):
        """Format message with optional metadata"""
        if metadata:
            metadata_str = ' | '.join([f"{k}={v}" for k, v in metadata.items()])
            return f"{message} | {metadata_str}"
        return message
    
    def log_step(self, step_number, step_name, status='START'):
        """Log workflow step"""
        message = f"STEP {step_number}/5: {step_name} [{status}]"
        if status == 'START':
            self.info(message)
        elif status == 'SUCCESS':
            self.info(message)
        elif status == 'FAIL':
            self.error(message)
        else:
            self.warning(message)
    
    def log_metric(self, metric_name, value, unit=''):
        """Log performance metric"""
        unit_str = f" {unit}" if unit else ""
        self.info(f"METRIC: {metric_name} = {value}{unit_str}")
    
    def log_url_fetch(self, url, status_code, duration, size):
        """Log URL fetch operation"""
        self.info(
            f"URL Fetched",
            url=url,
            status=status_code,
            duration_ms=f"{duration*1000:.0f}",
            size_bytes=size
        )
    
    def log_data_extraction(self, item_type, count):
        """Log data extraction"""
        self.info(f"Extracted {count} {item_type} items")
    
    def log_file_operation(self, operation, file_path, success=True):
        """Log file operation"""
        status = "SUCCESS" if success else "FAILED"
        self.info(f"File {operation}: {file_path} [{status}]")
    
    def get_stats(self):
        """Get logging statistics"""
        self.stats['end_time'] = datetime.now()
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        self.stats['duration_seconds'] = duration
        return self.stats.copy()
    
    def save_stats(self, output_path):
        """Save statistics to JSON file"""
        stats = self.get_stats()
        
        # Convert datetime to string
        stats['start_time'] = stats['start_time'].isoformat()
        if stats['end_time']:
            stats['end_time'] = stats['end_time'].isoformat()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        self.info(f"Statistics saved to {output_path}")
    
    def close(self):
        """Close all handlers"""
        for handler in self.logger.handlers:
            handler.close()
        self.logger.handlers = []


# Global logger instance
_global_logger = None


def get_logger(name='intelligent_scraper'):
    """Get global logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = ScraperLogger(name)
    return _global_logger


def close_logger():
    """Close global logger"""
    global _global_logger
    if _global_logger:
        _global_logger.close()
        _global_logger = None

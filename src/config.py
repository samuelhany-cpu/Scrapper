import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Twitter Authentication
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME', '')
    TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD', '')
    
    # Scraping Configuration
    MAX_DEPTH = 3
    REQUEST_TIMEOUT = 60  # Increased to 60 seconds for complex sites
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    # Output Configuration
    OUTPUT_DIR = 'output'
    LOGS_DIR = 'logs'
    REPORTS_DIR = 'reports'
    
    # Language Configuration
    LANGUAGE = os.getenv('LANGUAGE', 'en')  # 'en' or 'ar'
    SUPPORT_RTL = True  # Right-to-Left support for Arabic
    
    # AI Configuration
    AI_MODEL = 'gpt-4o-mini'  # Updated to available model
    AI_TEMPERATURE = 0.1  # Lower temperature for more consistent extraction
    
    # Scraping Settings
    RESPECT_ROBOTS_TXT = True
    JAVASCRIPT_ENABLED = True
    WAIT_FOR_LOAD = 5000  # milliseconds - increased for JS-heavy sites
    
    @staticmethod
    def ensure_directories():
        """Create necessary directories if they don't exist"""
        for directory in [Config.OUTPUT_DIR, Config.LOGS_DIR, Config.REPORTS_DIR]:
            os.makedirs(directory, exist_ok=True)

import streamlit as st
import os
import sys
from datetime import datetime

from config import Config
from logger import ScraperLogger
from scraper_selenium import UniversalScraper  # Using Selenium for Python 3.13 compatibility
from report_generator import ReportGenerator
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Universal Web Scraper",
    page_icon=":globe_with_meridians:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .status-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'scraping_complete' not in st.session_state:
        st.session_state.scraping_complete = False
    if 'scraped_data' not in st.session_state:
        st.session_state.scraped_data = None
    if 'csv_file' not in st.session_state:
        st.session_state.csv_file = None
    if 'report_file' not in st.session_state:
        st.session_state.report_file = None
    if 'log_messages' not in st.session_state:
        st.session_state.log_messages = []
    if 'stats' not in st.session_state:
        st.session_state.stats = None

def run_scraper(url, progress_placeholder, log_placeholder):
    """Run the scraper synchronously"""
    # Create logger
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    logger = ScraperLogger(session_id)
    
    # Update progress
    progress_placeholder.info("Initializing scraper...")
    
    # Create scraper
    scraper = UniversalScraper(logger)
    
    # Run scraping
    progress_placeholder.info("Loading webpage and analyzing content...")
    success = scraper.scrape_url(url)
    
    if success:
        progress_placeholder.success("Scraping completed successfully")
        
        # Save to CSV
        progress_placeholder.info("Saving data to CSV...")
        csv_file = scraper.save_to_csv()
        
        # Generate report
        progress_placeholder.info("Generating report...")
        report_gen = ReportGenerator(logger, scraper)
        report_file = report_gen.generate_report(csv_file)
        
        # Store results in session state
        st.session_state.scraped_data = scraper.get_data()
        st.session_state.csv_file = csv_file
        st.session_state.report_file = report_file
        st.session_state.stats = logger.get_stats()
        st.session_state.scraping_complete = True
        
        progress_placeholder.success("All tasks completed successfully")
        
        # Read and display log
        try:
            with open(logger.get_log_file(), 'r', encoding='utf-8') as f:
                log_content = f.read()
                st.session_state.log_messages = log_content
        except Exception as e:
            st.session_state.log_messages = f"Could not read log file: {str(e)}"
        
    else:
        progress_placeholder.error("Scraping failed. Check logs for details.")
        st.session_state.scraping_complete = False

def main():
    # Initialize session state
    init_session_state()
    
    # Ensure directories exist
    Config.ensure_directories()
    
    # Header
    st.markdown('<div class="main-header">Universal Web Scraper</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Intelligent data extraction from any website</div>', unsafe_allow_html=True)
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("Configuration")
        
        st.subheader("API Settings")
        api_key = st.text_input("OpenAI API Key (Optional)", type="password", 
                                help="For AI-powered content analysis. Leave empty for traditional scraping.")
        
        if api_key:
            Config.OPENAI_API_KEY = api_key
            os.environ['OPENAI_API_KEY'] = api_key
        
        st.divider()
        
        st.subheader("Scraping Options")
        Config.JAVASCRIPT_ENABLED = st.checkbox("Enable JavaScript", value=True,
                                               help="Required for dynamic websites")
        Config.WAIT_FOR_LOAD = st.slider("Page Load Wait Time (ms)", 500, 5000, 2000, 500,
                                         help="Wait time after page load for dynamic content")
        
        st.divider()
        
        st.subheader("About")
        st.info("""
        This scraper uses:
        - Playwright for browser automation
        - BeautifulSoup for HTML parsing
        - OpenAI GPT-4 for intelligent content understanding
        - Pandas for data processing
        
        It can extract data from any website and save it to CSV format.
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Target URL")
        url = st.text_input("Enter the webpage URL to scrape", 
                           placeholder="https://example.com",
                           help="Enter the full URL including http:// or https://")
        
        if st.button("Start Scraping", type="primary", use_container_width=True):
            if url:
                # Reset session state
                st.session_state.scraping_complete = False
                st.session_state.scraped_data = None
                st.session_state.csv_file = None
                st.session_state.report_file = None
                
                # Create placeholders
                progress_placeholder = st.empty()
                log_placeholder = st.empty()
                
                # Run scraper
                run_scraper(url, progress_placeholder, log_placeholder)
                
                # Rerun to show results
                st.rerun()
            else:
                st.error("Please enter a valid URL")
    
    with col2:
        st.subheader("Quick Info")
        st.info("""
        **Steps:**
        1. Enter target URL
        2. Configure options (optional)
        3. Click 'Start Scraping'
        4. Download results
        """)
    
    # Results section
    if st.session_state.scraping_complete:
        st.divider()
        st.header("Results")
        
        # Statistics
        if st.session_state.stats:
            st.subheader("Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Pages Scraped", st.session_state.stats['pages_scraped'])
            with col2:
                st.metric("Items Extracted", st.session_state.stats['items_extracted'])
            with col3:
                st.metric("Duration", f"{st.session_state.stats['duration']:.2f}s")
            with col4:
                st.metric("Errors", st.session_state.stats['errors'])
        
        # Data preview
        if st.session_state.scraped_data:
            st.divider()
            st.subheader("Data Preview")
            
            df = pd.DataFrame(st.session_state.scraped_data)
            st.dataframe(df, use_container_width=True, height=400)
            
            st.info(f"Total records: {len(df)} | Total columns: {len(df.columns)}")
        
        # Download section
        st.divider()
        st.subheader("Download Files")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.csv_file and os.path.exists(st.session_state.csv_file):
                with open(st.session_state.csv_file, 'rb') as f:
                    st.download_button(
                        label="Download CSV Data",
                        data=f,
                        file_name=os.path.basename(st.session_state.csv_file),
                        mime="text/csv",
                        use_container_width=True
                    )
        
        with col2:
            if st.session_state.report_file and os.path.exists(st.session_state.report_file):
                with open(st.session_state.report_file, 'rb') as f:
                    st.download_button(
                        label="Download PDF Report",
                        data=f,
                        file_name=os.path.basename(st.session_state.report_file),
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        with col3:
            if st.session_state.log_messages:
                st.download_button(
                    label="Download Log File",
                    data=st.session_state.log_messages,
                    file_name=f"scraper_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Log viewer
        st.divider()
        with st.expander("View Detailed Logs", expanded=False):
            if st.session_state.log_messages:
                st.text_area("Log Output", st.session_state.log_messages, height=300)

if __name__ == "__main__":
    main()

"""
Professional Intelligent Web Scraper - Streamlit Application
Enterprise-grade web scraping with intelligent HTML analysis and automated workflows
"""

import streamlit as st
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import subprocess
import pandas as pd
import time

# Import core modules
from core.intelligent_analyzer_v2 import IntelligentAnalyzerV2
from core.scraper_generator import ScraperGenerator
from core.data_analyzer import DataAnalyzer
from core.pdf_generator import PDFGenerator
from core.professional_logger import get_logger

# Page configuration
st.set_page_config(
    page_title="Intelligent Web Scraper",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
    /* Main layout */
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Status boxes */
    .status-box {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
        font-family: 'Segoe UI', sans-serif;
    }
    .status-success {
        background-color: #f0fdf4;
        border-color: #22c55e;
        color: #166534;
    }
    .status-error {
        background-color: #fef2f2;
        border-color: #ef4444;
        color: #991b1b;
    }
    .status-info {
        background-color: #eff6ff;
        border-color: #3b82f6;
        color: #1e40af;
    }
    .status-warning {
        background-color: #fffbeb;
        border-color: #f59e0b;
        color: #92400e;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Step indicators */
    .step-indicator {
        display: inline-block;
        width: 32px;
        height: 32px;
        background-color: #3b82f6;
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 32px;
        font-weight: 600;
        margin-right: 10px;
    }
    
    .step-complete {
        background-color: #22c55e;
    }
    
    .step-active {
        background-color: #f59e0b;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Professional tables */
    .dataframe {
        font-size: 0.9rem;
        border-collapse: collapse;
    }
    
    /* Buttons */
    .stButton>button {
        font-weight: 500;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'workflow_complete' not in st.session_state:
        st.session_state.workflow_complete = False
    if 'workflow_results' not in st.session_state:
        st.session_state.workflow_results = {}
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = None
    if 'execution_logs' not in st.session_state:
        st.session_state.execution_logs = []


def add_log(message, level="INFO"):
    """Add log message to execution logs"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}"
    st.session_state.execution_logs.append(log_entry)


def run_intelligent_workflow(url, outputs_dir, options):
    """Execute the 5-step intelligent scraping workflow"""
    
    results = {
        'success': False,
        'steps_completed': 0,
        'files_generated': [],
        'errors': [],
        'statistics': {}
    }
    
    try:
        # Generate unique identifiers
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        domain = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')[:50]
        base_name = f"{domain}_{timestamp}"
        
        # STEP 1: Analyze HTML Structure
        st.session_state.current_step = 1
        add_log(f"Starting analysis of {url}", "INFO")
        
        step1_status = st.empty()
        step1_status.info("STEP 1/5: Analyzing HTML structure...")
        
        logger = get_logger('streamlit_scraper')
        
        analyzer = IntelligentAnalyzerV2(url, logger=logger)
        analysis_path = outputs_dir / f"{base_name}_analysis.json"
        
        analysis = analyzer.run_full_analysis(str(analysis_path))
        
        if not analysis:
            raise Exception("Failed to analyze URL")
        
        results['files_generated'].append(str(analysis_path))
        results['steps_completed'] = 1
        st.session_state.analysis_data = analysis
        
        add_log(f"HTML analysis complete: {analysis['structure'].get('total_elements', 0)} elements found", "SUCCESS")
        step1_status.success("STEP 1/5: HTML structure analyzed successfully")
        
        time.sleep(0.5)
        
        # STEP 2: Generate Custom Scraper
        st.session_state.current_step = 2
        add_log("Generating custom scraper code", "INFO")
        
        step2_status = st.empty()
        step2_status.info("STEP 2/5: Generating custom scraper...")
        
        scraper_path = outputs_dir / f"{base_name}_scraper.py"
        
        generator = ScraperGenerator(analysis)
        scraper_code = generator.generate_full_scraper(
            output_file=str(scraper_path),
            rate_limit=options['rate_limit']
        )
        
        results['files_generated'].append(str(scraper_path))
        results['steps_completed'] = 2
        
        add_log(f"Scraper generated: {len(scraper_code)} characters", "SUCCESS")
        step2_status.success("STEP 2/5: Custom scraper generated successfully")
        
        time.sleep(0.5)
        
        # STEP 3: Execute Scraper
        if options['auto_run_scraper']:
            st.session_state.current_step = 3
            add_log("Executing generated scraper", "INFO")
            
            step3_status = st.empty()
            step3_status.info("STEP 3/5: Extracting data from website...")
            
            # Run scraper as subprocess
            result = subprocess.run(
                [sys.executable, str(scraper_path)],
                cwd=str(outputs_dir),
                capture_output=True,
                text=True,
                timeout=options['scraper_timeout']
            )
            
            # Find generated CSV files
            csv_files = list(outputs_dir.glob(f"scraped_{domain}*.csv"))
            
            if csv_files:
                csv_file = csv_files[-1]
                results['files_generated'].append(str(csv_file))
                results['steps_completed'] = 3
                
                # Load data to get statistics
                df = pd.read_csv(csv_file)
                results['statistics']['rows_extracted'] = len(df)
                results['statistics']['columns'] = len(df.columns)
                
                add_log(f"Data extracted: {len(df)} rows, {len(df.columns)} columns", "SUCCESS")
                step3_status.success(f"STEP 3/5: Data extracted successfully ({len(df)} rows)")
            else:
                add_log("Scraper executed but no CSV file found", "WARNING")
                step3_status.warning("STEP 3/5: Scraper executed with warnings")
            
            time.sleep(0.5)
            
            # STEP 4: Analyze Scraped Data
            if csv_files and options['analyze_data']:
                st.session_state.current_step = 4
                add_log("Analyzing scraped data", "INFO")
                
                step4_status = st.empty()
                step4_status.info("STEP 4/5: Performing statistical analysis...")
                
                data_analyzer = DataAnalyzer(str(csv_file), str(outputs_dir))
                analysis_result = data_analyzer.analyze()
                
                data_analysis_path = outputs_dir / f"{base_name}_data_analysis.json"
                with open(data_analysis_path, 'w', encoding='utf-8') as f:
                    json.dump(analysis_result, f, indent=2, ensure_ascii=False)
                
                results['files_generated'].append(str(data_analysis_path))
                
                # Count charts generated
                chart_files = list(outputs_dir.glob(f"chart_{domain}*.png"))
                results['files_generated'].extend([str(f) for f in chart_files])
                results['statistics']['charts_generated'] = len(chart_files)
                results['statistics']['insights'] = len(analysis_result.get('insights', []))
                results['steps_completed'] = 4
                
                add_log(f"Data analysis complete: {len(chart_files)} charts, {len(analysis_result.get('insights', []))} insights", "SUCCESS")
                step4_status.success(f"STEP 4/5: Data analyzed ({len(chart_files)} charts generated)")
                
                time.sleep(0.5)
                
                # STEP 5: Generate PDF Report
                if options['generate_pdf']:
                    st.session_state.current_step = 5
                    add_log("Generating PDF report", "INFO")
                    
                    step5_status = st.empty()
                    step5_status.info("STEP 5/5: Creating professional PDF report...")
                    
                    pdf_generator = PDFGenerator(str(csv_file), str(data_analysis_path), url)
                    pdf_path = outputs_dir / f"{base_name}_report.pdf"
                    
                    pdf_generator.generate(str(pdf_path))
                    
                    results['files_generated'].append(str(pdf_path))
                    results['steps_completed'] = 5
                    
                    file_size = os.path.getsize(pdf_path) / 1024  # KB
                    add_log(f"PDF report generated: {file_size:.1f} KB", "SUCCESS")
                    step5_status.success(f"STEP 5/5: PDF report generated ({file_size:.1f} KB)")
        
        # Save workflow summary
        workflow_summary = {
            'url': url,
            'timestamp': timestamp,
            'steps_completed': results['steps_completed'],
            'files_generated': results['files_generated'],
            'statistics': results['statistics'],
            'options': options
        }
        
        summary_path = outputs_dir / f"{base_name}_workflow.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(workflow_summary, f, indent=2, ensure_ascii=False)
        
        results['files_generated'].append(str(summary_path))
        results['success'] = True
        add_log("Workflow completed successfully", "SUCCESS")
        
    except Exception as e:
        error_msg = f"Workflow error: {str(e)}"
        results['errors'].append(error_msg)
        add_log(error_msg, "ERROR")
        st.error(f"Error: {str(e)}")
    
    return results


def main():
    """Main application"""
    
    init_session_state()
    
    # Ensure output directory exists
    outputs_dir = Path("outputs/workflow")
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    # Header
    st.markdown('<div class="main-header">Intelligent Web Scraper</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enterprise-grade automated web scraping with intelligent HTML analysis</div>', unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("Configuration")
        
        st.subheader("Workflow Options")
        
        auto_run_scraper = st.checkbox(
            "Auto-execute scraper",
            value=True,
            help="Automatically run the generated scraper code"
        )
        
        analyze_data = st.checkbox(
            "Perform data analysis",
            value=True,
            help="Generate statistical analysis and visualizations"
        )
        
        generate_pdf = st.checkbox(
            "Generate PDF report",
            value=True,
            help="Create a comprehensive PDF report"
        )
        
        st.divider()
        
        st.subheader("Advanced Settings")
        
        rate_limit = st.slider(
            "Request delay (seconds)",
            min_value=0.5,
            max_value=5.0,
            value=1.0,
            step=0.5,
            help="Delay between requests to respect server resources"
        )
        
        scraper_timeout = st.number_input(
            "Scraper timeout (seconds)",
            min_value=30,
            max_value=600,
            value=300,
            step=30,
            help="Maximum time to wait for scraper execution"
        )
        
        max_pages = st.number_input(
            "Maximum pages to scrape",
            min_value=1,
            max_value=100,
            value=10,
            help="Limit the number of pages to scrape"
        )
        
        st.divider()
        
        st.subheader("Example URLs")
        
        examples = {
            "Quotes": "http://quotes.toscrape.com",
            "Books": "http://books.toscrape.com",
            "News (HN)": "https://news.ycombinator.com",
            "Wikipedia": "https://en.wikipedia.org/wiki/Web_scraping"
        }
        
        for name, example_url in examples.items():
            if st.button(name, use_container_width=True):
                st.session_state.example_url = example_url
                st.rerun()
    
    # Main content
    if not st.session_state.workflow_complete:
        # Input section
        st.subheader("Target Configuration")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            default_url = st.session_state.get('example_url', '')
            url = st.text_input(
                "Website URL",
                value=default_url,
                placeholder="https://example.com",
                help="Enter the complete URL including protocol (http:// or https://)"
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            start_button = st.button(
                "Start Workflow",
                type="primary",
                use_container_width=True,
                disabled=not url
            )
        
        # Information cards
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="status-box status-info">
                <strong>Step 1: HTML Analysis</strong><br/>
                Intelligent structure detection and pattern recognition
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="status-box status-info">
                <strong>Step 2: Code Generation</strong><br/>
                Dynamic scraper creation with optimal selectors
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="status-box status-info">
                <strong>Step 3: Data Extraction</strong><br/>
                Automated data collection with error handling
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="status-box status-info">
                <strong>Step 4: Statistical Analysis</strong><br/>
                Comprehensive data analysis and visualization
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="status-box status-info">
                <strong>Step 5: Report Generation</strong><br/>
                Professional PDF documentation with insights
            </div>
            """, unsafe_allow_html=True)
        
        # Execute workflow
        if start_button and url:
            # Reset session
            st.session_state.workflow_complete = False
            st.session_state.workflow_results = {}
            st.session_state.current_step = 0
            st.session_state.execution_logs = []
            
            # Collect options
            options = {
                'auto_run_scraper': auto_run_scraper,
                'analyze_data': analyze_data,
                'generate_pdf': generate_pdf,
                'rate_limit': rate_limit,
                'scraper_timeout': scraper_timeout,
                'max_pages': max_pages
            }
            
            # Progress container
            st.divider()
            st.subheader("Workflow Execution")
            
            progress_bar = st.progress(0)
            
            # Execute workflow
            with st.spinner("Executing intelligent workflow..."):
                results = run_intelligent_workflow(url, outputs_dir, options)
            
            # Update progress
            progress = (results['steps_completed'] / 5) * 100
            progress_bar.progress(int(progress))
            
            # Store results
            st.session_state.workflow_results = results
            st.session_state.workflow_complete = results['success']
            
            # Rerun to show results
            st.rerun()
    
    else:
        # Results section
        results = st.session_state.workflow_results
        
        st.divider()
        st.header("Workflow Results")
        
        # Success summary
        if results['success']:
            st.markdown("""
            <div class="status-box status-success">
                <strong>Workflow Completed Successfully</strong><br/>
                All steps executed without critical errors
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-box status-error">
                <strong>Workflow Completed with Errors</strong><br/>
                Some steps failed to execute
            </div>
            """, unsafe_allow_html=True)
        
        # Statistics
        st.subheader("Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Steps Completed", f"{results['steps_completed']}/5")
        
        with col2:
            st.metric("Files Generated", len(results['files_generated']))
        
        with col3:
            rows = results['statistics'].get('rows_extracted', 0)
            st.metric("Rows Extracted", rows)
        
        with col4:
            charts = results['statistics'].get('charts_generated', 0)
            st.metric("Charts Created", charts)
        
        # Data preview
        if results['statistics'].get('rows_extracted', 0) > 0:
            st.divider()
            st.subheader("Data Preview")
            
            csv_files = [f for f in results['files_generated'] if f.endswith('.csv')]
            if csv_files:
                df = pd.read_csv(csv_files[0])
                
                st.dataframe(
                    df.head(50),
                    use_container_width=True,
                    height=400
                )
                
                st.caption(f"Showing first 50 of {len(df)} rows")
        
        # HTML Analysis
        if st.session_state.analysis_data:
            st.divider()
            st.subheader("HTML Structure Analysis")
            
            analysis = st.session_state.analysis_data
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Elements", analysis['structure'].get('total_elements', 0))
                st.metric("Unique Tags", analysis['structure'].get('unique_tags', 0))
            
            with col2:
                st.metric("Total Links", analysis['structure'].get('total_links', 0))
                st.metric("Internal Links", analysis['structure'].get('internal_links', 0))
            
            with col3:
                patterns = analysis['content_patterns'].get('list_patterns', [])
                st.metric("Repeating Patterns", len(patterns))
                
                if patterns:
                    best_pattern = patterns[0]
                    st.info(f"Best pattern: {best_pattern.get('item_count', 0)} items")
        
        # Charts
        chart_files = [f for f in results['files_generated'] if f.endswith('.png')]
        if chart_files:
            st.divider()
            st.subheader("Visualizations")
            
            cols = st.columns(3)
            for idx, chart_path in enumerate(chart_files[:6]):
                with cols[idx % 3]:
                    st.image(chart_path, use_column_width=True)
                    st.caption(Path(chart_path).stem.replace('_', ' ').title())
        
        # Download section
        st.divider()
        st.subheader("Download Files")
        
        download_cols = st.columns(5)
        
        # CSV
        csv_files = [f for f in results['files_generated'] if f.endswith('.csv')]
        if csv_files:
            with download_cols[0]:
                with open(csv_files[0], 'rb') as f:
                    st.download_button(
                        label="CSV Data",
                        data=f,
                        file_name=Path(csv_files[0]).name,
                        mime="text/csv",
                        use_container_width=True
                    )
        
        # PDF
        pdf_files = [f for f in results['files_generated'] if f.endswith('.pdf')]
        if pdf_files:
            with download_cols[1]:
                with open(pdf_files[0], 'rb') as f:
                    st.download_button(
                        label="PDF Report",
                        data=f,
                        file_name=Path(pdf_files[0]).name,
                        mime="application/pdf",
                        use_container_width=True
                    )
        
        # Analysis JSON
        analysis_files = [f for f in results['files_generated'] if 'analysis.json' in f]
        if analysis_files:
            with download_cols[2]:
                with open(analysis_files[0], 'rb') as f:
                    st.download_button(
                        label="Analysis JSON",
                        data=f,
                        file_name=Path(analysis_files[0]).name,
                        mime="application/json",
                        use_container_width=True
                    )
        
        # Scraper code
        scraper_files = [f for f in results['files_generated'] if f.endswith('_scraper.py')]
        if scraper_files:
            with download_cols[3]:
                with open(scraper_files[0], 'rb') as f:
                    st.download_button(
                        label="Scraper Code",
                        data=f,
                        file_name=Path(scraper_files[0]).name,
                        mime="text/x-python",
                        use_container_width=True
                    )
        
        # Logs
        if st.session_state.execution_logs:
            with download_cols[4]:
                log_content = '\n'.join(st.session_state.execution_logs)
                st.download_button(
                    label="Execution Logs",
                    data=log_content,
                    file_name=f"workflow_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Execution logs
        st.divider()
        with st.expander("View Execution Logs", expanded=False):
            if st.session_state.execution_logs:
                log_text = '\n'.join(st.session_state.execution_logs)
                st.text_area("Logs", log_text, height=300, disabled=True)
        
        # New workflow button
        st.divider()
        if st.button("Start New Workflow", type="primary", use_container_width=False):
            st.session_state.workflow_complete = False
            st.session_state.workflow_results = {}
            st.session_state.current_step = 0
            st.session_state.execution_logs = []
            st.session_state.analysis_data = None
            st.rerun()
    
    # Footer
    st.divider()
    st.caption("Intelligent Web Scraper v2.0 | Professional Enterprise Solution")


if __name__ == "__main__":
    main()

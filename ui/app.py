"""
Main UI application for the Dental AI Diagnostic Assistant
"""
import streamlit as st
from typing import Dict, Any, List, Optional
import sys
import os
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ai_engine import DentalAIEngine
from src.report_generator import ReportGenerator
from src.image_processor import ImageProcessor
import config
from ui.pages.analysis import render_analysis_page
from ui.pages.history import render_history_page
from ui.pages.settings import render_settings_page

class DentalAIWebApp:
    """Main web application for the Dental AI Diagnostic Assistant"""
    
    def __init__(self):
        """Initialize the web application"""
        self.setup()
        
    def setup(self):
        """Set up the application state and configuration"""
        # Initialize session state if not already done
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.api_key = ""
            st.session_state.ai_engine = None
            st.session_state.report_generator = None
            st.session_state.image_processor = None
            st.session_state.history = []
            st.session_state.current_analysis = None
            st.session_state.crm_settings = {
                "type": "None",
                "api_endpoint": "",
                "username": "",
                "password": "",
                "auto_export": False
            }
    
    def initialize_components(self):
        """Initialize AI components based on API key"""
        if st.session_state.api_key:
            st.session_state.ai_engine = DentalAIEngine(st.session_state.api_key)
            st.session_state.report_generator = ReportGenerator(st.session_state.api_key)
            st.session_state.image_processor = ImageProcessor()
    
    def run(self):
        """Run the web application"""
        # Set up page configuration
        st.set_page_config(
            page_title=config.APP_NAME,
            page_icon="🦷",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Header
        st.title("🦷 Dental AI Diagnostic Assistant")
        
        # Sidebar with API key input
        with st.sidebar:
            st.header("Configuration")
            api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key)
            
            if api_key != st.session_state.api_key:
                st.session_state.api_key = api_key
                self.initialize_components()
            
            if not api_key:
                st.warning("Please enter your OpenAI API key to use the application.")
        
        # Initialize components if needed
        if st.session_state.ai_engine is None and st.session_state.api_key:
            self.initialize_components()
        
        # Main navigation
        tab1, tab2, tab3 = st.tabs(["Patient Analysis", "Report History", "Settings"])
        
        with tab1:
            render_analysis_page()
            
        with tab2:
            render_history_page()
            
        with tab3:
            render_settings_page()


if __name__ == "__main__":
    app = DentalAIWebApp()
    app.run()

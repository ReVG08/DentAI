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

        # --- Robust Session State Initialization for All Settings ---
        ss = st.session_state
        ss.setdefault("initialized", True)
        ss.setdefault("api_keys", {})
        ss.setdefault("ai_settings", {})
        ss.setdefault("theme", {"mode": "Light"})
        ss.setdefault("user_profile", {})
        ss.setdefault("report_customization", {})
        ss.setdefault("language", {"lang": "English"})
        ss.setdefault("notifications", {})
        ss.setdefault("data_privacy", {})
        ss.setdefault("crm_settings", {"type": "None"})
        ss.setdefault("ai_engine", None)
        ss.setdefault("report_generator", None)
        ss.setdefault("image_processor", None)
        ss.setdefault("history", [])
        ss.setdefault("current_analysis", None)

        # Legacy for backwards-compatibility (if code elsewhere expects .api_key)
        if not hasattr(ss, "api_key"):
            ss.api_key = ss.get("api_keys", {}).get("openai", "")

    def initialize_components(self):
        """Initialize AI components based on API key and settings"""
        api_key = st.session_state.get("api_keys", {}).get("openai", "")
        ai_settings = st.session_state.get("ai_settings", {})
        # Only re-init if api_key is present
        if api_key:
            st.session_state.ai_engine = DentalAIEngine(
                api_key,
                model=ai_settings.get("model", "gpt-4"),
                temperature=ai_settings.get("temperature", 0.4),
                max_tokens=ai_settings.get("max_tokens", 1024)
            )
            st.session_state.report_generator = ReportGenerator(api_key)
            st.session_state.image_processor = ImageProcessor()

    def run(self):
        """Run the web application"""
        # Set up page configuration (theme integration)
        theme = st.session_state.get("theme", {})
        st.set_page_config(
            page_title=getattr(config, "APP_NAME", "Dental AI Assistant"),
            page_icon="🦷",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Header
        st.title("🦷 Dental AI Diagnostic Assistant by Renato Gloe")

        # Sidebar: configuration and navigation
        with st.sidebar:
            st.header("Configuration")

            # API key input, now synced with session_state["api_keys"]["openai"]
            api_keys = st.session_state.get("api_keys", {})
            openai_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=api_keys.get("openai", ""),
                key="sidebar_openai_api_key"
            )
            if openai_key != api_keys.get("openai", ""):
                st.session_state.api_keys["openai"] = openai_key
                self.initialize_components()

            if not openai_key:
                st.warning("Please enter your OpenAI API key to use the application.")

            # Optionally show quick theme or branding
            theme_mode = theme.get("mode", "Light")
            st.markdown(f"**Theme:** {theme_mode}  \n**Primary Color:** {theme.get('primary_color', '#0066cc')}")

            # Show profile if set
            profile = st.session_state.get("user_profile", {})
            if profile.get("name"):
                st.markdown(f"**Clinic:** {profile['name']}")
                if profile.get("logo"):
                    st.image(profile["logo"], width=80)

        # Ensure components always initialized if API key present
        if st.session_state.ai_engine is None and st.session_state.api_keys.get("openai"):
            self.initialize_components()

        # Main navigation using tabs
        tabs = st.tabs(["Patient Analysis", "Report History", "Settings"])
        with tabs[0]:
            render_analysis_page()
        with tabs[1]:
            render_history_page()
        with tabs[2]:
            render_settings_page()

if __name__ == "__main__":
    app = DentalAIWebApp()
    app.run()
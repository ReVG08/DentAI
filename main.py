"""
Dental AI Diagnostic Assistant
Main entry point for the application
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import the UI app
from ui.app import DentalAIWebApp

if __name__ == "__main__":
    # Launch the Streamlit app
    app = DentalAIWebApp()
    app.run()

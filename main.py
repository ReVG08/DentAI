"""
Dental AI Diagnostic Assistant
Main application entry point
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path for absolute imports
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from ui.app import DentalAIWebApp

def main():
    app = DentalAIWebApp()
    app.run()

if __name__ == "__main__":
    main()
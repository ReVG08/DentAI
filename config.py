import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
VISION_MODEL = "gpt-4-vision-preview"
COMPLETION_MODEL = "gpt-4"

# Application settings
APP_NAME = "Dental AI Diagnostic Assistant"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CRM Integration settings
DEFAULT_CRM = os.getenv("DEFAULT_CRM", "None")
CRM_API_ENDPOINT = os.getenv("CRM_API_ENDPOINT", "")
CRM_USERNAME = os.getenv("CRM_USERNAME", "")
CRM_PASSWORD = os.getenv("CRM_PASSWORD", "")

# Image processing settings
MAX_IMAGE_SIZE = (1024, 1024)  # Resize large images to this maximum size
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]

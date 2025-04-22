import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
VISION_MODEL = os.getenv("gpt-4o")
COMPLETION_MODEL = os.getenv("gpt-4")

# Application settings
APP_NAME = os.getenv("APP_NAME", "Dental AI Diagnostic Assistant")
DEBUG = os.getenv("DEBUG", "False").strip().lower() == "true"

# CRM Integration settings
DEFAULT_CRM = os.getenv("DEFAULT_CRM", "None")
CRM_API_ENDPOINT = os.getenv("CRM_API_ENDPOINT", "")
CRM_USERNAME = os.getenv("CRM_USERNAME", "")
CRM_PASSWORD = os.getenv("CRM_PASSWORD", "")

# Image processing settings
MAX_IMAGE_SIZE = tuple(map(int, os.getenv("MAX_IMAGE_SIZE", "1024,1024").split(',')))
SUPPORTED_FORMATS = [fmt.strip().lower() for fmt in os.getenv("SUPPORTED_FORMATS", "jpg,jpeg,png").split(",")]
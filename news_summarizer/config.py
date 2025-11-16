"""
Configuration management for the news summarizer application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration from environment variables."""
    
    # Ground News Credentials
    GROUND_NEWS_EMAIL = os.getenv("GROUND_NEWS_EMAIL")
    GROUND_NEWS_PASSWORD = os.getenv("GROUND_NEWS_PASSWORD")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Scraping Settings
    MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", "10"))
    HEADLESS_BROWSER = os.getenv("HEADLESS_BROWSER", "true").lower() == "true"
    
    # Timeout settings
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    ELEMENT_WAIT_TIMEOUT = int(os.getenv("ELEMENT_WAIT_TIMEOUT", "10"))
    
    # Output directory
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./summaries"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        errors = []
        
        if not cls.GROUND_NEWS_EMAIL:
            errors.append("GROUND_NEWS_EMAIL is required")
        if not cls.GROUND_NEWS_PASSWORD:
            errors.append("GROUND_NEWS_PASSWORD is required")
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
            
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        # Create output directory if it doesn't exist
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        return True

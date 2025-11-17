"""
Simple usage example for the News Summarizer.
This script demonstrates how to use the news summarizer.
"""
import os
from pathlib import Path

def create_example_env():
    """Create an example .env file if it doesn't exist."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("Creating .env file from example...")
        example_file = Path(".env.example")
        if example_file.exists():
            # Copy example to .env
            env_file.write_text(example_file.read_text())
            print("\n⚠️  Please edit .env file with your actual credentials:")
            print("   - GROUND_NEWS_EMAIL")
            print("   - GROUND_NEWS_PASSWORD")
            print("   - OPENAI_API_KEY")
            return False
        else:
            print("Error: .env.example not found")
            return False
    return True

def main():
    """Main function to demonstrate usage."""
    print("=" * 80)
    print("News Summarizer - Usage Example")
    print("=" * 80)
    print()
    
    # Check if .env exists
    if not create_example_env():
        print("\nPlease configure your .env file before running the application.")
        return
    
    print("Configuration file found!")
    print()
    print("To run the news summarizer:")
    print("  1. Make sure you have configured .env with your credentials")
    print("  2. Run: python run.py")
    print("  3. Or: python -m news_summarizer.main")
    print()
    print("The application will:")
    print("  - Log into Ground News with your credentials")
    print("  - Scrape the latest articles")
    print("  - Generate AI summaries for each article")
    print("  - Create a daily digest in markdown format")
    print("  - Save the digest to the 'summaries/' directory")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()

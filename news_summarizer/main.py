"""
Main application for news summarizer.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

from .config import Config
from .scraper import GroundNewsScraper
from .summarizer import ArticleSummarizer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('news_summarizer.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    try:
        logger.info("Starting News Summarizer application...")
        
        # Validate configuration
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Initialize components
        scraper = None
        articles = []
        
        try:
            # Create scraper and login
            logger.info("Initializing Ground News scraper...")
            with GroundNewsScraper(
                email=Config.GROUND_NEWS_EMAIL,
                password=Config.GROUND_NEWS_PASSWORD,
                headless=Config.HEADLESS_BROWSER
            ) as scraper:
                
                # Login to Ground News
                logger.info("Logging in to Ground News...")
                if not scraper.login():
                    logger.error("Failed to login to Ground News")
                    sys.exit(1)
                
                # Scrape articles
                logger.info(f"Scraping up to {Config.MAX_ARTICLES} articles...")
                articles = scraper.scrape_articles(max_articles=Config.MAX_ARTICLES)
                
                if not articles:
                    logger.warning("No articles were scraped")
                    return
                
                logger.info(f"Successfully scraped {len(articles)} articles")
                
                # Optionally get full content for articles
                # Note: This can be slow, so we'll skip it for now and summarize based on title/description
                # for article in articles[:5]:  # Limit to first 5 for testing
                #     if article.get('url'):
                #         content = scraper.get_article_content(article['url'])
                #         if content:
                #             article['content'] = content
            
            # Initialize summarizer
            logger.info("Initializing article summarizer...")
            summarizer = ArticleSummarizer(
                api_key=Config.OPENAI_API_KEY,
                model=Config.OPENAI_MODEL
            )
            
            # Summarize articles
            logger.info("Summarizing articles...")
            summarized_articles = summarizer.summarize_articles(articles)
            
            # Create daily digest
            logger.info("Creating daily digest...")
            digest = summarizer.create_daily_digest(summarized_articles)
            
            # Save digest to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Config.OUTPUT_DIR / f"news_digest_{timestamp}.md"
            
            output_file.write_text(digest, encoding='utf-8')
            logger.info(f"Daily digest saved to: {output_file}")
            
            # Print digest to console
            print("\n" + "="*80)
            print(digest)
            print("="*80 + "\n")
            
            logger.info("News Summarizer completed successfully!")
            
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
            sys.exit(0)
            
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

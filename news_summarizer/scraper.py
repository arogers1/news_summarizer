"""
Web scraper for Ground News website with login support.
"""
import logging
import time
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

from .config import Config

logger = logging.getLogger(__name__)


class GroundNewsScraper:
    """Scraper for Ground News articles with login capability."""
    
    def __init__(self, email: str, password: str, headless: bool = True):
        """
        Initialize the Ground News scraper.
        
        Args:
            email: Ground News account email
            password: Ground News account password
            headless: Whether to run browser in headless mode
        """
        self.email = email
        self.password = password
        self.headless = headless
        self.driver = None
        
    def _setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        
    def login(self) -> bool:
        """
        Log in to Ground News.
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info("Navigating to Ground News login page...")
            self.driver.get("https://ground.news/")
            time.sleep(2)
            
            # Look for login/sign in button
            wait = WebDriverWait(self.driver, Config.ELEMENT_WAIT_TIMEOUT)
            
            try:
                # Try to find and click "Sign In" or "Log In" button
                login_button = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
                )
                login_button.click()
                logger.info("Clicked sign in button")
                time.sleep(2)
            except TimeoutException:
                # Maybe already on login page or different button text
                logger.info("Could not find 'Sign in' link, trying alternative methods...")
                try:
                    login_button = self.driver.find_element(By.LINK_TEXT, "Log in")
                    login_button.click()
                    time.sleep(2)
                except NoSuchElementException:
                    # Try going directly to login URL
                    self.driver.get("https://ground.news/login")
                    time.sleep(2)
            
            # Enter email
            email_field = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
            )
            email_field.clear()
            email_field.send_keys(self.email)
            logger.info("Entered email")
            
            # Enter password
            password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password'], input[name='password']")
            password_field.clear()
            password_field.send_keys(self.password)
            logger.info("Entered password")
            
            # Click login button
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            logger.info("Clicked login button")
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful by looking for user-specific elements
            # or checking if we're redirected away from login page
            current_url = self.driver.current_url
            if "login" not in current_url.lower():
                logger.info("Login successful!")
                return True
            else:
                logger.error("Login may have failed - still on login page")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False
    
    def scrape_articles(self, max_articles: int = 10) -> List[Dict[str, str]]:
        """
        Scrape articles from Ground News.
        
        Args:
            max_articles: Maximum number of articles to scrape
            
        Returns:
            List of dictionaries containing article information
        """
        articles = []
        
        try:
            logger.info("Navigating to Ground News homepage...")
            self.driver.get("https://ground.news/")
            time.sleep(3)
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Find article elements (these selectors may need adjustment based on actual site structure)
            article_elements = soup.find_all(['article', 'div'], class_=lambda x: x and ('article' in x.lower() or 'story' in x.lower()))
            
            if not article_elements:
                # Try alternative selectors
                article_elements = soup.find_all('a', href=lambda x: x and '/article/' in x)
            
            logger.info(f"Found {len(article_elements)} potential article elements")
            
            for idx, element in enumerate(article_elements[:max_articles]):
                try:
                    # Extract article information
                    article = {}
                    
                    # Try to find title
                    title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                    if title_elem:
                        article['title'] = title_elem.get_text(strip=True)
                    else:
                        article['title'] = element.get_text(strip=True)[:100]
                    
                    # Try to find link
                    link_elem = element.find('a', href=True)
                    if link_elem:
                        href = link_elem['href']
                        if href.startswith('/'):
                            article['url'] = f"https://ground.news{href}"
                        else:
                            article['url'] = href
                    elif element.name == 'a' and element.get('href'):
                        href = element['href']
                        if href.startswith('/'):
                            article['url'] = f"https://ground.news{href}"
                        else:
                            article['url'] = href
                    else:
                        article['url'] = ""
                    
                    # Try to extract description/snippet
                    desc_elem = element.find('p')
                    if desc_elem:
                        article['description'] = desc_elem.get_text(strip=True)
                    else:
                        article['description'] = ""
                    
                    if article.get('title'):
                        articles.append(article)
                        logger.info(f"Scraped article {idx + 1}: {article['title'][:50]}...")
                        
                except Exception as e:
                    logger.warning(f"Error extracting article {idx}: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(articles)} articles")
            
        except Exception as e:
            logger.error(f"Error scraping articles: {e}")
        
        return articles
    
    def get_article_content(self, url: str) -> Optional[str]:
        """
        Get the full content of an article.
        
        Args:
            url: URL of the article
            
        Returns:
            Article content as string, or None if failed
        """
        try:
            logger.info(f"Fetching article content from {url}")
            self.driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Try to find main content area
            content = soup.find(['article', 'div'], class_=lambda x: x and ('content' in x.lower() or 'article' in x.lower()))
            
            if content:
                # Remove script and style elements
                for script in content(['script', 'style']):
                    script.decompose()
                
                text = content.get_text(separator='\n', strip=True)
                return text
            else:
                # Fallback: get all text from body
                body = soup.find('body')
                if body:
                    for script in body(['script', 'style', 'nav', 'header', 'footer']):
                        script.decompose()
                    return body.get_text(separator='\n', strip=True)
                
            return None
            
        except Exception as e:
            logger.error(f"Error getting article content: {e}")
            return None
    
    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
    
    def __enter__(self):
        """Context manager entry."""
        self._setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

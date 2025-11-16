"""
LLM-based article summarization using OpenAI API.
"""
import logging
from typing import List, Dict
from openai import OpenAI

from .config import Config

logger = logging.getLogger(__name__)


class ArticleSummarizer:
    """Summarizes news articles using OpenAI's LLM."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize the article summarizer.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use for summarization
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def summarize_article(self, article: Dict[str, str]) -> str:
        """
        Summarize a single article.
        
        Args:
            article: Dictionary containing article information (title, url, description, content)
            
        Returns:
            Summary of the article
        """
        try:
            # Prepare the article text for summarization
            article_text = f"Title: {article.get('title', 'No title')}\n\n"
            
            if article.get('description'):
                article_text += f"Description: {article['description']}\n\n"
            
            if article.get('content'):
                article_text += f"Content: {article['content'][:4000]}\n"  # Limit content length
            
            # Create the prompt
            prompt = f"""Please provide a concise summary of the following news article. 
Include the main points and key takeaways in 2-3 sentences.

{article_text}

Summary:"""
            
            # Call OpenAI API
            logger.info(f"Summarizing article: {article.get('title', 'Unknown')[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news articles concisely and accurately."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info("Summary generated successfully")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            return f"Error generating summary: {str(e)}"
    
    def summarize_articles(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Summarize multiple articles.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of articles with summaries added
        """
        summarized_articles = []
        
        for idx, article in enumerate(articles, 1):
            logger.info(f"Processing article {idx}/{len(articles)}")
            summary = self.summarize_article(article)
            
            summarized_article = article.copy()
            summarized_article['summary'] = summary
            summarized_articles.append(summarized_article)
        
        logger.info(f"Completed summarization of {len(summarized_articles)} articles")
        return summarized_articles
    
    def create_daily_digest(self, articles: List[Dict[str, str]]) -> str:
        """
        Create a daily digest from summarized articles.
        
        Args:
            articles: List of articles with summaries
            
        Returns:
            Formatted daily digest as string
        """
        digest = "# Daily News Digest\n\n"
        digest += f"Total Articles: {len(articles)}\n\n"
        digest += "---\n\n"
        
        for idx, article in enumerate(articles, 1):
            digest += f"## {idx}. {article.get('title', 'No title')}\n\n"
            
            if article.get('url'):
                digest += f"**Source:** {article['url']}\n\n"
            
            if article.get('summary'):
                digest += f"**Summary:** {article['summary']}\n\n"
            
            digest += "---\n\n"
        
        return digest

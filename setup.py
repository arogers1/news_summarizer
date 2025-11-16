"""
Setup configuration for the News Summarizer package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="news-summarizer",
    version="1.0.0",
    author="arogers1",
    description="A news scraper and summarizer for Ground News using LLM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arogers1/news_summarizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.15.0",
        "webdriver-manager>=4.0.1",
        "python-dotenv>=1.0.0",
        "openai>=1.3.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "news-summarizer=news_summarizer.main:main",
        ],
    },
)

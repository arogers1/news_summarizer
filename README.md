# News Summarizer

A Python application that scrapes news articles from Ground News using authenticated login and summarizes them using an LLM (Large Language Model) to help you keep up with the news efficiently.

## 🚀 Quick Start

New to the project? Check out our [**Quick Start Guide**](QUICKSTART.md) for step-by-step instructions!

## Features

- 🔐 **Authenticated Scraping**: Logs into Ground News with your credentials
- 🤖 **AI-Powered Summaries**: Uses OpenAI's GPT models to generate concise article summaries
- 📰 **Daily Digest**: Creates a formatted markdown digest of summarized articles
- ⚙️ **Configurable**: Easy configuration via environment variables
- 📝 **Logging**: Comprehensive logging for debugging and monitoring

## Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (for Selenium)
- Ground News account
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arogers1/news_summarizer.git
cd news_summarizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up configuration:
```bash
cp .env.example .env
```

4. Edit `.env` file with your credentials:
```
GROUND_NEWS_EMAIL=your_email@example.com
GROUND_NEWS_PASSWORD=your_password
OPENAI_API_KEY=your_openai_api_key
```

## Configuration

All configuration is done via environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `GROUND_NEWS_EMAIL` | Your Ground News account email | **Required** |
| `GROUND_NEWS_PASSWORD` | Your Ground News account password | **Required** |
| `OPENAI_API_KEY` | Your OpenAI API key | **Required** |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `MAX_ARTICLES` | Maximum number of articles to scrape | `10` |
| `HEADLESS_BROWSER` | Run browser in headless mode | `true` |
| `PAGE_LOAD_TIMEOUT` | Page load timeout in seconds | `30` |
| `ELEMENT_WAIT_TIMEOUT` | Element wait timeout in seconds | `10` |
| `OUTPUT_DIR` | Directory for saving summaries | `./summaries` |

## Usage

Run the application:

```bash
python run.py
```

Or:

```bash
python -m news_summarizer.main
```

The application will:
1. Log into Ground News with your credentials
2. Scrape the latest articles (up to MAX_ARTICLES)
3. Generate AI summaries for each article
4. Create a daily digest in markdown format
5. Save the digest to the `summaries/` directory
6. Print the digest to the console

## Output

The application generates a markdown file with the following format:

```markdown
# Daily News Digest

Total Articles: 10

---

## 1. Article Title

**Source:** https://ground.news/article/...

**Summary:** AI-generated summary of the article...

---
```

Output files are saved in the `summaries/` directory with timestamps:
- `summaries/news_digest_20231216_143022.md`

## Logging

Logs are written to both:
- Console (stdout)
- `news_summarizer.log` file

## Project Structure

```
news_summarizer/
├── news_summarizer/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── scraper.py           # Ground News scraper
│   ├── summarizer.py        # LLM summarization
│   └── main.py              # Main application
├── run.py                   # CLI entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## How It Works

1. **Configuration**: Loads settings from environment variables
2. **Web Scraping**: Uses Selenium to:
   - Navigate to Ground News
   - Log in with provided credentials
   - Scrape article titles, descriptions, and URLs
3. **Summarization**: Uses OpenAI API to:
   - Generate concise summaries for each article
   - Create a formatted daily digest
4. **Output**: Saves results to markdown file and displays in console

## Troubleshooting

**📖 For comprehensive troubleshooting, see our [Troubleshooting Guide](TROUBLESHOOTING.md)**

### Quick Fixes

#### Login Issues
- Verify your Ground News credentials are correct
- Check if Ground News has changed their login page structure
- Try running with `HEADLESS_BROWSER=false` to see browser interactions

#### Scraping Issues
- Ground News may have updated their HTML structure
- Check the logs for specific error messages
- Ensure you have a stable internet connection

#### Scraping Issues
- Ground News may have updated their HTML structure
- Check the logs for specific error messages
- Ensure you have a stable internet connection

#### API Issues
- Verify your OpenAI API key is valid
- Check your OpenAI API usage limits
- Ensure you have sufficient credits

#### Browser Issues
- Make sure Chrome/Chromium is installed
- The webdriver-manager will auto-download chromedriver
- On Linux, you may need to install: `apt-get install chromium-browser`

## Scheduling

To run the news summarizer automatically on a schedule, you can use:

### Linux/Mac (cron)
```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/news_summarizer && /usr/bin/python3 run.py
```

### Windows (Task Scheduler)
Create a task that runs `python run.py` on your desired schedule.

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys and passwords secure
- The `.env` file is included in `.gitignore`

## Important Notes

- **Ground News Structure**: The scraper uses CSS selectors to find articles on the Ground News website. If Ground News changes their website structure, the scraper may need updates.
- **Rate Limiting**: Be mindful of Ground News's terms of service and avoid excessive scraping that could overload their servers.
- **OpenAI Costs**: Each article summary uses OpenAI API credits. Monitor your usage to avoid unexpected costs.
- **Two-Factor Authentication**: Currently not supported. If your Ground News account requires 2FA, the login will fail.

## Future Enhancements

- Email delivery of daily digest
- Support for multiple news sources
- Customizable summary formats
- Article filtering by topics/categories
- Database storage of articles and summaries

## License

This project is provided as-is for personal use.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

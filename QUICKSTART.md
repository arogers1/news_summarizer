# Quick Start Guide

This guide will help you get the News Summarizer up and running quickly.

## Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher installed
- A Ground News account ([Sign up here](https://ground.news/))
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/arogers1/news_summarizer.git
cd news_summarizer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your Credentials
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite text editor
nano .env  # or vim, code, etc.
```

Update these required fields in `.env`:
```bash
GROUND_NEWS_EMAIL=your_email@example.com
GROUND_NEWS_PASSWORD=your_password
OPENAI_API_KEY=sk-your-api-key-here
```

### 4. Run the Application
```bash
python run.py
```

## What Happens Next?

When you run the application, it will:

1. ✅ Validate your configuration
2. 🌐 Open a browser and log into Ground News
3. 📰 Scrape the latest news articles
4. 🤖 Generate AI summaries using OpenAI
5. 💾 Save a daily digest to `summaries/` directory
6. 📊 Display the digest in your terminal

## Example Output

```markdown
# Daily News Digest

Total Articles: 10

---

## 1. Major Development in Technology Sector

**Source:** https://ground.news/article/...

**Summary:** A groundbreaking announcement from leading tech companies 
reveals new innovations in AI technology that could reshape the industry...

---
```

## Troubleshooting

### "ModuleNotFoundError"
Make sure you installed dependencies: `pip install -r requirements.txt`

### "Configuration errors"
Check that your `.env` file has valid credentials for all required fields.

### "Login failed"
- Verify your Ground News credentials are correct
- Try logging in manually to ensure your account works
- Check if Ground News requires 2FA (currently not supported)

### Browser issues
On Linux, you may need to install Chrome/Chromium:
```bash
sudo apt-get update
sudo apt-get install chromium-browser
```

## Advanced Usage

### Customize Number of Articles
Edit `.env` and change:
```bash
MAX_ARTICLES=20  # Default is 10
```

### Run in Visible Browser Mode
Edit `.env` and change:
```bash
HEADLESS_BROWSER=false
```
This lets you see what the scraper is doing.

### Schedule Daily Runs

#### Linux/Mac (cron)
```bash
crontab -e
# Add this line to run daily at 8 AM:
0 8 * * * cd /path/to/news_summarizer && /usr/bin/python3 run.py
```

#### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create a new task
3. Set trigger to daily at your preferred time
4. Set action to run `python.exe` with argument `run.py`
5. Set start in directory to your project folder

## Next Steps

- Check the `summaries/` folder for your daily digest
- Customize the `.env` file for your preferences
- Set up automated scheduling
- Read the full README for more details

## Getting Help

If you encounter issues:
1. Check the `news_summarizer.log` file for errors
2. Review the troubleshooting section above
3. Open an issue on GitHub with details about your problem

Happy news reading! 📰✨

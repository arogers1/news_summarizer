# Troubleshooting Guide

This guide covers common issues and their solutions.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Scraping Issues](#scraping-issues)
- [API Issues](#api-issues)
- [Browser Issues](#browser-issues)
- [General Issues](#general-issues)

## Installation Issues

### "ModuleNotFoundError: No module named 'X'"

**Problem**: Python can't find required packages.

**Solution**:
```bash
pip install -r requirements.txt
```

If that doesn't work, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### "Permission denied" when installing packages

**Problem**: Insufficient permissions to install packages.

**Solution**:
```bash
# Use --user flag
pip install -r requirements.txt --user

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration Issues

### "Configuration errors: GROUND_NEWS_EMAIL is required"

**Problem**: Missing .env file or empty configuration values.

**Solution**:
1. Create .env file from example:
   ```bash
   cp .env.example .env
   ```
2. Edit .env and fill in your actual credentials
3. Make sure there are no quotes around values in .env

### "GROUND_NEWS_EMAIL appears to be a placeholder value"

**Problem**: You're using the example placeholder values.

**Solution**:
Edit `.env` and replace placeholder values with your actual credentials:
```bash
GROUND_NEWS_EMAIL=your_actual_email@example.com
GROUND_NEWS_PASSWORD=your_actual_password
OPENAI_API_KEY=sk-your-actual-api-key
```

## Scraping Issues

### "Failed to login to Ground News"

**Possible causes and solutions**:

1. **Incorrect credentials**
   - Verify your email and password are correct
   - Try logging in manually at https://ground.news/

2. **Two-factor authentication (2FA)**
   - The scraper doesn't support 2FA
   - Disable 2FA on your Ground News account if possible

3. **Website structure changed**
   - Ground News may have updated their login page
   - Check logs for specific error messages
   - The scraper may need updating

4. **Network issues**
   - Check your internet connection
   - Try with HEADLESS_BROWSER=false to see what's happening

### "No articles were scraped"

**Possible causes**:

1. **Login failed** - Check if login was successful in logs
2. **Website structure changed** - Ground News may have updated their HTML
3. **Content not loading** - Try increasing timeouts in .env:
   ```bash
   PAGE_LOAD_TIMEOUT=60
   ELEMENT_WAIT_TIMEOUT=20
   ```

### "TimeoutException" errors

**Problem**: Browser can't find elements or pages take too long to load.

**Solution**:
Increase timeout values in `.env`:
```bash
PAGE_LOAD_TIMEOUT=60
ELEMENT_WAIT_TIMEOUT=20
```

## API Issues

### "AuthenticationError" from OpenAI

**Problem**: Invalid or missing API key.

**Solution**:
1. Verify your API key at https://platform.openai.com/api-keys
2. Make sure the key starts with `sk-`
3. Update OPENAI_API_KEY in .env
4. Check if you have spaces or quotes around the key (remove them)

### "RateLimitError" from OpenAI

**Problem**: You've exceeded OpenAI's rate limits.

**Solution**:
1. Reduce MAX_ARTICLES in .env
2. Wait before running again
3. Upgrade your OpenAI plan for higher limits

### "InsufficientQuotaError" from OpenAI

**Problem**: No credits remaining on your OpenAI account.

**Solution**:
1. Check your usage at https://platform.openai.com/usage
2. Add credits to your OpenAI account
3. Verify billing is set up correctly

## Browser Issues

### "ChromeDriver not found" or "WebDriver exception"

**Problem**: Selenium can't find or start Chrome/ChromeDriver.

**Solution**:

On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install chromium-browser
```

On macOS:
```bash
brew install --cask google-chrome
```

On Windows:
- Install Google Chrome from https://www.google.com/chrome/

### "Session not created" error

**Problem**: ChromeDriver version mismatch.

**Solution**:
The webdriver-manager should auto-download the correct version. If it doesn't work:
```bash
pip install --upgrade webdriver-manager
```

### Browser opens but crashes immediately

**Problem**: Headless mode issues.

**Solution**:
Try running in non-headless mode to debug:
```bash
# In .env
HEADLESS_BROWSER=false
```

## General Issues

### Slow performance

**Causes and solutions**:

1. **Too many articles** - Reduce MAX_ARTICLES in .env
2. **Slow internet** - Increase timeouts
3. **API delays** - OpenAI API can be slow during peak times

### "Permission denied" when saving files

**Problem**: Can't write to summaries directory.

**Solution**:
```bash
# Create directory manually
mkdir summaries
chmod 755 summaries

# Or change output directory in .env
OUTPUT_DIR=./my_summaries
```

### Logs show errors but application continues

**Problem**: Non-critical errors are logged as warnings.

**Solution**:
- Check `news_summarizer.log` for details
- If articles are still being scraped and summarized, the app is working
- Some errors (like failing to extract description) are expected

## Getting More Help

If none of these solutions work:

1. **Check the logs**
   - Look at `news_summarizer.log` for detailed error messages
   - Run with `HEADLESS_BROWSER=false` to see browser behavior

2. **Search existing issues**
   - Check [GitHub Issues](https://github.com/arogers1/news_summarizer/issues)
   - Someone may have had the same problem

3. **Create a new issue**
   - Include the error message
   - Include relevant logs
   - Describe what you've already tried
   - Include your environment (OS, Python version)

4. **Enable debug logging**
   ```python
   # In news_summarizer/main.py, change logging level to DEBUG
   logging.basicConfig(
       level=logging.DEBUG,  # Changed from INFO
       ...
   )
   ```

## Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `ModuleNotFoundError` | Missing package | `pip install -r requirements.txt` |
| `ValueError: Configuration errors` | Missing .env values | Edit .env with actual credentials |
| `AuthenticationError` | Invalid API key | Check OpenAI API key |
| `TimeoutException` | Slow loading or wrong selectors | Increase timeouts or check site structure |
| `WebDriverException` | Chrome/ChromeDriver issue | Install Chrome or update webdriver-manager |
| `RateLimitError` | Too many API calls | Reduce MAX_ARTICLES or wait |

---

Still stuck? Don't hesitate to [open an issue](https://github.com/arogers1/news_summarizer/issues/new)!

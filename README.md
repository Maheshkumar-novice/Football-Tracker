# Football Matches Tracker

A lightweight Flask web application that displays recent football match results from the last 7 days across the top 5 European leagues plus the Champions League.

## Features

### Phase 1 - Core Functionality
- **Recent Match Results**: Displays matches from the last 7 days
- **6 Major Competitions**: Premier League, La Liga, Bundesliga, Serie A, Ligue 1, and Champions League
- **Auto-Refresh**: Automatically updates every 30 minutes
- **Smart Caching**: Caches API results for 30 minutes to stay within free-tier limits
- **Clean UI**: Minimal, mobile-friendly interface
- **Click-to-Search**: Click any match to search for details on Google
- **Error Handling**: Gracefully falls back to cached data on API failures

### Phase 2 - AI-Powered Features
- **AI-Generated Summaries**: On-demand AI summaries of match results using Anthropic's Claude
- **Sports Journalist Style**: Dramatic, headline-style summaries covering big wins, losses, and notable performances
- **Cost Control**: Summary generation limited to once per data refresh to manage API costs
- **Smart Auto-Refresh**: When summary is visible, shows reload banner instead of auto-refreshing

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Source**: [Football-Data.org API](https://www.football-data.org/) (Free Tier)
- **Package Manager**: uv

## Supported Competitions

| Competition      | Code |
| ---------------- | ---- |
| Premier League   | PL   |
| La Liga          | PD   |
| Bundesliga       | BL1  |
| Serie A          | SA   |
| Ligue 1          | FL1  |
| Champions League | CL   |

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Football-Data.org API key (free tier)
- Anthropic API key (for AI summary generation)

## Setup Instructions

### 1. Get Your API Keys

**Football-Data.org API:**
1. Visit [Football-Data.org](https://www.football-data.org/)
2. Register for a free account
3. Get your API key from the dashboard

**Anthropic API:**
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Get your API key from the API Keys section

### 2. Clone and Setup

```bash
# Navigate to project directory
cd football-tracker

# The .env file should already exist with your API keys
# If not, create it:
cat > .env << EOF
FOOTBALL_API_KEY=your_football_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-20250514
ANTHROPIC_TIMEOUT_SECONDS=30
EOF
```

### 3. Install Dependencies

```bash
# Install dependencies using uv
uv sync
```

This will:
- Create a virtual environment at `.venv/`
- Install Flask, python-dotenv, requests, and anthropic

### 4. Run the Application

```bash
# Run with uv
uv run python app.py

# Or activate the virtual environment and run directly
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python app.py
```

The application will start on `http://localhost:5000`

## Configuration

You can customize the application using environment variables in your `.env` file:

| Variable                     | Description                                         | Default                    | Required |
| ---------------------------- | --------------------------------------------------- | -------------------------- | -------- |
| `FOOTBALL_API_KEY`           | Your Football-Data.org API key                      | -                          | Yes      |
| `ANTHROPIC_API_KEY`          | Your Anthropic API key for AI summaries             | -                          | Yes      |
| `ANTHROPIC_MODEL`            | Anthropic model to use                              | claude-sonnet-4-20250514   | No       |
| `ANTHROPIC_TIMEOUT_SECONDS`  | Timeout for Anthropic API calls                     | 30                         | No       |
| `CACHE_TTL`                  | Cache time-to-live in seconds                       | 1800                       | No       |
| `LOG_LEVEL`                  | Logging level (DEBUG, INFO, WARNING, etc)           | INFO                       | No       |

Example `.env` file:
```bash
FOOTBALL_API_KEY=your_football_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-20250514
ANTHROPIC_TIMEOUT_SECONDS=30
CACHE_TTL=1800
LOG_LEVEL=INFO
```

## Project Structure

```
football-tracker/
├── app.py                 # Main Flask application
├── ai_summary.py          # AI-powered summary generation (Phase 2)
├── cache.py               # In-memory caching with TTL
├── config.py              # Configuration management
├── data_processor.py      # Data normalization
├── data_service.py        # Service layer orchestrating API and cache
├── football_api.py        # Football-Data.org API client
├── logging_config.py      # Logging configuration
├── templates/
│   └── index.html        # Main HTML template with AI summary UI
├── static/
│   ├── styles.css        # CSS styling
│   └── script.js         # JavaScript for auto-refresh and AI summaries
├── .env                  # Environment variables (not in git)
├── .gitignore            # Git ignore rules
├── pyproject.toml        # Project dependencies
└── README.md             # This file
```

## Using AI Summaries

1. **Open the application** in your browser at `http://localhost:5000`
2. **Click "Generate Summary"** button below the header
3. Wait a few seconds while AI analyzes the matches
4. **View the summary** - dramatic headlines about recent results
5. The button will disable after use (cost control)
6. **Refresh the page** to enable summary generation again with new data

**Notes:**
- Summary generation requires both Football-Data.org AND Anthropic API keys
- Summaries are ephemeral and not cached
- Button can only be used once per data refresh (every 30 minutes)
- Full prompt and response are logged to `app.log` for debugging

## API Rate Limits

The free tier of Football-Data.org has the following limits:
- **10 API calls per minute**
- **Scores and schedules are delayed**
- **12 competitions available**

The application caches results for 30 minutes to stay well within these limits.

## Logging

Logs are written to:
- **Console**: Concise format for development
- **app.log**: Detailed format with module names and line numbers

Log level can be controlled via the `LOG_LEVEL` environment variable.

## Troubleshooting

### "FOOTBALL_API_KEY environment variable is required"
- Make sure your `.env` file exists and contains valid API keys
- Check that the `.env` file is in the same directory as `app.py`
- Both `FOOTBALL_API_KEY` and `ANTHROPIC_API_KEY` are required

### No matches displayed
- The app only shows matches from the last 7 days
- If there are no recent matches, the page will show "No matches found"
- Check `app.log` for API errors

### Summary generation fails
- Verify `ANTHROPIC_API_KEY` is set correctly in `.env`
- Check `app.log` for detailed error messages
- Ensure you have internet connectivity
- Try refreshing the page and generating again

### API errors
- Verify your API key is valid
- Check that you haven't exceeded the rate limit (10 calls/minute)
- The app will fall back to cached data if available

## Development

To run in development mode with auto-reload:

```bash
uv run python app.py
```

Flask debug mode is enabled by default in `app.py`.

## Future Enhancements

Potential features for future versions:
- Dark mode
- More competitions
- Live match updates via WebSockets
- Filtering and search
- Team logos
- Match details modal
- Deployment to cloud platform

## License

This project is for educational purposes. Please respect Football-Data.org's terms of service and rate limits.

## Credits

- Data provided by [Football-Data.org](https://www.football-data.org/)
- Built with Flask and Python

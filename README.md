# Football Matches Tracker

A lightweight Flask web application that displays recent football match results from the last 7 days across the top 5 European leagues.

## Features

- **Recent Match Results**: Displays matches from the last 7 days
- **5 Major Leagues**: Premier League, La Liga, Bundesliga, Serie A, and Ligue 1
- **Auto-Refresh**: Automatically updates every 30 minutes
- **Smart Caching**: Caches API results for 30 minutes to stay within free-tier limits
- **Clean UI**: Minimal, mobile-friendly interface
- **Click-to-Search**: Click any match to search for details on Google
- **Error Handling**: Gracefully falls back to cached data on API failures

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Source**: [Football-Data.org API](https://www.football-data.org/) (Free Tier)
- **Package Manager**: uv

## Supported Competitions

| Competition    | Code |
| -------------- | ---- |
| Premier League | PL   |
| La Liga        | PD   |
| Bundesliga     | BL1  |
| Serie A        | SA   |
| Ligue 1        | FL1  |

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Football-Data.org API key (free tier)

## Setup Instructions

### 1. Get Your API Key

1. Visit [Football-Data.org](https://www.football-data.org/)
2. Register for a free account
3. Get your API key from the dashboard

### 2. Clone and Setup

```bash
# Navigate to project directory
cd football-tracker

# The .env file should already exist with your API key
# If not, create it:
echo "FOOTBALL_API_KEY=your_api_key_here" > .env
```

### 3. Install Dependencies

```bash
# Install dependencies using uv
uv sync
```

This will:
- Create a virtual environment at `.venv/`
- Install Flask, python-dotenv, and requests

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

| Variable           | Description                              | Default |
| ------------------ | ---------------------------------------- | ------- |
| `FOOTBALL_API_KEY` | Your Football-Data.org API key (required)| -       |
| `CACHE_TTL`        | Cache time-to-live in seconds            | 1800    |
| `LOG_LEVEL`        | Logging level (DEBUG, INFO, WARNING, etc)| INFO    |

Example `.env` file:
```bash
FOOTBALL_API_KEY=your_api_key_here
CACHE_TTL=1800
LOG_LEVEL=INFO
```

## Project Structure

```
football-tracker/
├── app.py                 # Main Flask application
├── cache.py               # In-memory caching with TTL
├── config.py              # Configuration management
├── data_processor.py      # Data normalization
├── data_service.py        # Service layer orchestrating API and cache
├── football_api.py        # Football-Data.org API client
├── logging_config.py      # Logging configuration
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── styles.css        # CSS styling
│   └── script.js         # JavaScript for auto-refresh
├── .env                  # Environment variables (not in git)
├── .gitignore            # Git ignore rules
├── pyproject.toml        # Project dependencies
└── README.md             # This file
```

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
- Make sure your `.env` file exists and contains a valid API key
- Check that the `.env` file is in the same directory as `app.py`

### No matches displayed
- The app only shows matches from the last 7 days
- If there are no recent matches, the page will show "No matches found"
- Check `app.log` for API errors

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

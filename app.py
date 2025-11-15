"""Flask application for Football Matches Tracker."""

import logging
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
from logging_config import setup_logging
from config import Config
from data_service import MatchDataService

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Initialize data service
data_service = MatchDataService(api_key=Config.API_KEY, cache_ttl=Config.CACHE_TTL)

logger.info("Football Matches Tracker application starting...")
logger.info(f"Cache TTL configured: {Config.CACHE_TTL} seconds")


@app.route('/')
def index():
    """Display the main page with match results."""
    logger.info("Index route accessed")
    error = False

    # Try to refresh data (will use cache if still valid)
    try:
        data_service.refresh_data()
    except Exception as e:
        logger.error(f"Error refreshing data: {e}", exc_info=True)
        error = True

    # Get match data (from cache if available)
    competitions = data_service.get_matches()

    # Calculate relative time for "last updated"
    age_seconds = data_service.cache.get_age_seconds()
    if age_seconds is not None:
        if age_seconds < 60:
            last_updated = "Just now"
        elif age_seconds < 3600:
            minutes = int(age_seconds / 60)
            last_updated = f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif age_seconds < 86400:
            hours = int(age_seconds / 3600)
            last_updated = f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = int(age_seconds / 86400)
            last_updated = f"{days} day{'s' if days != 1 else ''} ago"
    else:
        last_updated = "Never"

    logger.info(f"Rendering page with {len(competitions)} competitions, last updated: {last_updated}")

    return render_template(
        'index.html',
        competitions=competitions,
        last_updated=last_updated,
        error=error
    )


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("Starting Flask development server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

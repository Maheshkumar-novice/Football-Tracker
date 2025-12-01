"""Flask application for Football Matches Tracker."""

import logging
import atexit
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
from logging_config import setup_logging
from config import Config
from data_service import MatchDataService
# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Initialize data service
data_service = MatchDataService(api_key=Config.API_KEY)

# Initialize Scheduler
scheduler = BackgroundScheduler()

def scheduled_refresh():
    """Background task to refresh data."""
    logger.info("Starting scheduled data refresh...")
    try:
        data_service.refresh_data()
        logger.info("Data refresh completed successfully")
    except Exception as e:
        logger.error(f"Error in scheduled refresh: {e}")

scheduler.add_job(func=scheduled_refresh, trigger="interval", minutes=30)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

logger.info("Football Matches Tracker application starting...")

# Startup Check: Ensure data exists
if data_service.db.is_empty():
    logger.info("Database is empty. Performing initial data fetch (this may take a minute)...")
    scheduled_refresh()
else:
    logger.info("Database has data. Skipping initial fetch.")


@app.route('/')
def index():
    """Display the main page with match results."""
    logger.info("Index route accessed")

    # Get data from database
    competitions = data_service.get_matches()
    scorers = data_service.get_scorers()
    standings = data_service.get_standings()

    # Calculate relative time for "last updated"
    last_updated = "Recently"

    logger.info(f"Rendering page with {len(competitions)} competitions")

    return render_template(
        'index.html',
        competitions=competitions,
        scorers=scorers,
        standings=standings,
        last_updated=last_updated,
        error=None
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
    logger.info(f"Starting Flask server on port {Config.PORT} (Debug: {Config.DEBUG})...")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=Config.PORT, use_reloader=False)

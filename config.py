"""Configuration management for the Football Matches Tracker application."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class that loads settings from environment variables."""

    # Required: API key for Football-Data.org
    API_KEY = os.getenv('FOOTBALL_API_KEY')

    # Optional: Cache TTL in seconds (default 30 minutes)
    CACHE_TTL = int(os.getenv('CACHE_TTL', '1800'))

    # Optional: Log level (default INFO)
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls):
        """
        Validate that all required configuration is present.

        Raises:
            ValueError: If required configuration is missing.
        """
        if not cls.API_KEY:
            raise ValueError(
                "FOOTBALL_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )


# Validate configuration on import
Config.validate()

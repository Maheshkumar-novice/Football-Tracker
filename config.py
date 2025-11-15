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

    # Required: API key for Anthropic
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Optional: Anthropic model (default: claude-sonnet-4-20250514)
    ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-20250514')

    # Optional: Anthropic API timeout in seconds (default: 30)
    ANTHROPIC_TIMEOUT_SECONDS = int(os.getenv('ANTHROPIC_TIMEOUT_SECONDS', '30'))

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

        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required. "
                "Please set it in your .env file or environment. "
                "Get your API key from https://console.anthropic.com/"
            )


# Validate configuration on import
Config.validate()

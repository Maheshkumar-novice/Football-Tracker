"""Logging configuration for the Football Matches Tracker application."""

import logging
import os
import sys


def setup_logging():
    """
    Configure logging for the application.

    Sets up both console and file logging with appropriate formatters.
    Log level can be controlled via LOG_LEVEL environment variable.
    """
    # Get log level from environment or default to INFO
    log_level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear any existing handlers
    root_logger.handlers.clear()

    # Console handler - more concise for development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler - more detailed for debugging
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Log the setup completion
    root_logger.info(f"Logging configured with level: {log_level_name}")

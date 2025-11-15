"""In-memory caching for match data with TTL (Time To Live)."""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MatchCache:
    """In-memory cache for match data with time-to-live validation."""

    def __init__(self, ttl_seconds=1800):
        """
        Initialize the cache.

        Args:
            ttl_seconds: Time-to-live in seconds (default: 1800 = 30 minutes)
        """
        self.ttl_seconds = ttl_seconds
        self.last_updated = None
        self.competitions = None
        logger.info(f"MatchCache initialized with TTL: {ttl_seconds} seconds")

    def is_valid(self):
        """
        Check if the cache is valid (exists and hasn't exceeded TTL).

        Returns:
            bool: True if cache is valid, False otherwise
        """
        if self.last_updated is None or self.competitions is None:
            return False

        age_seconds = self.get_age_seconds()
        if age_seconds is None:
            return False

        return age_seconds < self.ttl_seconds

    def get_age_seconds(self):
        """
        Get the age of the cache in seconds.

        Returns:
            float: Age in seconds, or None if cache is empty
        """
        if self.last_updated is None:
            return None

        now = datetime.utcnow()
        age = (now - self.last_updated).total_seconds()
        return age

    def set_data(self, competitions_dict, timestamp=None):
        """
        Store match data in cache.

        Only updates if the new timestamp is newer than existing, or cache is empty.

        Args:
            competitions_dict: Dict of matches grouped by competition code
            timestamp: UTC datetime of the data (default: current time)

        Returns:
            bool: True if cache was updated, False if skipped
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        # Only update if cache is empty or new data is newer
        if self.last_updated is not None and timestamp <= self.last_updated:
            logger.info(
                f"Skipping cache update: new data ({timestamp}) is not newer "
                f"than existing ({self.last_updated})"
            )
            return False

        self.competitions = competitions_dict
        self.last_updated = timestamp

        # Count total matches for logging
        total_matches = sum(len(matches) for matches in competitions_dict.values())
        logger.info(
            f"Cache updated with {len(competitions_dict)} competitions, "
            f"{total_matches} total matches at {timestamp}"
        )
        return True

    def get_data(self):
        """
        Retrieve cached match data.

        Returns:
            dict: Cached competitions dict, or None if cache is empty or invalid
        """
        if not self.is_valid():
            if self.competitions is None:
                logger.debug("Cache miss: no data available")
            else:
                logger.debug(f"Cache miss: data expired (age: {self.get_age_seconds():.1f}s)")
            return None

        logger.debug(f"Cache hit: data age {self.get_age_seconds():.1f}s")
        return self.competitions

    def clear(self):
        """Reset the cache to empty state."""
        self.last_updated = None
        self.competitions = None
        logger.info("Cache cleared")

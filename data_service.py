"""Data service orchestrating API calls and cache updates."""

import logging
from datetime import datetime
from football_api import FootballAPIClient
from cache import MatchCache
from data_processor import normalize_match, group_by_competition

logger = logging.getLogger(__name__)


class MatchDataService:
    """Service layer that coordinates API client, data processing, and caching."""

    # Competition codes for the 5 supported leagues
    COMPETITION_CODES = ["PL", "PD", "BL1", "SA", "FL1"]

    def __init__(self, api_key, cache_ttl=1800):
        """
        Initialize the data service.

        Args:
            api_key: API key for Football-Data.org
            cache_ttl: Cache time-to-live in seconds (default: 1800 = 30 minutes)
        """
        self.api_client = FootballAPIClient(api_key)
        self.cache = MatchCache(ttl_seconds=cache_ttl)
        logger.info("MatchDataService initialized")

    def refresh_data(self):
        """
        Refresh match data from API if cache is expired.

        If cache is still valid, this method does nothing (cache hit).
        If cache is expired or empty, fetches fresh data from API.

        Returns:
            bool: True if refresh was successful, False otherwise
        """
        # Check if cache is still valid
        if self.cache.is_valid():
            logger.info("Cache is still valid, skipping API refresh")
            return True

        logger.info("Cache expired or empty, fetching fresh data from API...")

        all_matches = []
        successful_fetches = 0
        failed_fetches = 0

        # Fetch data for each competition
        for comp_code in self.COMPETITION_CODES:
            try:
                # Fetch recent matches (last 7 days = 168 hours)
                response = self.api_client.fetch_recent_matches(comp_code, hours=168)

                if response is None:
                    logger.warning(f"Failed to fetch data for {comp_code}")
                    failed_fetches += 1
                    continue

                # Extract matches from response
                matches = response.get('matches', [])
                logger.info(f"Fetched {len(matches)} matches for {comp_code}")

                # Normalize each match
                for match_data in matches:
                    normalized = normalize_match(
                        match_data,
                        competition_code=comp_code,
                        competition_name=response.get('competition', {}).get('name', comp_code)
                    )
                    if normalized:
                        all_matches.append(normalized)

                successful_fetches += 1

            except Exception as e:
                logger.error(f"Error processing {comp_code}: {e}")
                failed_fetches += 1

        # Check if we got any data
        if successful_fetches == 0:
            logger.error("Failed to fetch data from all competitions")
            return False

        logger.info(
            f"Successfully fetched {successful_fetches}/{len(self.COMPETITION_CODES)} competitions, "
            f"{len(all_matches)} total matches"
        )

        # Group matches by competition
        grouped_matches = group_by_competition(all_matches)

        # Update cache
        timestamp = datetime.utcnow()
        self.cache.set_data(grouped_matches, timestamp)

        return True

    def get_matches(self):
        """
        Get match data (from cache if available).

        Returns:
            dict: Matches grouped by competition code, or empty dict if no data
        """
        data = self.cache.get_data()
        if data is None:
            logger.warning("No cached data available")
            return {}

        return data

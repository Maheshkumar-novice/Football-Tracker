"""API client for Football-Data.org API."""

import logging
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)


class FootballAPIClient:
    """Client for interacting with the Football-Data.org API."""

    # Base URL for the API
    BASE_URL = "https://api.football-data.org/v4"

    # Competition codes for the 6 supported competitions (Free tier)
    COMPETITION_CODES = ["PL", "PD", "BL1", "SA", "FL1", "CL"]

    def __init__(self, api_key):
        """
        Initialize the API client.

        Args:
            api_key: API key for Football-Data.org (X-Auth-Token header)
        """
        self.api_key = api_key
        self.headers = {
            "X-Auth-Token": api_key
        }

    def fetch_competition_matches(self, competition_code, params=None, retry=True):
        """
        Fetch matches for a specific competition.

        Args:
            competition_code: Competition code (e.g., 'PL', 'PD', 'BL1', 'SA', 'FL1')
            params: Optional query parameters (e.g., dateFrom, dateTo)
            retry: Whether to retry on failure (default: True)

        Returns:
            dict: JSON response from API, or None on failure
        """
        url = f"{self.BASE_URL}/competitions/{competition_code}/matches"

        try:
            logger.info(f"Fetching matches for competition: {competition_code}")
            if params:
                logger.debug(f"Query parameters: {params}")

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10  # 10 second timeout
            )
            response.raise_for_status()

            logger.info(
                f"Successfully fetched matches for {competition_code} "
                f"(status: {response.status_code})"
            )
            return response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logger.warning(f"Network error fetching {competition_code}: {e}")
            if retry:
                logger.info(f"Retrying {competition_code} after 2 seconds...")
                import time
                time.sleep(2)
                return self.fetch_competition_matches(competition_code, params, retry=False)
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"HTTP error fetching {competition_code}: {e.response.status_code} - {e}"
            )
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {competition_code}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {competition_code}: {e}")
            return None

    def fetch_recent_matches(self, competition_code, hours=168):
        """
        Fetch recent matches for a competition within a time range.

        Args:
            competition_code: Competition code (e.g., 'PL', 'PD', 'BL1', 'SA', 'FL1')
            hours: Number of hours to look back from now (default: 168 = 7 days)

        Returns:
            dict: JSON response from API, or None on failure
        """
        # Calculate date range in UTC
        now = datetime.utcnow()
        date_from = now - timedelta(hours=hours)

        # Format dates as YYYY-MM-DD (API expects date only, not timestamp)
        date_from_str = date_from.strftime("%Y-%m-%d")
        date_to_str = now.strftime("%Y-%m-%d")

        logger.info(
            f"Fetching recent matches for {competition_code} "
            f"from {date_from_str} to {date_to_str}"
        )

        # Build query parameters
        params = {
            "dateFrom": date_from_str,
            "dateTo": date_to_str
        }

        # Use the existing fetch method with date parameters
        return self.fetch_competition_matches(competition_code, params=params)

    def fetch_top_scorers(self, competition_code, limit=10):
        """
        Fetch top scorers for a specific competition.

        Args:
            competition_code: Competition code (e.g., 'PL', 'PD', 'BL1', 'SA', 'FL1', 'CL')
            limit: Number of top scorers to fetch (default: 10)

        Returns:
            dict: JSON response from API, or None on failure
        """
        url = f"{self.BASE_URL}/competitions/{competition_code}/scorers"
        params = {"limit": limit}

        try:
            logger.info(f"Fetching top {limit} scorers for {competition_code}")
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Successfully fetched scorers for {competition_code}")
            return response.json()

        except Exception as e:
            logger.error(f"Error fetching scorers for {competition_code}: {e}")
            return None

    def fetch_standings(self, competition_code):
        """
        Fetch standings for a specific competition.

        Args:
            competition_code: Competition code (e.g., 'PL', 'PD', 'BL1', 'SA', 'FL1', 'CL')

        Returns:
            dict: JSON response from API, or None on failure
        """
        url = f"{self.BASE_URL}/competitions/{competition_code}/standings"

        try:
            logger.info(f"Fetching standings for {competition_code}")
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Successfully fetched standings for {competition_code}")
            return response.json()

        except Exception as e:
            logger.error(f"Error fetching standings for {competition_code}: {e}")
            return None

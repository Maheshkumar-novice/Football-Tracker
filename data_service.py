"""Data service orchestrating API calls and database storage."""

import logging
import time
from datetime import datetime
from football_api import FootballAPIClient
from db_manager import DatabaseManager
from data_processor import normalize_match

logger = logging.getLogger(__name__)


class MatchDataService:
    """Service layer that coordinates API client, data processing, and database storage."""

    # Competition codes for the 6 supported competitions
    COMPETITION_CODES = ["PL", "PD", "BL1", "SA", "FL1", "CL"]

    def __init__(self, api_key):
        """
        Initialize the data service.

        Args:
            api_key: API key for Football-Data.org
        """
        self.api_client = FootballAPIClient(api_key)
        self.db = DatabaseManager()
        logger.info("MatchDataService initialized with SQLite storage")

    def refresh_data(self):
        """
        Fetch fresh data from API and update the database.
        
        This method fetches matches, scorers, and standings for all competitions
        and stores them in the SQLite database.
        
        Returns:
            bool: True if refresh was successful (at least partially), False otherwise
        """
        logger.info("Starting data refresh cycle...")
        
        successful_fetches = 0

        # 1. Fetch Matches
        for comp_code in self.COMPETITION_CODES:
            try:
                # Fetch recent matches (last 7 days = 168 hours)
                response = self.api_client.fetch_recent_matches(comp_code, hours=168)
                time.sleep(7) # Rate limit

                if response:
                    matches = response.get('matches', [])
                    normalized_matches = []
                    
                    for match_data in matches:
                        normalized = normalize_match(
                            match_data,
                            competition_code=comp_code,
                            competition_name=response.get('competition', {}).get('name', comp_code)
                        )
                        if normalized:
                            normalized_matches.append(normalized)
                    
                    self.db.save_matches(comp_code, normalized_matches)
                    successful_fetches += 1
                    logger.info(f"Updated matches for {comp_code}: {len(normalized_matches)} matches")
                
            except Exception as e:
                logger.error(f"Error updating matches for {comp_code}: {e}")

        # 2. Fetch Top Scorers
        for comp_code in self.COMPETITION_CODES:
            try:
                scorers_data = self.api_client.fetch_top_scorers(comp_code)
                if scorers_data:
                    scorers = scorers_data.get('scorers', [])
                    self.db.save_scorers(comp_code, scorers)
                    logger.info(f"Updated scorers for {comp_code}")
                time.sleep(7) # Rate limit
            except Exception as e:
                logger.error(f"Error updating scorers for {comp_code}: {e}")

        # 3. Fetch Standings
        for comp_code in self.COMPETITION_CODES:
            try:
                standings_data = self.api_client.fetch_standings(comp_code)
                if standings_data:
                    standings_list = standings_data.get('standings', [])
                    total_table = next((s for s in standings_list if s.get('type') == 'TOTAL'), None)
                    if total_table:
                        table_data = total_table.get('table', [])
                        self.db.save_standings(comp_code, table_data)
                        logger.info(f"Updated standings for {comp_code}")
                time.sleep(7) # Rate limit
            except Exception as e:
                logger.error(f"Error updating standings for {comp_code}: {e}")

        if successful_fetches == 0:
            logger.error("Failed to fetch match data from any competition")
            return False

        logger.info("Data refresh cycle completed")
        return True

    def get_matches(self):
        """
        Get match data from database.

        Returns:
            dict: Matches grouped by competition code
        """
        matches_by_comp = self.db.get_all_matches()
        
        # Sort matches for each competition by utc_kickoff descending (newest first)
        for comp_code, matches in matches_by_comp.items():
            if matches:
                matches.sort(
                    key=lambda m: m.get('utc_kickoff', ''),
                    reverse=True
                )
            
        return matches_by_comp

    def get_scorers(self):
        """
        Get top scorers data from database.

        Returns:
            dict: Scorers grouped by competition code
        """
        return self.db.get_all_scorers()

    def get_standings(self):
        """
        Get standings data from database.

        Returns:
            dict: Standings grouped by competition code
        """
        return self.db.get_all_standings()

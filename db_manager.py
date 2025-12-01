import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database connections and operations."""

    def __init__(self, db_path="football_data.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize database tables if they don't exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Matches table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS matches (
                        competition_code TEXT PRIMARY KEY,
                        data_json TEXT,
                        updated_at TIMESTAMP
                    )
                """)

                # Scorers table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scorers (
                        competition_code TEXT PRIMARY KEY,
                        data_json TEXT,
                        updated_at TIMESTAMP
                    )
                """)

                # Standings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS standings (
                        competition_code TEXT PRIMARY KEY,
                        data_json TEXT,
                        updated_at TIMESTAMP
                    )
                """)

                # App Metadata table (for AI summary, etc.)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS app_metadata (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        updated_at TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")

    def is_empty(self):
        """Check if the database has any match data."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM matches")
                count = cursor.fetchone()[0]
                return count == 0
        except Exception as e:
            logger.error(f"Error checking if DB is empty: {e}")
            return True

    def save_matches(self, competition_code, data):
        """Save match data for a competition."""
        self._save_data('matches', competition_code, data)

    def get_matches(self, competition_code):
        """Get match data for a competition."""
        return self._get_data('matches', competition_code)

    def get_all_matches(self):
        """Get all matches grouped by competition."""
        return self._get_all_data('matches')

    def save_scorers(self, competition_code, data):
        """Save scorer data for a competition."""
        self._save_data('scorers', competition_code, data)

    def get_scorers(self, competition_code):
        """Get scorer data for a competition."""
        return self._get_data('scorers', competition_code)

    def get_all_scorers(self):
        """Get all scorers grouped by competition."""
        return self._get_all_data('scorers')

    def save_standings(self, competition_code, data):
        """Save standings data for a competition."""
        self._save_data('standings', competition_code, data)

    def get_standings(self, competition_code):
        """Get standings data for a competition."""
        return self._get_data('standings', competition_code)

    def get_all_standings(self):
        """Get all standings grouped by competition."""
        return self._get_all_data('standings')

    def save_summary(self, summary_text):
        """Save the AI summary."""
        self._save_metadata('ai_summary', summary_text)

    def get_summary(self):
        """Get the AI summary."""
        return self._get_metadata('ai_summary')

    def _save_data(self, table, competition_code, data):
        """Helper to save data to a table."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    INSERT OR REPLACE INTO {table} (competition_code, data_json, updated_at)
                    VALUES (?, ?, ?)
                """, (competition_code, json.dumps(data), datetime.utcnow()))
                conn.commit()
        except Exception as e:
            logger.error(f"Error saving to {table} for {competition_code}: {e}")

    def _get_data(self, table, competition_code):
        """Helper to get data from a table."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT data_json FROM {table} WHERE competition_code = ?", (competition_code,))
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return None
        except Exception as e:
            logger.error(f"Error getting from {table} for {competition_code}: {e}")
            return None

    def _get_all_data(self, table):
        """Helper to get all data from a table as a dict."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT competition_code, data_json FROM {table}")
                rows = cursor.fetchall()
                result = {}
                for code, data_json in rows:
                    result[code] = json.loads(data_json)
                return result
        except Exception as e:
            logger.error(f"Error getting all from {table}: {e}")
            return {}

    def _save_metadata(self, key, value):
        """Helper to save metadata."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO app_metadata (key, value, updated_at)
                    VALUES (?, ?, ?)
                """, (key, value, datetime.utcnow()))
                conn.commit()
        except Exception as e:
            logger.error(f"Error saving metadata {key}: {e}")

    def _get_metadata(self, key):
        """Helper to get metadata."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM app_metadata WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    return row[0]
                return None
        except Exception as e:
            logger.error(f"Error getting metadata {key}: {e}")
            return None

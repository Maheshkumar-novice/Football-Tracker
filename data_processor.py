"""Data processing and normalization for match data."""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def normalize_match(match_data, competition_code=None, competition_name=None):
    """
    Normalize raw API match data into a consistent format.

    Args:
        match_data: Raw match data from API
        competition_code: Competition code (optional, extracted from match if not provided)
        competition_name: Competition name (optional, extracted from match if not provided)

    Returns:
        dict: Normalized match object with standardized fields
    """
    try:
        # Extract basic match information
        status = match_data.get('status', 'SCHEDULED')
        home_team = match_data.get('homeTeam', {}).get('name', 'N/A')
        away_team = match_data.get('awayTeam', {}).get('name', 'N/A')
        utc_kickoff = match_data.get('utcDate', '')

        # Format score based on match status
        score_text = _format_score(match_data, status)

        # Build normalized match object
        normalized = {
            'status': status,
            'score_text': score_text,
            'home_team': home_team,
            'away_team': away_team,
            'utc_kickoff': utc_kickoff,
        }

        # Add competition info if provided or extract from match data
        if competition_code:
            normalized['competition_code'] = competition_code
        elif 'competition' in match_data:
            normalized['competition_code'] = match_data['competition'].get('code', 'N/A')

        if competition_name:
            normalized['competition_name'] = competition_name
        elif 'competition' in match_data:
            normalized['competition_name'] = match_data['competition'].get('name', 'N/A')

        # Format display date (e.g., "Sat, Nov 15")
        if utc_kickoff:
            normalized['display_date'] = _format_display_date(utc_kickoff)
        else:
            normalized['display_date'] = 'N/A'

        # Create Google search query
        comp_name = normalized.get('competition_name', '')
        normalized['google_query'] = f"{comp_name} {home_team} vs {away_team}"

        return normalized

    except Exception as e:
        logger.warning(f"Error normalizing match data: {e}")
        return None


def _format_score(match_data, status):
    """
    Format the score text based on match status.

    Args:
        match_data: Raw match data from API
        status: Match status (FINISHED, LIVE, SCHEDULED, etc.)

    Returns:
        str: Formatted score text (e.g., "2–1", "LIVE", "SCHEDULED")
    """
    if status == 'FINISHED':
        # Extract full-time score
        score = match_data.get('score', {})
        full_time = score.get('fullTime', {})
        home_score = full_time.get('home')
        away_score = full_time.get('away')

        if home_score is not None and away_score is not None:
            # Use en dash (–) for score separator
            return f"{home_score}–{away_score}"
        else:
            logger.warning("Missing score data for finished match")
            return "N/A"

    elif status == 'LIVE' or status == 'IN_PLAY':
        return "LIVE"

    else:
        # For SCHEDULED, TIMED, POSTPONED, etc.
        return "SCHEDULED"


def _format_display_date(utc_date_str):
    """
    Format UTC date string to display format.

    Args:
        utc_date_str: ISO 8601 date string (e.g., "2025-11-15T17:30:00Z")

    Returns:
        str: Formatted date (e.g., "Sat, Nov 15")
    """
    try:
        # Parse ISO 8601 date string
        dt = datetime.fromisoformat(utc_date_str.replace('Z', '+00:00'))
        # Format as "Weekday, Month Day"
        return dt.strftime("%a, %b %d")
    except Exception as e:
        logger.warning(f"Error formatting date {utc_date_str}: {e}")
        return "N/A"


def group_by_competition(matches):
    """
    Group normalized matches by competition code.

    Args:
        matches: List of normalized match objects

    Returns:
        dict: Matches grouped by competition code, sorted by kickoff time (most recent first)
              Format: {"PL": [match_objects], "PD": [match_objects], ...}
    """
    grouped = {}

    for match in matches:
        if not match:
            continue

        comp_code = match.get('competition_code')
        if not comp_code:
            logger.warning("Match missing competition_code, skipping")
            continue

        if comp_code not in grouped:
            grouped[comp_code] = []

        grouped[comp_code].append(match)

    # Sort matches within each competition by kickoff time (most recent first)
    for comp_code in grouped:
        grouped[comp_code].sort(
            key=lambda m: m.get('utc_kickoff', ''),
            reverse=True
        )

    return grouped

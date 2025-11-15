#!/usr/bin/env python3
"""
Test script for Football-Data.org API
Fetches past 7 days and future matches to verify API connectivity and data structure.
"""

import sys
from datetime import datetime, timedelta
from logging_config import setup_logging
from config import Config
from football_api import FootballAPIClient
from data_processor import normalize_match, group_by_competition

# Setup logging
setup_logging()

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_match(match, show_raw=False):
    """Print match information in a readable format."""
    if show_raw:
        print(f"\nRaw match data keys: {list(match.keys())}")
        print(f"Status: {match.get('status')}")
        print(f"UTC Date: {match.get('utcDate')}")
        print(f"Home: {match.get('homeTeam', {}).get('name')}")
        print(f"Away: {match.get('awayTeam', {}).get('name')}")
        print(f"Score: {match.get('score')}")
    else:
        home = match.get('home_team', 'N/A')
        away = match.get('away_team', 'N/A')
        date = match.get('display_date', 'N/A')
        score = match.get('score_text', 'N/A')
        status = match.get('status', 'N/A')
        print(f"  {date:12} | {home:25} vs {away:25} | {score:10} ({status})")

def test_past_matches():
    """Test fetching past 7 days of matches."""
    print_section("Testing Past 7 Days Matches")

    client = FootballAPIClient(Config.API_KEY)

    # Calculate date range (past 7 days)
    now = datetime.utcnow()
    date_from = now - timedelta(days=7)

    date_from_str = date_from.strftime("%Y-%m-%d")
    date_to_str = now.strftime("%Y-%m-%d")

    print(f"\nDate range: {date_from_str} to {date_to_str}")
    print(f"Testing {len(client.COMPETITION_CODES)} competitions: {', '.join(client.COMPETITION_CODES)}")

    all_matches = []

    for comp_code in client.COMPETITION_CODES:
        print(f"\n--- {comp_code} (Past 7 days) ---")

        # Fetch matches with custom date range
        params = {
            "dateFrom": date_from_str,
            "dateTo": date_to_str
        }

        response = client.fetch_competition_matches(comp_code, params=params)

        if response is None:
            print(f"  ❌ Failed to fetch data for {comp_code}")
            continue

        matches = response.get('matches', [])
        comp_name = response.get('competition', {}).get('name', comp_code)

        print(f"  ✅ Found {len(matches)} matches for {comp_name}")

        if matches:
            print(f"\n  Sample raw match data (first match):")
            print_match(matches[0], show_raw=True)

            print(f"\n  Normalized matches:")
            for match_data in matches[:5]:  # Show first 5
                normalized = normalize_match(
                    match_data,
                    competition_code=comp_code,
                    competition_name=comp_name
                )
                if normalized:
                    print_match(normalized)
                    all_matches.append(normalized)

            if len(matches) > 5:
                print(f"  ... and {len(matches) - 5} more matches")

    print(f"\n📊 Total past matches found: {len(all_matches)}")

    return all_matches

def test_future_matches():
    """Test fetching future matches."""
    print_section("Testing Future Matches (Next 14 Days)")

    client = FootballAPIClient(Config.API_KEY)

    # Calculate date range (today to +14 days)
    now = datetime.utcnow()
    date_from = now
    date_to = now + timedelta(days=14)

    date_from_str = date_from.strftime("%Y-%m-%d")
    date_to_str = date_to.strftime("%Y-%m-%d")

    print(f"\nDate range: {date_from_str} to {date_to_str}")
    print(f"Testing {len(client.COMPETITION_CODES)} competitions: {', '.join(client.COMPETITION_CODES)}")

    all_matches = []

    for comp_code in client.COMPETITION_CODES:
        print(f"\n--- {comp_code} (Future matches) ---")

        # Fetch matches with custom date range
        params = {
            "dateFrom": date_from_str,
            "dateTo": date_to_str
        }

        response = client.fetch_competition_matches(comp_code, params=params)

        if response is None:
            print(f"  ❌ Failed to fetch data for {comp_code}")
            continue

        matches = response.get('matches', [])
        comp_name = response.get('competition', {}).get('name', comp_code)

        print(f"  ✅ Found {len(matches)} scheduled matches for {comp_name}")

        if matches:
            print(f"\n  Upcoming matches:")
            for match_data in matches[:5]:  # Show first 5
                normalized = normalize_match(
                    match_data,
                    competition_code=comp_code,
                    competition_name=comp_name
                )
                if normalized:
                    print_match(normalized)
                    all_matches.append(normalized)

            if len(matches) > 5:
                print(f"  ... and {len(matches) - 5} more matches")

    print(f"\n📊 Total future matches found: {len(all_matches)}")

    return all_matches

def test_combined_view():
    """Test fetching past 7 days and future matches combined."""
    print_section("Combined View: Past 7 Days + Future Matches")

    client = FootballAPIClient(Config.API_KEY)

    # Calculate date range (past 7 days to +14 days)
    now = datetime.utcnow()
    date_from = now - timedelta(days=7)
    date_to = now + timedelta(days=14)

    date_from_str = date_from.strftime("%Y-%m-%d")
    date_to_str = date_to.strftime("%Y-%m-%d")

    print(f"\nDate range: {date_from_str} to {date_to_str}")

    all_matches = []

    for comp_code in client.COMPETITION_CODES:
        params = {
            "dateFrom": date_from_str,
            "dateTo": date_to_str
        }

        response = client.fetch_competition_matches(comp_code, params=params)

        if response:
            matches = response.get('matches', [])
            comp_name = response.get('competition', {}).get('name', comp_code)

            for match_data in matches:
                normalized = normalize_match(
                    match_data,
                    competition_code=comp_code,
                    competition_name=comp_name
                )
                if normalized:
                    all_matches.append(normalized)

    # Group by competition
    grouped = group_by_competition(all_matches)

    print(f"\n📊 Summary by Competition:")
    for comp_code, matches in grouped.items():
        if matches:
            comp_name = matches[0].get('competition_name', comp_code)
            finished = sum(1 for m in matches if m.get('status') == 'FINISHED')
            scheduled = sum(1 for m in matches if m.get('status') in ['SCHEDULED', 'TIMED'])
            live = sum(1 for m in matches if m.get('status') in ['LIVE', 'IN_PLAY'])

            print(f"\n{comp_name} ({comp_code}):")
            print(f"  Total: {len(matches)} matches")
            print(f"  Finished: {finished}")
            print(f"  Scheduled: {scheduled}")
            print(f"  Live: {live}")

            # Show most recent finished match
            finished_matches = [m for m in matches if m.get('status') == 'FINISHED']
            if finished_matches:
                print(f"\n  Most recent result:")
                print_match(finished_matches[0])

            # Show next scheduled match
            scheduled_matches = [m for m in matches if m.get('status') in ['SCHEDULED', 'TIMED']]
            if scheduled_matches:
                # Sort by date (oldest first for upcoming)
                scheduled_matches.sort(key=lambda m: m.get('utc_kickoff', ''))
                print(f"\n  Next match:")
                print_match(scheduled_matches[0])

def main():
    """Main test function."""
    print_section("Football-Data.org API Test Script")
    print(f"\n✓ API Key configured: {bool(Config.API_KEY)}")
    print(f"✓ Competitions to test: {', '.join(FootballAPIClient.COMPETITION_CODES)}")

    try:
        # Test past matches
        past_matches = test_past_matches()

        # Test future matches
        future_matches = test_future_matches()

        # Test combined view
        test_combined_view()

        print_section("Test Complete")
        print(f"\n✅ Total past matches: {len(past_matches)}")
        print(f"✅ Total future matches: {len(future_matches)}")
        print(f"✅ Grand total: {len(past_matches) + len(future_matches)}")

        print("\n📝 Notes:")
        print("  - Free tier data is delayed by a few minutes")
        print("  - Rate limit: 10 calls per minute")
        print("  - All match times are in UTC")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

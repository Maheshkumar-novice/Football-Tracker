# Football Matches Tracker - TODO Checklist

## Initial Setup
- [x] Create project directory and virtual environment
- [x] Get API key from Football-Data.org
- [x] Create `.env` file with `FOOTBALL_API_KEY`
- [x] Create `.gitignore` (include `venv/`, `.env`, `*.log`)

---

## Step 1: Logging Configuration
- [x] Create `logging_config.py` with `setup_logging()` function
- [x] Configure console and file logging
- [x] Test: Verify logs appear in console and `app.log`

## Step 2: Environment Configuration
- [x] Install `python-dotenv`
- [x] Create `config.py` to load environment variables
- [x] Test: Import and verify Config values

## Step 3: API Client - Basic Structure
- [x] Install `requests`
- [x] Create `football_api.py` with `FootballAPIClient` class
- [x] Implement `fetch_competition_matches()` method
- [x] Test: Make API request and verify response

## Step 4: API Client - Date Filtering
- [x] Add `fetch_recent_matches(competition_code, hours=72)` method
- [x] Add date range query parameters
- [x] Test: Verify only recent matches returned

## Step 5: Data Normalization - Status and Score
- [x] Create `data_processor.py`
- [x] Implement `normalize_match()` function
- [x] Test: Verify score formatting (FINISHED, LIVE, SCHEDULED)

## Step 6: Data Normalization - Complete Match Object
- [x] Add remaining fields (competition_code, display_date, google_query)
- [x] Implement `group_by_competition()` function
- [x] Test: Verify 8 fields and sorting works

## Step 7: Cache Module - Basic Structure
- [x] Create `cache.py` with `MatchCache` class
- [x] Implement `is_valid()` and `get_age_seconds()` methods
- [x] Test: Verify TTL validation

## Step 8: Cache Module - Read and Write
- [x] Implement `set_data()`, `get_data()`, and `clear()` methods
- [x] Test: Verify cache updates and retrieval

## Step 9: Flask App - Basic Skeleton
- [x] Install Flask
- [x] Create `app.py` with basic routes (/, /health)
- [x] Test: Run app and access both routes

## Step 10: Flask App - Mock Data
- [x] Create `templates/` directory
- [x] Create basic `index.html` template
- [x] Pass mock data to template
- [x] Test: Verify mock data displays

## Step 11: HTML Template - Structure
- [x] Complete HTML structure with header, main, footer
- [x] Add error banner (conditional)
- [x] Link CSS and JS files
- [x] Test: Verify structure renders

## Step 12: HTML Template - Match Rendering
- [x] Add Jinja2 loops for competitions and matches
- [x] Add onclick handlers for Google search
- [x] Test: Verify matches display and clicks work

## Step 13: CSS - Layout and Headers
- [x] Create `static/styles.css`
- [x] Style error banner, header, competition sections
- [x] Test: Verify visual hierarchy

## Step 14: CSS - Match Rows
- [x] Style match rows with hover effects
- [x] Add responsive considerations
- [x] Test: Verify clickability and mobile view

## Step 15: JavaScript - Auto-Refresh
- [x] Create `static/script.js`
- [x] Add 30-minute auto-refresh timer
- [x] Test: Verify page reloads (use short interval for testing)

## Step 16: Integration - API to Cache
- [x] Create `data_service.py` with `MatchDataService` class
- [x] Implement `refresh_data()` and `get_matches()` methods
- [x] Test: Verify API calls populate cache

## Step 17: Integration - Service to Flask
- [x] Update `app.py` to use `MatchDataService`
- [x] Calculate relative time for "last updated"
- [x] Add try-except for error handling
- [x] Test: Verify real match data displays

## Step 18: Final Polish
- [x] Add detailed logging across all modules
- [x] Add retry logic to API client
- [x] Improve error banner visibility
- [x] Add empty state message
- [x] Create `README.md` with setup instructions

---

## Final Testing Checklist
- [x] App starts successfully
- [x] First load fetches from API
- [x] Second load uses cache (within 30 min)
- [x] API failure shows error banner with cached data
- [x] Match clicks open Google search
- [x] Page auto-refreshes after 30 minutes
- [x] Empty state displays gracefully

---

## Dependencies to Install
```bash
uv pip install flask python-dotenv requests
```

## Run the App
```bash
uv run python app.py
```

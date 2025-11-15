# Football Matches Tracker - Implementation Blueprint

## Initial Analysis

This is a Flask web application with moderate complexity. The key challenges are:
1. API integration with proper error handling
2. Cache management with timestamp comparison
3. Clean separation of concerns across modules
4. Frontend that auto-refreshes gracefully

## High-Level Architecture Plan

```
Phase 1: Core Infrastructure (logging, config)
Phase 2: API Integration Layer
Phase 3: Cache Management
Phase 4: Flask Application Core
Phase 5: Frontend Implementation
Phase 6: Integration & Polish
```

## Detailed Step Breakdown

### Round 1: Initial Chunking

1. **Logging setup** - standalone, testable
2. **API client** - fetch data from Football-Data.org
3. **Cache layer** - store and retrieve with TTL
4. **Flask routes** - serve HTML
5. **Frontend template** - display matches
6. **Auto-refresh** - JavaScript timer
7. **Integration** - wire everything together

### Round 2: Further Refinement

After reviewing, steps 2-3 are too large. Breaking down further:

1. Logging configuration
2. Environment variable loading
3. API client structure (no data processing yet)
4. Data normalization logic
5. Cache initialization
6. Cache read/write with TTL
7. Flask app skeleton
8. Index route with hardcoded data
9. HTML template structure
10. CSS styling
11. Match rendering logic
12. JavaScript auto-refresh
13. Error banner handling
14. Final integration

### Round 3: Size Validation

Steps look good, but step 4 (data normalization) and step 11 (match rendering) might be complex. Let's split:

**Final optimized steps:**

1. Logging configuration module
2. Environment variable configuration
3. API client - basic structure with one endpoint
4. API client - date filtering logic
5. Data normalization - status and score formatting
6. Data normalization - competition grouping
7. Cache module - initialization and basic structure
8. Cache module - read/write with TTL validation
9. Flask app - skeleton with health check
10. Flask app - index route with mock data
11. HTML template - header and structure
12. HTML template - match list rendering
13. CSS - layout and competition headers
14. CSS - match rows and footer
15. JavaScript - auto-refresh timer
16. Integration - connect API to cache
17. Integration - connect cache to Flask route
18. Error handling and banner display

---

## Implementation Prompts

Each prompt below is designed to be copy-pasted directly to a code-generation LLM.

---

### Prompt 1: Logging Configuration

```
Create a Python module called `logging_config.py` for a Flask application that sets up logging with the following requirements:

- Function `setup_logging()` that configures the root logger
- Log to both console (stdout) and a file named `app.log`
- Default log level should be INFO, but allow override via environment variable `LOG_LEVEL`
- Use a clear formatter that includes timestamp, level name, and message
- Console output should be readable for development
- File output should include more detail (module name, line number)
- No log rotation needed for V1

Example usage should be:
```python
from logging_config import setup_logging
setup_logging()
```

Keep it simple and focused - just the logging setup, no other dependencies.
```

---

### Prompt 2: Environment Configuration

```
Create a Python module called `config.py` that loads configuration from environment variables.

Requirements:
- Load `FOOTBALL_API_KEY` (required)
- Load `CACHE_TTL` with default of 1800 seconds
- Load `LOG_LEVEL` with default of "INFO"
- Raise a clear error if `FOOTBALL_API_KEY` is missing
- Use python-dotenv to load from `.env` file if present
- Provide a simple dict or class to access these values

Example usage:
```python
from config import Config
print(Config.API_KEY)
print(Config.CACHE_TTL)
```

Keep it minimal - just configuration loading, no business logic.
```

---

### Prompt 3: API Client - Basic Structure

```
Create a Python module called `football_api.py` that defines the basic structure for fetching data from Football-Data.org API.

Requirements:
- Class `FootballAPIClient` with constructor that takes an API key
- Define the 5 competition codes as a class constant: PL, PD, BL1, SA, FL1
- Method `fetch_competition_matches(competition_code)` that makes a GET request to:
  `https://api.football-data.org/v4/competitions/{code}/matches`
- Include header: `X-Auth-Token: {api_key}`
- Use the `requests` library
- Return the raw JSON response
- Add basic error handling: log errors and return None on failure
- Import logging and use logger.info/error for request tracking

Do NOT implement date filtering yet - just get the basic API call working with proper headers and error handling.

Example usage:
```python
client = FootballAPIClient(api_key)
data = client.fetch_competition_matches("PL")
```
```

---

### Prompt 4: API Client - Date Filtering

```
Extend the `football_api.py` module to add date filtering for recent matches.

Requirements:
- Add a new method `fetch_recent_matches(competition_code, hours=72)` that:
  - Calculates date range: from (now - hours) to (now) in UTC
  - Formats dates as ISO 8601 strings (e.g., "2025-11-15T00:00:00Z")
  - Adds query parameters `dateFrom` and `dateTo` to the API request
  - Calls the existing `fetch_competition_matches` method with these parameters
- Update `fetch_competition_matches` to accept optional query params
- Use `datetime` and `timedelta` from Python standard library
- Log the date range being requested

The API endpoint supports filtering: `/competitions/{code}/matches?dateFrom=...&dateTo=...`

Example usage:
```python
client = FootballAPIClient(api_key)
data = client.fetch_recent_matches("PL", hours=72)  # Last 3 days
```

Keep the existing basic fetch method intact for potential future use.
```

---

### Prompt 5: Data Normalization - Status and Score

```
Create a new module called `data_processor.py` that handles match data normalization.

Requirements:
- Function `normalize_match(match_data)` that takes raw API match data and returns a normalized dict
- Extract and format these fields:
  - `status`: from match status (e.g., "FINISHED", "LIVE", "SCHEDULED")
  - `score_text`: 
    - If FINISHED: format as "X–Y" using full-time score (use en dash, not hyphen)
    - If LIVE: return "LIVE"
    - Otherwise: return "SCHEDULED"
  - `home_team`: from match.homeTeam.name
  - `away_team`: from match.awayTeam.name
  - `utc_kickoff`: from match.utcDate (keep as ISO string)
- Handle missing data gracefully (use "N/A" for missing scores, log warnings)

Example raw API structure:
```json
{
  "status": "FINISHED",
  "utcDate": "2025-11-15T17:30:00Z",
  "homeTeam": {"name": "Arsenal"},
  "awayTeam": {"name": "Chelsea"},
  "score": {
    "fullTime": {"home": 2, "away": 1}
  }
}
```

Example output:
```python
{
  "status": "FINISHED",
  "score_text": "2–1",
  "home_team": "Arsenal",
  "away_team": "Chelsea",
  "utc_kickoff": "2025-11-15T17:30:00Z"
}
```

Focus only on status and score logic - we'll add more fields in the next step.
```

---

### Prompt 6: Data Normalization - Complete Match Object

```
Extend the `data_processor.py` module to create complete normalized match objects.

Requirements:
- Enhance `normalize_match()` to add these additional fields:
  - `competition_code`: from match.competition.code (or pass as parameter)
  - `competition_name`: from match.competition.name (or pass as parameter)
  - `display_date`: formatted as "Weekday, Month Day" (e.g., "Sat, Nov 15")
    - Parse `utc_kickoff` and format using strftime
  - `google_query`: format as "{competition_name} {home_team} vs {away_team}"
- Create a complete match dict with all 8 required fields

Also add a new function:
- `group_by_competition(matches)` that takes a list of normalized matches
- Returns a dict with competition codes as keys and lists of matches as values
- Sort matches within each competition by `utc_kickoff` descending (most recent first)

Example output structure:
```python
{
  "PL": [
    {
      "competition_code": "PL",
      "competition_name": "Premier League",
      "utc_kickoff": "2025-11-15T17:30:00Z",
      "display_date": "Sat, Nov 15",
      "home_team": "Arsenal",
      "away_team": "Chelsea",
      "status": "FINISHED",
      "score_text": "2–1",
      "google_query": "Premier League Arsenal vs Chelsea"
    }
  ],
  "PD": [...]
}
```
```

---

### Prompt 7: Cache Module - Basic Structure

```
Create a module called `cache.py` that implements in-memory caching with TTL.

Requirements:
- Class `MatchCache` that stores match data in memory
- Constructor accepts `ttl_seconds` parameter (default 1800)
- Internal structure to store:
  - `last_updated`: UTC timestamp
  - `competitions`: dict with competition codes as keys
- Methods to implement:
  - `__init__(ttl_seconds)`: initialize empty cache
  - `is_valid()`: returns True if cache exists and hasn't exceeded TTL
  - `get_age_seconds()`: returns how old the cache is, or None if empty
- Use `datetime.datetime.utcnow()` for timestamp operations
- Store data as a simple dict attribute

Do NOT implement read/write methods yet - just the structure and TTL validation logic.

Example usage:
```python
cache = MatchCache(ttl_seconds=1800)
if cache.is_valid():
    print("Cache is still fresh")
age = cache.get_age_seconds()
```
```

---

### Prompt 8: Cache Module - Read and Write Operations

```
Extend the `cache.py` module to add data storage and retrieval.

Requirements:
- Add method `set_data(competitions_dict, timestamp=None)`:
  - Stores the competitions dict
  - Sets `last_updated` to provided timestamp or current UTC time
  - ONLY updates if new timestamp is newer than existing (or cache is empty)
  - Returns True if updated, False if skipped
  - Log when cache is updated or skipped
- Add method `get_data()`:
  - Returns the cached competitions dict
  - Returns None if cache is empty or invalid
  - Log cache hits and misses
- Add method `clear()`:
  - Resets cache to empty state

Expected data format:
```python
{
  "PL": [match_objects],
  "PD": [match_objects],
  ...
}
```

Example usage:
```python
cache = MatchCache()
cache.set_data(competitions_dict, timestamp=datetime.utcnow())
data = cache.get_data()  # Returns dict or None
```

Include appropriate logging for debugging cache behavior.
```

---

### Prompt 9: Flask App - Basic Skeleton

```
Create the main Flask application file `app.py` with basic structure.

Requirements:
- Import Flask and create app instance
- Import and call `setup_logging()` at module level
- Import `Config` and access environment variables
- Create two routes:
  - `GET /` - returns a simple "Football Matches Tracker" message for now
  - `GET /health` - returns {"status": "ok"} as JSON
- Add basic error handler for 500 errors that logs the exception
- Include `if __name__ == "__main__"` block to run in debug mode
- Set up logger to log app startup

Do NOT connect to cache or API yet - just get the Flask skeleton running.

Example structure:
```python
from flask import Flask, jsonify
from logging_config import setup_logging
from config import Config

setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return "Football Matches Tracker"

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
```

Test that the app starts and both routes are accessible.
```

---

### Prompt 10: Flask App - Index Route with Mock Data

```
Update `app.py` to render a template with mock match data.

Requirements:
- Create a `templates/` directory
- Update the `/` route to:
  - Define mock data structure matching the normalized format (2-3 sample matches)
  - Calculate a mock "last_updated" timestamp (e.g., 10 minutes ago)
  - Pass data to template using `render_template()`
  - Pass: `competitions` dict, `last_updated` timestamp, `error` flag (False for now)
- Create a minimal `templates/index.html` that displays:
  - Page title
  - "Last updated: X minutes ago" (calculate relative time in template or Python)
  - A simple list of competitions showing match count
  
Mock data example:
```python
mock_competitions = {
    "PL": [
        {
            "competition_name": "Premier League",
            "display_date": "Sat, Nov 15",
            "home_team": "Arsenal",
            "away_team": "Chelsea",
            "score_text": "2–1",
            "google_query": "Premier League Arsenal vs Chelsea"
        }
    ]
}
```

The template can be very basic for now - we'll enhance it in the next steps.

Test that the route renders the template with the mock data visible.
```

---

### Prompt 11: HTML Template - Header and Structure

```
Create a complete `templates/index.html` template with proper structure.

Requirements:
- Standard HTML5 doctype and structure
- `<head>` section with:
  - Page title: "Football Matches Tracker"
  - Link to `/static/styles.css`
  - Meta charset and viewport tags
- `<body>` structure:
  - Error banner div (hidden by default, controlled by `error` variable)
    - Show "Error fetching match data. Showing cached results." if error is True
    - Style as red bar at very top
  - Header section with:
    - "Football Matches Tracker"
    - "Recent Results — Last 72 Hours"
    - "Last updated: {relative_time}" (pass as variable from Flask)
  - Main content area (empty `<div id="matches">` for now)
  - Footer: "Data provided by Football-Data.org"
- Script tag linking to `/static/script.js` at end of body

Use Jinja2 syntax for:
- Conditional error banner: `{% if error %}`
- Display last_updated: `{{ last_updated }}`

Keep semantic HTML - use `<header>`, `<main>`, `<footer>` tags.

Do NOT add match rendering yet - that's the next step.
```

---

### Prompt 12: HTML Template - Match List Rendering

```
Extend `templates/index.html` to render the matches list.

Requirements:
- Inside the `<main>` section, loop through competitions dict
- For each competition:
  - Show competition header (e.g., "▌ Premier League")
  - Loop through matches in that competition
  - Display each match as a clickable row with format:
    `Display_date • Home_team vs Away_team • Score_text`
  - Make the entire row a link with onclick that opens Google search in new tab
    - Use JavaScript: `window.open('https://www.google.com/search?q=' + encodeURIComponent(query), '_blank')`
    - Pass google_query from match data

Jinja2 structure:
```html
{% for code, matches in competitions.items() %}
  {% if matches %}
    <div class="competition-section">
      <h2 class="competition-header">▌ {{ matches[0].competition_name }}</h2>
      {% for match in matches %}
        <div class="match-row" onclick="window.open('https://www.google.com/search?q=' + encodeURIComponent('{{ match.google_query }}'), '_blank')" style="cursor: pointer;">
          <span class="match-date">{{ match.display_date }}</span>
          <span class="match-separator">•</span>
          <span class="match-teams">{{ match.home_team }} vs {{ match.away_team }}</span>
          <span class="match-separator">•</span>
          <span class="match-score">{{ match.score_text }}</span>
        </div>
      {% endfor %}
    </div>
  {% endif %}
{% endfor %}
```

Handle empty state: show "No recent matches found" if competitions dict is empty or all lists are empty.

Add appropriate CSS classes for styling in the next steps.
```

---

### Prompt 13: CSS - Layout and Competition Headers

```
Create `static/styles.css` with base layout and competition section styling.

Requirements:
- **Global styles:**
  - Light mode only (white/light gray backgrounds)
  - Sans-serif font family
  - Reset margins/padding on body
  - Max width container for readability (e.g., 1200px centered)
- **Error banner:**
  - Position at very top, full width
  - Red background (#dc3545), white text
  - Padding for readability
  - Display: none by default, shown via class
- **Header:**
  - Large title text
  - Subtitle in muted color
  - "Last updated" text in smaller, lighter font
  - Adequate spacing below header
- **Competition sections:**
  - Competition header styled as section bar:
    - Left border accent (thick, colored)
    - Background: light gray
    - Bold text
    - Padding and margin for separation
  - Use distinct colors for different leagues (optional but nice)
- **Footer:**
  - Centered, muted text
  - Small font size
  - Margin top for spacing

Focus on structure and headers - match rows styling comes next.

Keep design clean and minimal - avoid over-styling.
```

---

### Prompt 14: CSS - Match Rows and Polish

```
Extend `static/styles.css` to style match rows and add final polish.

Requirements:
- **Match rows:**
  - Display as flexbox or inline elements with proper spacing
  - Padding for comfortable click target
  - Hover effect: subtle background color change
  - Cursor: pointer
  - Border or alternating background colors for separation
  - Separators (•) styled in muted color
  - Score text can be slightly bolder or different color
- **Responsive considerations:**
  - Allow team names to wrap if long
  - Maintain readability on smaller screens
  - Match rows should stack gracefully
- **Typography:**
  - Match date: smaller, muted
  - Team names: regular weight
  - Score: slightly emphasized
- **Spacing:**
  - Moderate spacing between competition sections
  - Comfortable padding within match rows
  - Adequate margin around page content

Aim for "light structure" tier as specified:
- Subtle visual hierarchy
- Clean, not cluttered
- Professional appearance

Test the styles with the mock data to ensure readability and clickability.
```

---

### Prompt 15: JavaScript - Auto-Refresh Timer

```
Create `static/script.js` to implement auto-refresh functionality.

Requirements:
- Set up a timer that reloads the page every 30 minutes (1,800,000 milliseconds)
- Use `setTimeout()` to schedule the reload
- On reload, use `window.location.reload()` to refresh the entire page
- No loading indicators needed
- Add a console.log message when timer is set for debugging

Implementation:
```javascript
// Auto-refresh every 30 minutes
const REFRESH_INTERVAL = 30 * 60 * 1000; // 30 minutes in milliseconds

setTimeout(() => {
  console.log('Auto-refreshing page...');
  window.location.reload();
}, REFRESH_INTERVAL);

console.log(`Auto-refresh scheduled for ${REFRESH_INTERVAL / 1000 / 60} minutes from now`);
```

Keep it simple - no need for progress bars or countdown displays.

Test by temporarily setting interval to a few seconds to verify reload works.
```

---

### Prompt 16: Integration - Connect API to Cache

```
Create a new module called `data_service.py` that orchestrates API calls and cache updates.

Requirements:
- Import `FootballAPIClient`, `MatchCache`, and `data_processor` functions
- Class `MatchDataService` with:
  - Constructor that takes API key and cache TTL
  - Initializes API client and cache
  - Stores list of competition codes
- Method `refresh_data()` that:
  - Checks if cache is still valid - if so, return immediately (cache hit)
  - If cache expired or empty:
    - Loop through all 5 competition codes
    - Call `fetch_recent_matches()` for each
    - Normalize each match using `normalize_match()`
    - Group all matches using `group_by_competition()`
    - Update cache with new data and current timestamp
    - Log the refresh operation
  - Return success/failure status
- Method `get_matches()` that:
  - Returns cached data if available
  - Returns empty dict if no data
- Handle API failures gracefully:
  - If some competitions fail, still cache the successful ones
  - Log errors but don't crash

Example usage:
```python
service = MatchDataService(api_key=Config.API_KEY, cache_ttl=Config.CACHE_TTL)
service.refresh_data()
matches = service.get_matches()
```

This service layer decouples the Flask app from API and cache details.
```

---

### Prompt 17: Integration - Connect Service to Flask Route

```
Update `app.py` to use the `MatchDataService` instead of mock data.

Requirements:
- Import `MatchDataService` and `Config`
- Create a global service instance: `data_service = MatchDataService(Config.API_KEY, Config.CACHE_TTL)`
- Update the `/` route to:
  - Call `data_service.refresh_data()` (this checks cache internally)
  - Get matches using `data_service.get_matches()`
  - Calculate relative time for "last updated" display
    - Get cache age using `data_service.cache.get_age_seconds()`
    - Format as "X minutes ago" or "X hours ago"
  - Set `error = False` (we'll add error handling next)
  - Pass all data to template
- Add try-except around refresh call:
  - If exception occurs, log it
  - Set `error = True`
  - Still get and display cached data if available

Template variables to pass:
- `competitions`: dict of matches
- `last_updated`: formatted string like "12 minutes ago"
- `error`: boolean flag

Example route logic:
```python
@app.route('/')
def index():
    error = False
    try:
        data_service.refresh_data()
    except Exception as e:
        logger.error(f"Error refreshing data: {e}")
        error = True
    
    competitions = data_service.get_matches()
    
    # Calculate relative time
    age = data_service.cache.get_age_seconds()
    if age:
        minutes = int(age / 60)
        last_updated = f"{minutes} minutes ago"
    else:
        last_updated = "Never"
    
    return render_template('index.html', 
                          competitions=competitions,
                          last_updated=last_updated,
                          error=error)
```

Test with actual API calls - you should see real match data!
```

---

### Prompt 18: Final Polish and Error Handling

```
Add final error handling, logging improvements, and edge case handling across all modules.

Requirements:

**In `app.py`:**
- Add startup logging: log when app starts and service initializes
- Improve error handler to show user-friendly 500 page
- Add better relative time formatting (handle hours, days)
- Log every request to index route with cache status

**In `data_service.py`:**
- Add detailed logging for each competition fetch (success/failure)
- Handle case where ALL competitions fail: return empty but don't crash
- Add method to get cache metadata (age, validity) for debugging

**In `football_api.py`:**
- Add timeout to requests (e.g., 10 seconds)
- Handle network errors specifically (ConnectionError, Timeout)
- Add retry logic: retry once on failure after 2 second delay

**In `templates/index.html`:**
- Improve error banner styling (make it more visible)
- Add empty state message when no matches: "No matches found in the last 72 hours"
- Ensure banner is properly shown/hidden based on error flag

**Testing checklist:**
1. App starts successfully
2. First load fetches data from API
3. Second load within 30 min uses cache
4. After 30 min, refetches data
5. If API is unreachable, shows error banner but displays cached data
6. If no data at all, shows empty state gracefully
7. Match clicks open Google search in new tab
8. Page auto-refreshes after 30 minutes

**Add a README.md with:**
- Setup instructions
- Environment variables needed
- How to run the app
- API key setup instructions
- Dependencies list

This completes the implementation. All modules should now work together seamlessly!
```

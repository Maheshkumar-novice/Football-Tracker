# 📌 Football Matches Tracker — Full Specification (Developer-Ready)

## 1. Project Summary

Football Matches Tracker is a lightweight Flask web app that displays **recent football match results (last 72 hours)** across the **top 5 European leagues**, refreshing automatically every 30 minutes. It retrieves match data from **Football-Data.org (Free Tier)** and emphasizes clean UI, fast loading, and minimal interaction.

---

## 2. Supported Competitions

| Competition    | Code |
| -------------- | ---- |
| Premier League | PL   |
| La Liga        | PD   |
| Bundesliga     | BL1  |
| Serie A        | SA   |
| Ligue 1        | FL1  |

Only matches from these 5 competitions are displayed.

---

## 3. Functional Requirements

### 3.1 Match Data Rules

* Show **only recent matches** from the **last 72 hours**.
* Only the following fields are shown in UI:

  * Competition name (header only)
  * Match date (formatted)
  * Home team
  * Away team
  * Score or status

### 3.2 Score / Status Display Logic

| Match Status | Display in score column |
| ------------ | ----------------------- |
| FINISHED     | Score (e.g., `2–1`)     |
| LIVE         | `LIVE`                  |
| SCHEDULED    | `SCHEDULED`             |
| Others       | `SCHEDULED`             |

### 3.3 Match Click Behavior

Clicking on a match opens a new browser tab with a Google search using this format:

```
"Competition Name Home Team vs Away Team"
```

---

## 4. UI / UX Specifications

### 4.1 Page Layout

* Single scrolling page — no tabs, pagination, or controls.
* Group matches **by competition**.
* Within each competition, order is **reverse chronological (most recent first)**.

### 4.2 Match Row Format

```
Date • Home Team vs Away Team • Score/Status
```

Date format: **`Weekday, Month Day`** (e.g., `Sat, Nov 15`)

If team names are long → allow text wrapping (no truncation or abbreviations).

### 4.3 Header

Displayed above match list:

```
Football Matches Tracker
Recent Results — Last 72 Hours
Last updated: {relative time}   (e.g., "12 minutes ago")
```

### 4.4 Error Banner

If data refresh fails:

* Display **red bar at the very top**:

  > `Error fetching match data. Showing cached results.`
* Continue rendering cached results normally.

### 4.5 Footer

```
Data provided by Football-Data.org
```

### 4.6 Theme / Design

* **Light mode only**
* Visual style tier: **light structure**

  * Subtle row separators or alternating row backgrounds
  * Competition headers styled as **section bars**:

    ```
    ▌ Premier League
    ```
* Moderate spacing for readability.

---

## 5. Auto-Refresh Behavior

* Auto refresh every **30 minutes** using **JS timer + full page reload**.
* No loading indicator.
* Cached data is used without an API call if cache is still valid.

---

## 6. Backend Architecture

### 6.1 Tech Stack

| Layer         | Technology              |
| ------------- | ----------------------- |
| Backend       | Flask (Python)          |
| Frontend      | HTML + CSS + JS         |
| Data Provider | Football-Data.org API   |
| Caching       | In-memory Python object |
| Logging       | File + console          |

### 6.2 Directory Structure

```
/project
  app.py
  cache.py
  football_api.py
  logging_config.py
  templates/
    index.html
  static/
    styles.css
    script.js
```

### 6.3 Internal Match Object Format

Data normalized before caching:

```python
{
  "competition_code": "PL",
  "competition_name": "Premier League",
  "utc_kickoff": "2025-11-15T17:30:00Z",
  "display_date": "Sat, Nov 15",
  "home_team": "Arsenal",
  "away_team": "Chelsea",
  "status": "FINISHED",
  "score_text": "2–1",  # or LIVE / SCHEDULED
  "google_query": "Premier League Arsenal vs Chelsea"
}
```

### 6.4 Cached Structure

```python
{
  "last_updated": <UTC timestamp>,
  "competitions": {
    "PL": [match_objects],
    "PD": [match_objects],
    "BL1": [match_objects],
    "SA": [match_objects],
    "FL1": [match_objects]
  }
}
```

Cache lifetime: **30 minutes**, in-memory only.

Cache overwrite policy:

* **Only replace cache if API response timestamps are newer**.

---

## 7. API Integration Details

### 7.1 Request Strategy

* **One request per competition**
* Use **API date range filtering**:

  * From = now − 72 hours (UTC)
  * To = now (UTC)

### 7.2 Required Fields to Extract

From API response:

* Competition name
* Match kickoff datetime
* Home + away team names
* Full-time score (if finished)
* Status

### 7.3 API Header

```
X-Auth-Token: {env variable FOOTBALL_API_KEY}
```

---

## 8. Environment & Configuration

All configuration via **environment variables**:

| Variable           | Purpose                                  |
| ------------------ | ---------------------------------------- |
| `FOOTBALL_API_KEY` | Auth token                               |
| `CACHE_TTL`        | Default 1800 seconds (optional override) |
| `LOG_LEVEL`        | Default `INFO`                           |

---

## 9. Logging Requirements

### 9.1 Default Level

`INFO`

### 9.2 Log Content

* API requests & responses (status only, not full body)
* Cache hits / misses
* Refresh cycles
* Errors

### 9.3 Output Destinations

* Console
* `app.log` file (single file, no rotation)

---

## 10. Error Handling Rules

| Scenario                | User Sees            | Logged | Backend Uses      |
| ----------------------- | -------------------- | ------ | ----------------- |
| API OK                  | Normal page          | INFO   | New data          |
| API fails & cache valid | Banner               | ERROR  | Cached data       |
| API fails & no cache    | Banner + empty lists | ERROR  | Nothing available |

---

## 11. Performance Requirements

* Long lists allowed — no pagination.
* No stress scaling required for V1 — **single-user local environment** assumed.
* Startup must fetch if cache empty; otherwise show cached data.

---

## 12. Future-Ready Notes (not part of V1)

Not implemented now, but architecture enables future upgrades:

* Tabbed navigation
* JSON API endpoints
* Dark mode
* WebSockets or AJAX incremental updates
* Team logos
* Deployments with multi-process cache (Redis, SQLite, etc.)

---

# Football Matches Tracker — Idea Document

## 1. Project Overview
Football Matches Tracker is a lightweight web application that displays recent football match results and upcoming fixtures in one minimal interface. The application is designed to save football fans from repeatedly searching online for scores and match information.

## 2. Objective
Provide a clean, responsive, mobile-friendly UI that shows recent match results and scheduled fixtures across supported football competitions, using the **Football-Data.org API (Free Plan)** as the sole data source.

## 3. Motivation
Users often have to search multiple sources manually to find match details and results. This application consolidates the essential information into a single screen without unnecessary statistics or noise.

## 4. Tech Stack
| Layer | Technology |
|-------|-------------|
| Backend | Flask (Python) |
| Frontend | HTML, CSS, JavaScript |
| Data Provider | https://www.football-data.org/ API |
| Deployment (future) | Not specified; should allow scaling |

## 5. Core Features
| Feature | Description |
|--------|-------------|
| Match Display | Show recently completed matches + upcoming fixtures across supported competitions |
| Match Redirect Action | Clicking a match opens a Google search with an appropriate query (e.g., `"TeamA vs TeamB score"`) |
| Auto Refresh | Data refreshes automatically every **30 minutes** |
| Caching | Cache API results for **30 minutes** to limit API calls and stay within free-tier restrictions |
| Logging | Thorough logging for API calls, refresh cycles, cache usage, and errors |
| Responsive Layout | Minimal and mobile-friendly UI with no visual clutter |

## 6. API Usage Notes
- The API Key must be included via the `X-Auth-Token` header.
- API documentation:
  - https://www.football-data.org/documentation/quickstart/
  - https://docs.football-data.org/general/v4/resources.html
  - https://docs.football-data.org/general/v4/match.html
  - https://www.football-data.org/pricing

### Free-Plan Constraints
- **10 API calls per minute**
- **Scores & schedules are delayed**
- **League tables available**
- Access to the following **12 competitions only**:
  - WC, CL, BL1, DED, BSA, PD, FL1, ELC, PPL, EC, SA, PL

### Minimum Data Needed from API
To keep the UI minimal and usage efficient, only fetch:
- Competition name
- Match date and time
- Home and away teams
- Full-time score (if match is finished)
- Match status (`SCHEDULED`, `LIVE`, `FINISHED`, etc.)

## 7. Error Handling & Reliability
- If API calls fail, fallback to cached data rather than breaking the UI.
- UI should display the timestamp of the last refresh.
- Logs must record:
  - API request + response status
  - Cache hits / misses
  - Auto-refresh runs
  - Errors and fallback conditions

## 8. Out-of-Scope for Initial Version
The following features will **not** be included initially to maintain project focus:
- Historical match browsing
- Player statistics
- Live commentary streams
- Predictive analytics
- Fantasy or betting integrations
- Data outside free-tier competitions

## 9. Basic User Flow
1. User opens the application.
2. The UI loads matches from cache or fetches new data if cache expired.
3. Clicking a match opens a Google search tab with a predefined query.
4. The system automatically refreshes match data every 30 minutes.

---

**End of document**

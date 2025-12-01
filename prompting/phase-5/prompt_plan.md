# Phase 5 Prompt Plan: League Standings

## 1. Goal
Implement the **League Standings** feature, displaying the full table (all teams) for each competition.

## 2. Backend Implementation

### 2.1 `football_api.py`
-   **Add Method**: `fetch_standings(self, competition_code)`
    -   Endpoint: `/competitions/{code}/standings`
    -   Returns: JSON response or `None`.

### 2.2 `cache.py`
-   **Update `MatchCache`**:
    -   Add `self.standings` to `__init__`.
    -   Add `set_standings(self, standings_dict)` and `get_standings(self)`.
    -   Update `clear()` to reset standings.

### 2.3 `data_service.py`
-   **Update `MatchDataService`**:
    -   Add `get_standings(self)` method.
    -   Update `refresh_data()` to fetch standings for all competitions.
    -   Extract the `TOTAL` table from the API response.
    -   Cache standings data.

### 2.4 `app.py`
-   **Update `index` route**:
    -   Call `data_service.get_standings()`.
    -   Pass `standings` dictionary to `render_template`.

## 3. Frontend Implementation

### 3.1 `templates/index.html`
-   **Add Standings Section**:
    -   Inside the `competition-section` loop.
    -   Below the `scorers-section`.
    -   Create a full-width table.
    -   Headers: Pos, Team, P, W, D, L, GF, GA, GD, Pts.

### 3.2 `static/styles.css`
-   **Style the Standings Table**:
    -   Compact rows.
    -   Responsive design (maybe hide W/D/L on very small screens if needed, but aim to keep them).
    -   Highlight "Points" column (bold).
    -   Use `nth-child` for striping if desired.

## 4. Verification Steps
1.  **Start App**: `uv run app.py`
2.  **Check UI**: Verify Standings table appears for each league below Top Scorers.
3.  **Check Data**: Verify points and stats match `test_standings.py` output.
4.  **Check Layout**: Ensure the table fits well and doesn't break the layout.

# Football Matches Tracker — Phase 5 Specification

## 1. Phase 5 Scope
Phase 5 introduces **League Standings** to the application.
The goal is to display the full league table for each competition, providing a comprehensive view of team performance.

## 2. Functional Requirements

### 2.1 Data Retrieval
-   **Endpoint**: `GET /competitions/{code}/standings`
-   **Scope**: Fetch for all 6 tracked competitions (PL, PD, BL1, SA, FL1, CL).
-   **Data Type**: Use the `TOTAL` table type.
-   **Fields**:
    -   Position (Rank)
    -   Team Name & Crest
    -   Played Games (P)
    -   Won (W)
    -   Draw (D)
    -   Lost (L)
    -   Goals For (GF)
    -   Goals Against (GA)
    -   Goal Difference (GD)
    -   Points (Pts)

### 2.2 UI Integration
-   **Placement**: Displayed **below the Top Scorers section** for each competition.
-   **Format**: A full-width data table.
-   **Rows**: Show **ALL teams** in the league (e.g., 20 rows for PL, 36 for CL). No "Show More" button; always expanded.
-   **Columns**: Rank, Team, P, W, D, L, GF, GA, GD, Pts.
-   **Styling**:
    -   Compact rows to manage vertical space.
    -   Clear headers.
    -   Highlight the "Points" column.

### 2.3 AI Integration
-   **None**: The AI Summary will **NOT** include standings analysis, as requested.

## 3. Technical Implementation

### 3.1 Backend
-   **`football_api.py`**: Add `fetch_standings(competition_code)` method.
-   **`data_service.py`**:
    -   Update `refresh_data` to fetch standings.
    -   Cache standings data (key: `standings_{code}`).
    -   Add `get_standings()` method.
-   **`app.py`**: Pass standings data to the template.

### 3.2 Frontend
-   **`templates/index.html`**: Add the Standings table loop within each `competition-section`.
-   **`static/styles.css`**: Add styles for the standings table (responsive, compact).

## 4. Acceptance Criteria
-   [ ] Full league table displayed for each competition.
-   [ ] All columns (P, W, D, L, GF, GA, GD, Pts) are visible.
-   [ ] UI is clean and legible despite the density of data.
-   [ ] AI Summary remains unchanged (no standings data sent to AI).

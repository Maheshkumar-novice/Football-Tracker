# Football Matches Tracker — Phase 4 Specification

## 1. Phase 4 Scope
Phase 4 introduces **Top Scorer Statistics** to the application.
The goal is to provide context on player performance alongside match results and integrate this data into the AI summaries.

## 2. Functional Requirements

### 2.1 Data Retrieval
-   **Endpoint**: `GET /competitions/{code}/scorers`
-   **Scope**: Fetch for all 6 tracked competitions (PL, PD, BL1, SA, FL1, CL).
-   **Fields**:
    -   Player Name
    -   Team Name
    -   Goals
    -   Assists (if available)
-   **Limit**: Fetch/Display the **Top 10** scorers per competition.

### 2.2 UI Integration
-   **Placement**: Displayed **below the match list** for each competition section.
-   **Format**: A compact table or list view.
    -   Columns: Rank, Player (Team), Goals, Assists.
-   **Styling**: Consistent with the existing card/section design.
-   **Empty State**: If no scorer data is available, hide the section or show "No scorer data available".

### 2.3 AI Integration
-   **Prompt Update**:
    -   Include Top Scorer data in the JSON payload sent to Anthropic.
    -   Instruct the AI to mention significant changes in the Golden Boot race (e.g., "Haaland extends lead").
-   **Context**: The AI should use this data to add depth to the "News Stories" (e.g., mentioning a player's season total when reporting on their goal in a match).

## 3. Technical Implementation

### 3.1 Backend
-   **`football_api.py`**: Add `fetch_top_scorers(competition_code)` method.
-   **`data_service.py`**:
    -   Update `get_matches()` (or create `get_data()`) to fetch both matches and scorers.
    -   Cache scorer data (can use same TTL as matches).
-   **`app.py`**: Pass scorer data to the template.
-   **`ai_summary.py`**: Update `generate_summary` to accept and process scorer data.

### 3.2 Frontend
-   **`templates/index.html`**: Add a loop to render the Top Scorers list within each `competition-section`.
-   **`static/styles.css`**: Add styles for the scorers table/list (compact, readable).

## 4. Acceptance Criteria
-   [ ] Top 10 scorers displayed for each competition (where available).
-   [ ] Goals and Assists are visible.
-   [ ] AI Summary includes context about top scorers.
-   [ ] UI looks clean and integrated (not cluttered).

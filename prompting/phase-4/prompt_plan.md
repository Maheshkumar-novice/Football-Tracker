# Phase 4 Prompt Plan: Top Scorers

## 1. Goal
Implement the **Top Scorers** feature, displaying the top 10 scorers (goals + assists) for each competition and integrating this data into the AI summaries.

## 2. Backend Implementation

### 2.1 `football_api.py`
-   **Add Method**: `fetch_top_scorers(self, competition_code, limit=10)`
    -   Endpoint: `/competitions/{code}/scorers`
    -   Params: `limit={limit}`
    -   Returns: JSON response or `None`.

### 2.2 `data_service.py`
-   **Update `MatchDataService`**:
    -   Add `get_scorers(self)` method.
    -   Orchestrate fetching scorers for all competitions.
    -   **Caching**: Store scorer data in `self.cache` (key: `scorers_{code}`).
    -   **Refresh Logic**: Update `refresh_data` to also fetch scorers.

### 2.3 `app.py`
-   **Update `index` route**:
    -   Call `data_service.get_scorers()`.
    -   Pass `scorers` dictionary to `render_template`.
-   **Update `generate_summary` route**:
    -   Retrieve scorer data.
    -   Pass it to `summary_generator.generate_summary`.

### 2.4 `ai_summary.py`
-   **Update `generate_summary`**: Accept `scorers_data` argument.
-   **Update `_build_prompt`**:
    -   Include `scorers_data` in the JSON payload.
    -   Update `user_prompt` to ask the AI to mention key scorer stats if relevant to the news stories.

## 3. Frontend Implementation

### 3.1 `templates/index.html`
-   **Add Scorer Section**:
    -   Inside the `competition-section` loop.
    -   Below the `matches-container`.
    -   Create a collapsible or compact view for "Top Scorers".
    -   Table columns: Rank, Player, Team, Goals, Assists.

### 3.2 `static/styles.css`
-   **Style the Scorer Section**:
    -   Compact font size.
    -   Subtle background.
    -   Clean table layout.

## 4. Verification Steps
1.  **Start App**: `uv run app.py`
2.  **Check UI**: Verify Top Scorers list appears for each league.
3.  **Check Data**: Verify Goals and Assists are correct (compare with `test_top_scorers.py` output).
4.  **Check AI**: Generate a summary and check if it mentions top scorers (e.g., "Haaland").

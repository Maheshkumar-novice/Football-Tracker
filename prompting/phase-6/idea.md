## Phase 6: SQLite Caching & Background Refresh

**Goal**: Replace in-memory caching with a persistent SQLite database and implement a background scheduler for data updates.

**Features**:
-   **SQLite Database**: Store Matches, Top Scorers, and Standings in a local `.db` file.
-   **Background Scheduler**: Automatically fetch fresh data every 30 minutes.
-   **Startup Check**: Fetch data immediately on app startup if the cache is empty.
-   **Rate Limiting**: Ensure background updates respect API limits (10 req/min).
-   **UI**: Always serve data from the database (fast load times).

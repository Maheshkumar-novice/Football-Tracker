# Football Matches Tracker — Phase 6 Specification

## 1. Phase 6 Scope
Phase 6 introduces **Persistent Caching** using SQLite and **Background Updates** to ensure data is always available and up-to-date without user intervention.

## 2. Functional Requirements

### 2.1 SQLite Caching
-   **Storage**: Use a local SQLite database (`football_data.db`).
-   **Schema**:
    -   `matches`: `competition_code` (PK), `data_json` (TEXT), `updated_at` (DATETIME).
    -   `scorers`: `competition_code` (PK), `data_json` (TEXT), `updated_at` (DATETIME).
    -   `standings`: `competition_code` (PK), `data_json` (TEXT), `updated_at` (DATETIME).
-   **Data Access**: The app always reads from the database.

### 2.2 Background Refresh
-   **Scheduler**: Use `APScheduler` to run a data refresh job every **30 minutes**.
-   **Rate Limiting**: Strictly enforce delays (e.g., 7s) between API calls to respect the 10 req/min limit.
-   **Error Handling**: If a job fails, **retry once** after 1 minute. If it fails again, wait for the next scheduled run.

### 2.3 Startup Behavior
-   **Initial Fetch**: On application startup, check if the database is empty.
-   **Blocking**: If empty, perform a full data fetch **synchronously** before starting the Flask server. This ensures the user never sees an empty state.
-   **Logging**: Log progress clearly during the initial fetch.

## 3. Technical Implementation

### 3.1 Dependencies
-   Add `APScheduler` to `pyproject.toml`.

### 3.2 Database Manager (`db_manager.py`)
-   Create a new module to handle SQLite connections and queries.
-   Methods: `init_db`, `save_matches`, `get_matches`, etc.

### 3.3 Data Service Updates (`data_service.py`)
-   Remove in-memory `MatchCache`.
-   Integrate `db_manager`.
-   Refactor `refresh_data` to write to SQLite.
-   Add `update_job` function for the scheduler.

### 3.4 Application Entry Point (`app.py`)
-   Initialize `APScheduler`.
-   Run `data_service.refresh_data()` on startup if DB is empty.
-   Start the scheduler.

## 4. Acceptance Criteria
-   [ ] `football_data.db` file is created.
-   [ ] App starts with data pre-loaded (if fresh install).
-   [ ] Data refreshes automatically in the background every 30 mins.
-   [ ] UI loads instantly from local DB.
-   [ ] No 429 errors in logs during refresh cycles.

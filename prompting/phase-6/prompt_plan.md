# Phase 6 Prompt Plan: SQLite Caching & Background Refresh

## 1. Goal
Replace in-memory caching with SQLite and implement automated background updates.

## 2. Dependencies
-   **Action**: Add `APScheduler` to `pyproject.toml`.
-   **Command**: `uv add APScheduler`

## 3. Database Implementation (`db_manager.py`)
-   **Create Module**: `db_manager.py`
-   **Class**: `DatabaseManager`
-   **Methods**:
    -   `__init__(self, db_path)`
    -   `init_db(self)`: Create tables (`matches`, `scorers`, `standings`) if not exist.
    -   `save_matches(self, competition_code, data)`
    -   `get_matches(self, competition_code)`
    -   `save_scorers(self, competition_code, data)`
    -   `get_scorers(self, competition_code)`
    -   `save_standings(self, competition_code, data)`
    -   `get_standings(self, competition_code)`
    -   `is_empty(self)`: Check if any data exists.

## 4. Data Service Refactor (`data_service.py`)
-   **Imports**: Remove `MatchCache`, add `DatabaseManager`.
-   **Init**: Initialize `DatabaseManager` instead of `MatchCache`.
-   **`refresh_data(self)`**:
    -   Keep the fetching logic (with rate limits).
    -   Replace `cache.set_data` calls with `db.save_matches`, etc.
-   **Getters**: Update `get_matches`, etc., to call `db.get_matches`.

## 5. Application Integration (`app.py`)
-   **Imports**: Add `BackgroundScheduler` from `apscheduler.schedulers.background`.
-   **Startup Logic**:
    -   Initialize `scheduler`.
    -   Check `data_service.db.is_empty()`.
    -   If empty, call `data_service.refresh_data()` *before* `app.run()`.
    -   Add job: `scheduler.add_job(data_service.refresh_data, 'interval', minutes=30)`.
    -   Start scheduler.

## 6. Verification Steps
1.  **Clean Slate**: Delete existing `football_data.db` (if any).
2.  **Startup**: Run `uv run python app.py`.
3.  **Check 1**: Verify "Initializing data..." logs appear and server waits.
4.  **Check 2**: Verify `football_data.db` is created and populated.
5.  **Check 3**: Verify UI loads data.
6.  **Check 4**: Wait 30 mins (or temporarily set to 1 min) to verify background refresh works.

# Phase 16 Specification

## File Operations

### Delete
-   `/home/elliot/Documents/football-tracker/ai_summary.py`
-   `/home/elliot/Documents/football-tracker/cache.py`
-   `/home/elliot/Documents/football-tracker/mockup.html`

### Move
-   `inspect_match_data.py` -> `development_scripts/inspect_match_data.py`
-   `check_db.py` -> `development_scripts/check_db.py`
-   `test_api.py` -> `development_scripts/test_api.py`
-   `test_standings.py` -> `development_scripts/test_standings.py`
-   `test_top_scorers.py` -> `development_scripts/test_top_scorers.py`

## Code Improvements

### `app.py`
-   Review imports.
-   Ensure `debug=True` is controlled by config or env var (it is currently hardcoded in `__main__`).

### `config.py`
-   Ensure `API_KEY` is loaded from env.

### `data_processor.py`
-   Check for magic strings.

## Testing
-   After moving tests, create `tests/__init__.py` (optional for pytest but good practice).
-   Run `uv run pytest` (or `python -m pytest`) to verify tests still pass.

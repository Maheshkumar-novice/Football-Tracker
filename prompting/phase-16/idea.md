# Phase 16: Code Cleanup & Organization

## Goal
Inspect code, clear tech debt, and organize the codebase.

## Actions

### 1. Remove Unused Files
-   `ai_summary.py`: Legacy file, no longer used.
-   `cache.py`: Unused caching module.
-   `mockup.html`: Initial mockup, no longer needed.

### 2. Organize Directory Structure
-   **Development Scripts**: Move `inspect_match_data.py`, `check_db.py`, `test_api.py`, `test_standings.py`, `test_top_scorers.py` to `development_scripts/`.

### 3. Code Inspection & Tech Debt
-   **`app.py`**: Check for hardcoded values, ensure clean imports.
-   **`config.py`**: Ensure all secrets/constants are here.
-   **Docstrings**: Add missing docstrings to key functions in `data_processor.py` and `db_manager.py`.

## Verification
-   Run tests after moving them (might need to adjust imports).
-   Run app to ensure no broken imports.

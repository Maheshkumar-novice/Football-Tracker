# Phase 16 Prompt Plan

## Goal
Clean up and organize the codebase.

## Steps

### 1. Delete Unused Files
-   Delete `ai_summary.py`, `cache.py`, `mockup.html`.

### 2. Organize Files
-   Create `development_scripts/` directory.
-   Move script and test files to `development_scripts/`.

### 3. Code Inspection
-   Read `app.py` and `config.py`.
-   Refactor if necessary (e.g., move debug flag to config).

### 4. Verification
-   Run `uv run pytest` to ensure tests pass (might need to fix imports in tests).
-   Run `uv run python app.py` to ensure app starts.

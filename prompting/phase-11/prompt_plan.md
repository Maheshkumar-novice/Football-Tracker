# Phase 11 Prompt Plan

## Goal
Automate AI summary and limit to 10 lines.

## Steps

### 1. Update Database Manager
-   Modify `db_manager.py`.
-   Add `app_metadata` table.
-   Add `save_summary` and `get_summary` methods.

### 2. Update AI Generator
-   Modify `ai_summary.py`.
-   Update prompt to request "Exactly 10 lines of important match news".

### 3. Update App Logic
-   Modify `app.py`.
-   Update `scheduled_refresh` to generate and save summary.
-   Update `index` route to fetch and pass summary.
-   Remove `/generate-summary` route (optional, or just unused).

### 4. Update Frontend
-   Modify `templates/partials/header.html` (remove button).
-   Modify `templates/partials/ai_summary.html` (display summary directly).
-   Modify `static/script.js` (remove button listener).

### 5. Verification
-   Restart server.
-   Wait for initial refresh (or trigger one).
-   Verify summary appears automatically and is ~10 lines.

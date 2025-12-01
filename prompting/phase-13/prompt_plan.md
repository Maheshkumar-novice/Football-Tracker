# Phase 13 Prompt Plan

## Goal
Refine UI, remove unused JS, and improve match sorting.

## Steps

### 1. Refine Scorers Table
-   Modify `templates/partials/scorers.html`.
-   Apply `table-container` and `table` classes.
-   Match the `standings.html` layout (rank, player/team, goals, assists).

### 2. Remove marked.js
-   Modify `templates/index.html` (or `base.html`).
-   Remove the script tag.

### 3. Update Match Sorting
-   Modify `data_processor.py`.
-   Update `group_by_competition` to sort by `(is_finished, date)` descending.

### 4. Verification
-   Restart server.
-   Verify Scorers table looks like Standings table.
-   Verify `marked.js` is not loaded (view source).
-   Verify matches are sorted correctly (Finished/Live first, then by date).

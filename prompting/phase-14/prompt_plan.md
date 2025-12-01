# Phase 14 Prompt Plan

## Goal
Convert Recent Matches to a table layout.

## Steps

### 1. Update Matches Partial
-   Modify `templates/partials/matches.html`.
-   Replace card layout with `<table>` structure.
-   Columns: Date, Home, Away, Result, Status, Link.

### 2. Update CSS
-   Modify `static/styles.css`.
-   Add styles for `.team-info` (flexbox for crest + name).
-   Add styles for status colors (optional but nice).
-   Ensure table responsiveness.

### 3. Verification
-   Restart server (optional, template changes might reload automatically but safer to restart).
-   Verify "Recent Matches" is a table.
-   Verify all columns are present and correct.
-   Verify Google Link works.

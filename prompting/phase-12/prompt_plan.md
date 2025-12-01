# Phase 12 Prompt Plan

## Goal
Remove AI features and split scorers columns.

## Steps

### 1. Update Scorers Table
-   Modify `templates/partials/scorers.html`.
-   Implement separate Goals and Assists columns.

### 2. Clean Up App Logic
-   Modify `app.py`.
-   Remove `AISummaryGenerator` import and usage.
-   Remove AI logic from `scheduled_refresh`.
-   Remove AI variables from `index` route.

### 3. Clean Up Config
-   Modify `config.py`.
-   Remove Anthropic keys and flags.

### 4. Clean Up Templates
-   Modify `templates/index.html` (remove include).
-   Modify `templates/partials/header.html` (remove comments).

### 5. Delete Files
-   Delete `ai_summary.py`.
-   Delete `templates/partials/ai_summary.html`.

### 6. Verification
-   Restart server.
-   Verify scorers table has 4 columns (#, Player, Goals, Assists).
-   Verify no errors related to missing AI modules.

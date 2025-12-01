# Phase 10 Prompt Plan

## Goal
Implement compact header and move AI button.

## Steps

### 1. Update Header Partial
-   Modify `templates/partials/header.html`.
-   Implement the flexbox structure with Title and Button.

### 2. Update AI Summary Partial
-   Modify `templates/partials/ai_summary.html`.
-   Remove the button and header, keep only the content div.

### 3. Update CSS
-   Modify `static/styles.css`.
-   Add `.compact-header`, `.header-title-group`, `.btn-compact` styles.
-   Adjust font sizes.

### 4. Verification
-   Restart server.
-   Verify layout is single row.
-   Verify button still works (JS targets ID `generate-summary-btn`, so it should work if ID is preserved).

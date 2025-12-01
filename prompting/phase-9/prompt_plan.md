# Phase 9 Prompt Plan

## Goal
Implement clickable match cards and single-column layout.

## Steps

### 1. Update Matches Partial
-   Modify `templates/partials/matches.html`.
-   Wrap `.match-card` in an `<a>` tag pointing to Google Search.
-   Use `{{ match.google_query }}`.

### 2. Update CSS
-   Modify `static/styles.css`.
-   Change `.tab-content.active` to use a single column layout (`grid-template-columns: 1fr`).
-   Add styles for the match link (remove underline, inherit color).

### 3. Verification
-   Restart server (to reload templates).
-   Verify clicking a match opens Google.
-   Verify layout is single column on desktop.

# Phase 8 Prompt Plan: Frontend Refactoring

## Goal
Refactor `index.html` into a modular structure using Jinja2 templates and partials.

## Steps

### 1. Setup & Base Template
-   Create `templates/partials/` directory.
-   Create `templates/base.html` with the common HTML structure (`head`, `body`, `scripts`).

### 2. Extract Components
-   Extract Header to `templates/partials/header.html`.
-   Extract Footer to `templates/partials/footer.html`.
-   Extract AI Summary to `templates/partials/ai_summary.html`.
-   Extract Tabs Navigation to `templates/partials/tabs.html`.
-   Extract Matches List to `templates/partials/matches.html`.
-   Extract Top Scorers to `templates/partials/scorers.html`.
-   Extract Standings to `templates/partials/standings.html`.

### 3. Update Index
-   Rewrite `templates/index.html` to extend `base.html` and include the partials.

### 4. Cleanup
-   Review `static/styles.css` and remove any unused legacy styles.

### 5. Verification
-   Restart server (to pick up new templates).
-   Verify UI functionality (Tabs, Sort, Filter, AI Summary).

# Phase 15 Prompt Plan

## Goal
Refactor CSS into modular files.

## Steps

### 1. Setup
-   Create `static/css/` directory.

### 2. Create CSS Files
-   Create `static/css/variables.css`.
-   Create `static/css/reset.css`.
-   Create `static/css/layout.css`.
-   Create `static/css/components.css`.
-   Create `static/css/tables.css`.
-   Create `static/css/utils.css`.
-   *Note*: I will read `static/styles.css` first to ensure I copy everything correctly and don't lose anything.

### 3. Update Main CSS
-   Overwrite `static/styles.css` with `@import` statements.

### 4. Verification
-   Restart server (CSS changes might need hard refresh or restart if static files are cached).
-   Verify the app looks exactly the same.
-   Check browser network tab to see imports loading.

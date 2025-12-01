# Phase 17 Prompt Plan

## Goal
Make tables responsive.

## Steps

### 1. Update CSS
-   Add `.hide-mobile` media query to `static/css/utils.css`.
-   Adjust table padding/font-size for mobile in `static/css/tables.css`.

### 2. Update Templates
-   `templates/partials/matches.html`: Add `.hide-mobile` to Status and Link columns.
-   `templates/partials/standings.html`: Add `.hide-mobile` to GF, GA, GD columns.

### 3. Verification
-   Restart app.
-   Use browser tool with mobile viewport size (e.g., 375x812) to verify columns are hidden and layout fits.

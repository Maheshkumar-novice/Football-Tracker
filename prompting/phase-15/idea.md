# Phase 15: CSS Refactor

## Goal
Refactor the monolithic `styles.css` into multiple, logical CSS files to improve maintainability and organization.

## Strategy
1.  **Create Directory**: `static/css/`.
2.  **Split Files**:
    -   `variables.css`: CSS variables (colors, fonts).
    -   `reset.css`: Global reset and body styles.
    -   `layout.css`: Header, Footer, Main Container, Tabs, Grid.
    -   `components.css`: Buttons, Banners, Cards, Sections.
    -   `tables.css`: Styles for Matches, Scorers, and Standings tables.
    -   `utils.css`: Utility classes (status colors, helpers).
3.  **Main Entry Point**: `static/styles.css` will use `@import` to load these files.
    -   *Alternative*: Update `base.html` to link multiple files.
    -   *Decision*: `@import` in `styles.css` is cleaner for `base.html` and allows us to keep the existing `<link href="styles.css">`.

## Cleanup
-   Remove unused CSS (e.g., old AI summary styles, legacy match card styles if fully replaced by table).

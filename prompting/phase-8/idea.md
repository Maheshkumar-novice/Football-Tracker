# Phase 8: Frontend Refactoring & Modularization

## Goal
Refactor the existing monolithic `index.html` and associated CSS/JS into modular components (partials) to improve maintainability, readability, and scalability.

## Current State
- `index.html`: Contains everything (Header, AI Summary, Tabs, Matches, Scorers, Standings, Footer). ~200 lines.
- `styles.css`: ~700 lines, mixed concerns.
- `script.js`: ~100 lines, handles tabs, list.js, and AI summary.

## Proposed Changes

### 1. HTML Modularization (Jinja2 Partials)
Create a `templates/partials/` directory and extract reusable components:

-   `layout.html`: Base template with `<head>`, `<body>`, scripts, and styles.
-   `partials/header.html`: Title and Last Updated.
-   `partials/footer.html`: Copyright/Data source.
-   `partials/ai_summary.html`: The AI Summary section (button + content).
-   `partials/tabs_nav.html`: The tab buttons navigation.
-   `partials/matches_list.html`: The "Recent Matches" list.
-   `partials/scorers_table.html`: The "Top Scorers" table.
-   `partials/standings_table.html`: The "League Table" with sort/filter.

`index.html` will then just extend `layout.html` and include these partials.

### 2. CSS Organization
-   Review `styles.css` for unused styles (from the old vertical layout).
-   Group styles logically (Layout, Components, Utilities).
-   Ensure `:root` variables are used consistently.

### 3. JS Refactoring
-   Ensure functions are well-documented.
-   Separate "Business Logic" (AI Summary) from "UI Logic" (Tabs, List.js).
-   Maybe split into `ui.js` and `api.js` if it grows, but for now, just organizing `script.js` with clear comments and sections is sufficient.

## Benefits
-   **Maintainability**: Easier to edit specific components without scrolling through a huge file.
-   **Reusability**: Components like `matches_list` could be reused in other views (e.g., a "Team Details" page in the future).
-   **Clarity**: Clear separation of concerns.

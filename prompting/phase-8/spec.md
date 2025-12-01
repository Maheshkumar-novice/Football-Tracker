# Phase 8 Specification: Frontend Refactoring

## 1. File Structure

```text
templates/
├── base.html             # Base layout (HTML shell, head, scripts)
├── index.html            # Main page (extends base, includes partials)
└── partials/
    ├── header.html       # App header
    ├── footer.html       # App footer
    ├── ai_summary.html   # AI Summary section
    ├── tabs.html         # Tab navigation buttons
    ├── match_card.html   # Single match card component (optional, or part of matches_list)
    ├── matches.html      # Recent Matches section
    ├── scorers.html      # Top Scorers section
    └── standings.html    # League Table section
```

## 2. Component Details

### `base.html`
-   `<!DOCTYPE html>`
-   `<head>` with meta tags, title, CSS links, JS CDNs (Marked.js, List.js).
-   `<body>` with a block for `content`.
-   Footer inclusion.
-   Script inclusion.

### `index.html`
-   Extends `base.html`.
-   Defines the `content` block.
-   Includes `header.html`.
-   Includes `ai_summary.html` (conditional).
-   Includes `tabs.html`.
-   Iterates through competitions to create tab content containers.
-   Inside tab content:
    -   Includes `matches.html`.
    -   Includes `scorers.html`.
    -   Includes `standings.html`.

### `partials/*.html`
-   **header.html**: `<h1>` and Last Updated.
-   **ai_summary.html**: The generate button and content div.
-   **tabs.html**: The loop generating tab buttons.
-   **matches.html**: The loop generating match cards.
-   **scorers.html**: The table for top scorers.
-   **standings.html**: The table for standings with search input.

## 3. CSS & JS
-   **CSS**: Clean up `styles.css`. Remove any legacy styles. Ensure `.left-col` and grid layouts are robust.
-   **JS**: No major logic changes, just ensure `openTab` and `List.js` init works with the new HTML structure (IDs and classes must match).

## 4. Verification
-   The app should look and behave **exactly the same** as before.
-   Verify all tabs, sorting, filtering, and AI summary still work.

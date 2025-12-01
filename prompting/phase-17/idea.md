# Phase 17: Responsive Tables

## Goal
Make the data tables (Matches, Standings, Scorers) look good on mobile devices.

## Current State
-   `overflow-x: auto` is present, so tables scroll horizontally.
-   However, scrolling isn't always the best UX. We can hide less critical columns on very small screens.

## Strategy
1.  **Matches Table**:
    -   Hide "Status" and "Link" on mobile (< 600px).
    -   Keep: Date, Home, Away, Result.
    -   Maybe shorten headers (Home Team -> Home).

2.  **Standings Table**:
    -   Hide "Played", "GF", "GA", "GD" on mobile.
    -   Keep: Rank, Team, W, D, L, Pts.
    -   Actually, "Played" is important. Maybe hide GF/GA/GD only.

3.  **Scorers Table**:
    -   Hide "Assists" if space is tight? Or just keep it as it's small.
    -   Maybe hide "Team" if it's too wide, but that's critical.

4.  **Styling**:
    -   Reduce padding on `td`/`th` for mobile.
    -   Reduce font size slightly.

## Implementation
-   Use CSS Media Queries in `static/css/tables.css`.
-   Add classes like `.hide-mobile` to specific columns in HTML?
-   Or use `nth-child` selectors in CSS (cleaner HTML, but more fragile if columns change).
-   *Decision*: Add utility class `.hide-mobile` to HTML columns is explicit and robust.

## Files to Modify
-   `templates/partials/matches.html`
-   `templates/partials/standings.html`
-   `templates/partials/scorers.html`
-   `static/css/tables.css` (or `utils.css`)

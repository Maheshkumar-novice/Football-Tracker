# Phase 14: Matches Table Refactor

## Goal
Convert the "Recent Matches" section from a list of cards to a structured table.

## Columns
1.  **Date**: Display date (e.g., "Mon, Nov 24").
2.  **Home Team**: Team name (with crest).
3.  **Away Team**: Team name (with crest).
4.  **Result**: Score (e.g., "0–1").
5.  **Status**: Match status (e.g., "FINISHED").
6.  **Link**: Link to Google Search.

## Changes
-   **Modify**: `templates/partials/matches.html`.
-   **Style**: Use `table-container` and `table` classes consistent with Standings and Scorers.
-   **Layout**:
    -   Use `<thead>` for column headers.
    -   Use `<tbody>` for match rows.
    -   Ensure responsive design (might need horizontal scroll on small screens, which `table-container` handles).

## Design Details
-   **Home Team / Away Team**: Align text to center or left? Usually Home is right-aligned and Away is left-aligned in scoreboards, but in a table, maybe just standard alignment. Let's try:
    -   Home Team: Right aligned (or standard left with crest).
    -   Away Team: Left aligned (or standard left with crest).
    -   Actually, standard table alignment (left) is safest for readability.
-   **Google Link**: A simple "Search" link or an external link icon.

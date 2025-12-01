# Phase 9 Specification

## 1. Templates (`templates/partials/matches.html`)
-   Wrap the content of `.match-card` in an anchor tag:
    ```html
    <a href="https://www.google.com/search?q={{ match.google_query }}" target="_blank" class="match-card-link">
        <div class="match-card">
            ...
        </div>
    </a>
    ```
-   OR, make the `.match-card` itself the anchor tag if styling permits (might need to adjust `display` properties).

## 2. Styles (`static/styles.css`)
-   **Layout**:
    -   Update `.tab-content.active`:
        -   Remove `grid-template-columns: 1fr 1.5fr`.
        -   Set `grid-template-columns: 1fr`.
    -   Ensure `.left-col` (Matches + Scorers) sits above `.standings-section` (Standings).
    -   Actually, since `.left-col` contains Matches and Scorers, and Standings is a separate sibling, a single column grid will stack them:
        1. Left Col (Matches, Scorers)
        2. Standings
    -   This matches the requirement "Matches, Top Scorers, and Standings in a single column".

-   **Match Link**:
    -   Style the anchor tag to remove text decoration and inherit colors.
    -   Ensure hover effects still work on the card.

## 3. Data
-   `google_query` is already fixed in `data_processor.py`.
-   No DB deletion.

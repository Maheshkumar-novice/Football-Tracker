# Phase 9: Clickable Matches & Single Column Layout

## Goals
1.  **Clickable Matches**: Restore the functionality where clicking a match card opens a Google search for that match.
2.  **Single Column Layout**: Simplify the UI by stacking "Recent Matches", "Top Scorers", and "League Table" vertically in a single column for ALL screen sizes (removing the split view).

## Implementation Details

### 1. Clickable Matches
-   Update `templates/partials/matches.html`.
-   Wrap the `.match-card` div in an `<a>` tag (or make the div clickable via JS/onclick, but `<a>` is better for accessibility and SEO).
-   Target URL: `https://www.google.com/search?q={{ match.google_query }}`.
-   Target attribute: `_blank` (to open in new tab).

### 2. Single Column Layout
-   Update `static/styles.css`.
-   Modify `.tab-content.active` grid definition.
-   Change `grid-template-columns: 1fr 1.5fr` to `grid-template-columns: 1fr` (or just `display: block`).
-   Ensure `.left-col` and `.standings-section` stack nicely with appropriate spacing.

## Constraints
-   **Do NOT delete the database**. The `google_query` fix in `data_processor.py` will apply to future data fetches. Existing data might have malformed queries, but we will proceed without wiping data.

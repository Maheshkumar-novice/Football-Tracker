# Phase 7: UI Overhaul & Configurable AI

## 1. Configurable AI Summary
**Goal**: Allow the AI Summary feature to be disabled via configuration.
-   **Mechanism**: Check `ANTHROPIC_API_KEY` or a specific `ENABLE_AI_SUMMARY` env var.
-   **UI Impact**: If disabled, hide the "Generate Summary" button and the summary section entirely.

## 2. UI Organization Brainstorming
**Problem**: The current "long scroll" layout is becoming unwieldy with the addition of Standings and Top Scorers.

### Option A: Tabbed Interface (Horizontal)
-   **Layout**: A row of tabs at the top (Premier League, La Liga, Bundesliga, etc.).
-   **Behavior**: Clicking a tab shows *only* that competition's data (Matches, Standings, Scorers).
-   **Pros**: Clean, familiar, saves vertical space.
-   **Cons**: Can get crowded on mobile if too many tabs.

### Option B: Sidebar Navigation (Vertical)
-   **Layout**: A fixed sidebar on the left with competition logos/names.
-   **Behavior**: Clicking a link scrolls to the section (if single page) or swaps the main content view.
-   **Pros**: Great for desktop, scalable for many leagues.
-   **Cons**: Takes up horizontal space, needs a hamburger menu on mobile.

### Option C: Dashboard + Drill-down
-   **Layout**: A "Home" view with a summary (e.g., just the top 3 matches and top 5 standings for each league).
-   **Behavior**: "View Details" buttons to go to a full page for that competition.
-   **Pros**: Less overwhelming at first glance.
-   **Cons**: More clicks to see specific data.

## 3. Table Operations
**Goal**: Make the Standings and Match tables interactive.

### Features
-   **Sorting**: Click column headers (e.g., "Pts", "GD", "Goals") to sort ascending/descending.
-   **Filtering**: A search bar above the table to filter by Team Name.
-   **Highlighting**: Hover effects on rows.

### Technical Approach
-   **Library**: Use a lightweight JS library like `List.js` or `Tablesort`, or write custom vanilla JS (preferred for learning/control).
-   **Implementation**:
    -   Add `data-sort` attributes to headers.
    -   Add a text input for filtering.

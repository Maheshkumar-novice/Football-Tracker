# Football Matches Tracker — Phase 7 Specification

## 1. Phase 7 Scope
Phase 7 focuses on improving the **User Interface** and making the **AI Summary** feature configurable.
The goal is to organize the growing amount of data (Matches, Scorers, Standings) into a cleaner, tabbed layout and add interactivity to tables.

## 2. Functional Requirements

### 2.1 UI Layout (Tabs)
-   **Structure**: Replace the long vertical scroll with a **Tabbed Interface**.
-   **Tabs**: One tab for each competition (e.g., "Premier League", "La Liga", etc.).
-   **Behavior**:
    -   Clicking a tab displays the content for that competition only.
    -   The selected tab is highlighted.
    -   Default to the first tab (Premier League) on load.

### 2.2 Table Features (Sort & Filter)
-   **Library**: Use `List.js` (via CDN) for table functionality.
-   **Standings Table**:
    -   **Sort**: Clickable headers for Points, GD, Goals, etc.
    -   **Filter**: Search bar to filter rows by Team Name.
-   **Match List**:
    -   **Filter**: Search bar to filter by Team Name.

### 2.3 Configurable AI Summary
-   **Configuration**: Add a new environment variable `ENABLE_AI_SUMMARY` (true/false).
-   **Logic**:
    -   If `ENABLE_AI_SUMMARY` is `false` OR `ANTHROPIC_API_KEY` is missing -> **Hide** the AI Summary section and button.
    -   If `true` AND key exists -> **Show** the UI.

## 3. Technical Implementation

### 3.1 Frontend (`index.html`, `styles.css`, `script.js`)
-   **HTML**:
    -   Add a tab navigation bar.
    -   Wrap competition sections in tab content containers.
    -   Add `data-sort` attributes to table headers.
    -   Add search input fields.
-   **CSS**:
    -   Style the tabs (active/inactive states).
    -   Hide inactive tab content.
    -   Style sort indicators (arrows).
-   **JS**:
    -   Implement tab switching logic.
    -   Initialize `List.js` for each competition's tables.

### 3.2 Backend (`app.py`, `config.py`)
-   **Config**: Add `ENABLE_AI_SUMMARY` to `Config` class.
-   **Route**: Pass this config value to the template.
-   **Template**: Use Jinja `{% if enable_ai %}` block to conditionally render the summary section.

## 4. Acceptance Criteria
-   [ ] UI is organized into tabs (one per league).
-   [ ] Clicking tabs switches content instantly.
-   [ ] Standings table can be sorted by clicking headers.
-   [ ] Standings and Matches can be filtered by team name.
-   [ ] AI Summary UI is hidden if `ENABLE_AI_SUMMARY=false`.

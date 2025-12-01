# Phase 7 Prompt Plan: UI Overhaul & Configurable AI

## 1. Goal
Implement a tabbed interface, add table sorting/filtering, and make AI summary configurable.

## 2. Configurable AI
-   **`config.py`**: Add `ENABLE_AI_SUMMARY` (default: True).
-   **`app.py`**: Pass `enable_ai_summary` to template.
-   **`templates/index.html`**: Wrap summary section in `{% if enable_ai_summary %}`.

## 3. UI Overhaul (Tabs)
-   **`templates/index.html`**:
    -   Add `<div class="tabs">` container.
    -   Add buttons for each competition.
    -   Wrap each competition's content in `<div class="tab-content" id="tab-{code}">`.
-   **`static/styles.css`**:
    -   Style tabs (flexbox, active state).
    -   Hide `.tab-content` by default, show `.tab-content.active`.
-   **`static/script.js`**:
    -   Add event listeners to tab buttons to toggle active class on buttons and content.

## 4. Table Features (List.js)
-   **`templates/index.html`**:
    -   Add `list.min.js` CDN.
    -   Add classes `list`, `sort`, `search` to tables/inputs as required by List.js.
    -   Add `data-sort="pts"` etc. to headers.
-   **`static/script.js`**:
    -   Initialize `new List(...)` for each competition's standings and match list.

## 5. Verification Steps
1.  **AI Config**:
    -   Set `ENABLE_AI_SUMMARY=false` in `.env`.
    -   Restart app.
    -   Verify summary section is gone.
2.  **Tabs**:
    -   Verify tabs appear.
    -   Click tabs -> content switches correctly.
3.  **Tables**:
    -   Click "Pts" header -> table sorts.
    -   Type in search bar -> table filters.

# Phase 11: Automated AI Summary

## Goal
Automate the AI summary generation so it runs during the background data refresh. The summary should be concise (10 lines max) and displayed automatically in the UI, removing the need for a manual "Generate" button.

## Changes

### 1. Database (`db_manager.py`)
-   Add a new table `summary` (or `metadata`) to store the latest AI generated summary.
-   Schema: `key TEXT PRIMARY KEY, value TEXT, updated_at TIMESTAMP`.
-   Methods: `save_summary(text)`, `get_summary()`.

### 2. AI Generator (`ai_summary.py`)
-   Update the prompt to strictly request **10 lines** of text.
-   Focus on "Important Match News".

### 3. Backend Logic (`app.py`)
-   In `scheduled_refresh()`:
    -   After fetching matches/scorers/standings, call `ai_generator.generate_summary(data)`.
    -   Save the result to the DB using `db_manager.save_summary()`.
-   In `index()` route:
    -   Fetch the summary using `db_manager.get_summary()`.
    -   Pass it to the template.

### 4. Frontend (`templates/partials/header.html` & `ai_summary.html`)
-   **Header**: Remove the "AI Summary" button.
-   **AI Summary Partial**: Display the summary text directly if available.

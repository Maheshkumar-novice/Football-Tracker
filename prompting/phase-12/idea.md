# Phase 12: Remove AI & Enhance Scorers

## Goals
1.  **Remove AI Summary**: Completely remove the AI summary feature, including backend logic, database storage, and frontend UI.
2.  **Enhance Scorers Table**: Split the "Goals (Assists)" column into two separate columns: "Goals" and "Assists".

## Changes

### 1. Remove AI Features
-   **Delete**: `ai_summary.py`.
-   **Delete**: `templates/partials/ai_summary.html`.
-   **Modify**: `app.py` (remove `AISummaryGenerator`, `scheduled_refresh` AI logic, and `index` route variables).
-   **Modify**: `config.py` (remove Anthropic keys and `ENABLE_AI_SUMMARY`).
-   **Modify**: `templates/index.html` (remove include).
-   **Modify**: `templates/partials/header.html` (clean up).

### 2. Enhance Scorers Table
-   **Modify**: `templates/partials/scorers.html`.
-   **Structure**:
    -   Add `<th>Assists</th>`.
    -   Add `<td>{{ player.assists }}</td>`.
    -   Ensure `Goals` column only shows goals.

# Phase 11 Specification

## 1. Database (`db_manager.py`)
-   **Table**: `app_metadata`
    ```sql
    CREATE TABLE IF NOT EXISTS app_metadata (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TIMESTAMP
    )
    ```
-   **Methods**:
    -   `save_metadata(key, value)`
    -   `get_metadata(key)`
    -   Wrappers: `save_summary(summary_text)`, `get_summary()` (using key='ai_summary').

## 2. AI Generator (`ai_summary.py`)
-   **Prompt Update**:
    -   "Provide a concise summary of the most important match news."
    -   "Strictly limit the output to exactly 10 lines."
    -   "Focus on key results, upsets, or major changes in standings."

## 3. App Logic (`app.py`)
-   **Scheduled Job**:
    ```python
    def scheduled_refresh():
        # ... existing refresh logic ...
        matches = db_manager.get_all_matches()
        scorers = db_manager.get_all_scorers()
        standings = db_manager.get_all_standings()
        
        # Prepare data for AI
        context = { ... } 
        
        if config.ENABLE_AI_SUMMARY:
            summary = ai_generator.generate_summary(context)
            db_manager.save_summary(summary)
    ```
-   **Route**:
    ```python
    @app.route('/')
    def index():
        # ... fetch data ...
        summary = db_manager.get_summary()
        return render_template(..., summary=summary)
    ```

## 4. UI
-   **Header**: Remove button.
-   **AI Summary Partial**:
    ```html
    {% if summary %}
    <div class="summary-section">
        <h3>⚡ Match Highlights</h3>
        <div class="summary-text">
            {{ summary | safe }} <!-- Render Markdown -->
        </div>
    </div>
    {% endif %}
    ```

# Phase 12 Specification

## 1. Top Scorers Table (`templates/partials/scorers.html`)
```html
<table class="scorers-table">
    <thead>
        <tr>
            <th>#</th>
            <th>Player</th>
            <th class="text-center">Goals</th>
            <th class="text-center">Assists</th>
        </tr>
    </thead>
    <tbody>
        {% for player in scorers[code] %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>
                <div class="player-info">
                    <span class="player-name">{{ player.player.name }}</span>
                    <span class="team-name-small">{{ player.team.name }}</span>
                </div>
            </td>
            <td class="text-center"><strong>{{ player.goals }}</strong></td>
            <td class="text-center">{{ player.assists or 0 }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

## 2. Remove AI Features
-   **`app.py`**:
    -   Remove `from ai_summary import AISummaryGenerator`.
    -   Remove `summary_generator` initialization.
    -   Remove AI logic inside `scheduled_refresh`.
    -   Remove `ai_summary` fetch in `index` route.
    -   Remove `enable_ai_summary` and `summary` from `render_template`.
-   **`config.py`**:
    -   Remove `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, `ANTHROPIC_TIMEOUT_SECONDS`, `ENABLE_AI_SUMMARY`.
-   **`templates/index.html`**:
    -   Remove `{% include 'partials/ai_summary.html' %}`.
-   **`templates/partials/header.html`**:
    -   Remove any AI-related comments or logic.
-   **Files to Delete**:
    -   `ai_summary.py`
    -   `templates/partials/ai_summary.html`

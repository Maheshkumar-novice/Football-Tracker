# Phase 13 Specification

## 1. Scorers Table (`templates/partials/scorers.html`)
Match the structure of `standings.html`:
```html
<div class="table-container">
    <table>
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
                <td class="rank">{{ loop.index }}</td>
                <td class="team">
                    <div class="team-cell">
                        <!-- Player Name & Team -->
                        <div class="player-info">
                            <span class="team-name-text">{{ player.player.name }}</span>
                            <span class="team-name-small" style="font-size: 0.8em; color: #666;">{{ player.team.name }}</span>
                        </div>
                    </div>
                </td>
                <td class="text-center"><strong>{{ player.goals }}</strong></td>
                <td class="text-center">{{ player.assists or 0 }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

## 2. Remove `marked.js`
-   Check `templates/index.html` and `templates/base.html`.
-   Remove `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>`.

## 3. Sort Matches (`data_processor.py`)
Update `group_by_competition`:
```python
    # Sort matches within each competition
    for comp_code in grouped:
        grouped[comp_code].sort(
            key=lambda m: (
                m.get('status') in ['FINISHED', 'IN_PLAY', 'PAUSED'], # Prioritize active/finished
                m.get('utc_kickoff', '') # Then by date
            ),
            reverse=True # True > False, Newest > Oldest
        )
```

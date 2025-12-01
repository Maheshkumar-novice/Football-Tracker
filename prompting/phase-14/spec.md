# Phase 14 Specification

## Matches Table (`templates/partials/matches.html`)

Replace the existing `.matches-list` with:

```html
<div class="section matches-section">
    <h3>Recent Matches</h3>
    {% if matches %}
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Home Team</th>
                    <th>Away Team</th>
                    <th class="text-center">Result</th>
                    <th class="text-center">Status</th>
                    <th class="text-center">Link</th>
                </tr>
            </thead>
            <tbody>
                {% for match in matches %}
                <tr>
                    <td class="match-date">{{ match.date }}</td>
                    <td class="team-cell">
                        <div class="team-info">
                            <img src="{{ match.home_team.crest }}" alt="" class="team-crest-small" onerror="this.style.display='none'">
                            <span>{{ match.home_team.name }}</span>
                        </div>
                    </td>
                    <td class="team-cell">
                        <div class="team-info">
                            <img src="{{ match.away_team.crest }}" alt="" class="team-crest-small" onerror="this.style.display='none'">
                            <span>{{ match.away_team.name }}</span>
                        </div>
                    </td>
                    <td class="text-center font-bold">{{ match.score_text }}</td>
                    <td class="text-center status-{{ match.status|lower }}">{{ match.status }}</td>
                    <td class="text-center">
                        <a href="https://www.google.com/search?q={{ match.home_team.name }} vs {{ match.away_team.name }}" 
                           target="_blank" 
                           class="btn-link">
                            Search
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% else %}
    <p class="no-data">No recent matches found.</p>
    {% endif %}
</div>
```

## CSS Updates (`static/styles.css`)
-   Ensure `.team-info` aligns crest and text nicely.
-   Add `.btn-link` style if needed (or just use standard link styling).
-   Add status colors if desired (e.g., `.status-finished`, `.status-live`).

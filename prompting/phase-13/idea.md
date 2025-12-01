# Phase 13: UI Refinement & Cleanup

## Goals
1.  **Refine Scorers Table**: Update the top scorers table to match the visual style of the standings table (using `<table>` with consistent classes and headers).
2.  **Remove `marked.js`**: Remove the unused Markdown library since the AI summary feature is gone.
3.  **Sort Matches**: Sort recent matches to show the "latest completed" matches first.

## Changes

### 1. Refine Scorers Table
-   **Modify**: `templates/partials/scorers.html`.
-   **Style**: Use the same `<table>`, `<thead>`, `<th>`, `<tbody>`, `<tr>`, `<td>` structure and classes as `templates/partials/standings.html`.
-   **Columns**: #, Player (with team), Goals, Assists.

### 2. Remove `marked.js`
-   **Modify**: `templates/index.html` (or `base.html` if it's there).
-   **Action**: Delete the `<script>` tag loading `marked.min.js`.

### 3. Sort Matches
-   **Modify**: `data_processor.py`.
-   **Logic**: Update `group_by_competition` to sort matches:
    1.  Primary Sort: `status == 'FINISHED'` (First).
    2.  Secondary Sort: `utc_kickoff` (Descending / Most Recent).
    -   *Note*: Actually, if we want "latest completed", we want FINISHED matches first, sorted by date desc. Then scheduled matches? Or just all matches sorted by date desc?
    -   *User Request*: "sort recent matches by latest completed".
    -   *Interpretation*: Finished matches should be at the top, sorted by most recent. Then scheduled/live matches? Or maybe just strictly by date, but since we fetch "recent" matches (past 7 days), they are mostly finished.
    -   *Refinement*: Let's stick to: Sort by `utc_kickoff` descending (newest first). This naturally puts the latest games at the top.
    -   *Wait*, the user specifically said "latest completed". If there are scheduled matches in the future (unlikely for "recent matches" endpoint which usually looks back, but `fetch_recent_matches` looks back 7 days), they might be mixed in?
    -   Actually, `fetch_recent_matches` fetches `dateFrom` = 7 days ago, `dateTo` = today. So it shouldn't have future matches unless they are today.
    -   If there are matches *today* that haven't started, they would be at the top if sorted by date desc.
    -   User wants "latest completed". So:
        -   Priority 1: Status = FINISHED (or IN_PLAY).
        -   Priority 2: Date Descending.
        -   Scheduled matches (if any) should be at the bottom? Or maybe just strictly Date Descending is what they mean, but they want to see the *results*.
        -   Let's implement a sort key: `(is_finished, date_desc)`.

## Implementation Details
-   **Scorers UI**: Copy classes from `standings.html`.
-   **Sorting**:
    ```python
    def sort_key(match):
        is_finished = match.get('status') in ['FINISHED', 'IN_PLAY', 'PAUSED']
        date = match.get('utc_kickoff', '')
        return (is_finished, date)
    ```
    -   Sort `reverse=True` so `True` (Finished) comes before `False`, and later dates come before earlier dates.

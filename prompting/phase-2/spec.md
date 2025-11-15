# Football Matches Tracker — Phase 2 Specification

## 1. Phase 2 Scope
Phase 2 adds two major capabilities to the existing Football Matches Tracker system:
1. **Anthropic AI summary generation for currently displayed results**
2. **Champions League (UCL) competition integration**

All Phase-1 functionality remains unchanged except where explicitly extended here.

---

## 2. Anthropic AI Summary Feature

### 2.1 Overview
Users can manually trigger an **AI-generated sports-journalist style summary** based on the match results currently shown in the UI (last 7 days, across all tracked competitions including UCL).

The feature is **on-demand only** — summaries are not automatically generated.

### 2.2 Trigger Behavior
- A button **in the header** labeled `Generate Summary`.
- When clicked:
  - Button label changes to **"Generating…"**
  - Button becomes disabled
  - A loading placeholder appears **below the timestamp** and **above the button**:
    ```
    Generating summary…
    ```
- After summary generation completes:
  - Button returns to **`Generate Summary`**
  - Button becomes **disabled until the next match-data refresh**

### 2.3 Summary Visibility Rules
- Summary block appears **below the timestamp and above the button**.
- Appears only when the user generates it.
- Disappears automatically on **page reload or auto-refresh**.
- Uses **moderate vertical spacing** before the match list.

### 2.4 Summary Styling
- Highlight block (attention-grabbing accent background).
- **Each headline on its own line** (no bullets, no numbering).
- Include small internal timestamp:
````

(Summary generated X minutes ago)

````

### 2.5 Output Format Requirements
- Role-based prompt: persona = **sports journalist**
- Expected tone: dramatic and headline-like
- Output count: **3–7 headlines (dynamic range)**
- **Lenient acceptance**: any number of lines returned are displayed as-is.
- **No sanitization or post-processing** — UI renders the Anthropic text exactly.

### 2.6 Data Sent to Anthropic
Anthropic receives a JSON list of matches, with each object containing:

| Field |
|--------|
| `competition_code` |
| `competition_name` |
| `utc_kickoff` |
| `display_date` |
| `home_team` |
| `away_team` |
| `status` |
| `score_text` |
| `google_query` |

The summary must cover **all 6 competitions**, including UCL.

### 2.7 Anthropic API Configuration
All configuration via environment variables:

| Env Variable |
|--------------|
| `ANTHROPIC_API_KEY` |
| `ANTHROPIC_MODEL` |
| `ANTHROPIC_TIMEOUT_SECONDS` (optional) |

- Temperature: **medium**
- If the request fails:
- Loading placeholder is replaced with an inline error:
  ```
  Failed to generate summary. Please try again.
  ```

### 2.8 Logging for AI Summary
- **Full prompt + full response** are logged directly into `app.log`.
- No separate log file.

### 2.9 Cost Control Logic
- Summary button **can only be used once per data refresh**.
- After summary is generated:
````

Summary available after next update

````
(disabled state)
- Button re-enabled only when new match data is downloaded (initial load or 30-min refresh).

### 2.10 Auto-Refresh Interaction
- If auto-refresh triggers while summary is visible:
- **Do not reload automatically**
- Display informational banner **below header and above summary**:
  ```
  New data available — reload now?
  [Reload button]
  ```
- User must click reload to refresh.

---

## 3. UCL (Champions League) Integration

### 3.1 Data Retrieval
- Add UCL (`competition_code = "CL"`) as the **6th tracked competition**.
- Use the same API patterns as the other leagues:
- Match window: **last 7 days**
- Same fields extracted
- Included in the same cached structure

### 3.2 UI Behavior
- UCL is displayed as **its own competition section** with header:
````

▌ Champions League

```
- Order in UI: **standard alphabetical/API ordering** alongside other leagues (no prioritization).
- If no UCL matches in the last 7 days:
```

No recent matches

````

### 3.3 Error Behavior
- If UCL API call fails:
- Other competitions unaffected
- UCL section still appears
- If cached UCL data exists → show cached data
- Else → show error placeholder:
  ```
  Error fetching data. Showing cached results.
  ```

### 3.4 AI Integration
- UCL results are **always included** in the JSON sent to Anthropic and therefore in the summary.

---

## 4. Backend Architecture Impact

### 4.1 New Module
A new file is added:
````

ai_summary.py

```

Responsibilities:
- Construct JSON payload from cached match data
- Build Anthropic prompt
- Call Anthropic
- Return raw string output

### 4.2 Existing Modules Unchanged
- `app.py` remains the route + rendering entry point
- `football_api.py` still handles Football-Data.org calls
- `cache.py` continues Phase-1 caching model
- `app.log` continues as the single log target

### 4.3 No Caching of Summaries
- Every summary request calls Anthropic fresh.
- No storage of summary history.

---

## 5. Acceptance Criteria for Phase 2 Completion
Phase 2 is considered **complete** when:

| Feature | Requirement |
|---------|-------------|
| UCL integration | UCL appears as 6th competition with full fallback logic |
| AI summary | Manual trigger via header button |
| Output | Highlight block with headlines + timestamp |
| Placement | Below timestamp, above button |
| Logging | Full prompt + response in `app.log` |
| Button state | Disabled until next match data refresh |
| Refresh UX | Banner prompt rather than auto-refresh while summary visible |
| Local run | All features function correctly in local development environment |

No deployment, staging, automated tests, or production hardening is required for Phase 2.

---

# End of Document

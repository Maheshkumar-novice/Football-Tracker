# Football Matches Tracker - Phase 2 Implementation Blueprint

## Analysis of Phase 2 Requirements

Phase 2 adds two main features:
1. **AI Summary Generation** - On-demand Anthropic API integration for match summaries
2. **Champions League (UCL)** - Add 6th competition to tracking

Key considerations:
- Must preserve all Phase 1 functionality
- AI summaries are ephemeral (no caching)
- Button state management prevents excessive API calls
- Auto-refresh behavior changes when summary is visible
- UCL integration follows existing patterns

---

## High-Level Phase 2 Architecture

```
Phase 2A: UCL Integration (extends existing patterns)
Phase 2B: AI Summary Infrastructure
Phase 2C: Frontend Integration
Phase 2D: State Management & Polish
```

---

## Detailed Step Breakdown

### Round 1: Initial Assessment

The work naturally splits into:
1. Extend competitions to include UCL
2. Create AI summary module
3. Add frontend button and summary display
4. Implement button state logic
5. Handle auto-refresh with summary visible

### Round 2: Granular Steps

Breaking down further for safety:

1. Add UCL to competition codes
2. Update data processor for 6 competitions
3. Create AI summary module
4. Add Anthropic API configuration
5. Build prompt construction logic
6. Add summary route to Flask
7. Add Generate Summary button to template
8. Add summary display area
9. Style summary highlight block
10. Add JavaScript for button interaction
11. Implement button state management
12. Add auto-refresh override logic
13. Add reload banner
14. Full integration testing

### Round 3: Final Sizing

Steps look well-sized. Each is small enough to implement safely but substantial enough to show progress.

---

## Implementation Prompts for Phase 2

---

### Prompt 1: Add UCL Competition Code

```
Extend the existing Football Matches Tracker to support Champions League (UCL).

Requirements:
- Update `football_api.py`:
  - Add "CL" (Champions League) to the COMPETITION_CODES constant
  - This should now be a list/tuple of 6 codes: PL, PD, BL1, SA, FL1, CL
- Update any hardcoded references to "5 competitions" in comments or docstrings to "6 competitions"
- No other logic changes needed

The competition codes should now be:
```python
COMPETITION_CODES = ["PL", "PD", "BL1", "SA", "FL1", "CL"]
```

Test:
- Verify the constant is updated
- Run the app and check that UCL matches appear if any exist in last 72 hours
- Verify other 5 competitions still work correctly
```

---

### Prompt 2: Update Config for Anthropic API

```
Extend `config.py` to support Anthropic API configuration.

Requirements:
- Add three new environment variables:
  - `ANTHROPIC_API_KEY` (required - raise error if missing)
  - `ANTHROPIC_MODEL` (optional, default to "claude-sonnet-4-20250514")
  - `ANTHROPIC_TIMEOUT_SECONDS` (optional, default to 30)
- Update the Config class/dict to expose these values
- Keep all existing Football-Data.org config unchanged

Example usage:
```python
from config import Config
print(Config.ANTHROPIC_API_KEY)
print(Config.ANTHROPIC_MODEL)
print(Config.ANTHROPIC_TIMEOUT_SECONDS)
```

Update `.env` template/comments to document these new variables.

Test:
- Import Config and verify all 3 new values are accessible
- Verify error is raised if ANTHROPIC_API_KEY is missing
- Verify defaults work when optional vars not set
```

---

### Prompt 3: Create AI Summary Module - Basic Structure

```
Create a new module `ai_summary.py` that handles Anthropic API integration.

Requirements:
- Install anthropic SDK: `pip install anthropic`
- Create class `AISummaryGenerator` with:
  - Constructor accepting: api_key, model, timeout
  - Store these as instance variables
  - Initialize Anthropic client
- Add method stub `generate_summary(matches_data)`:
  - Accept matches_data as a list of match dicts
  - For now, just return a placeholder string: "Summary generation coming soon"
  - Add logging for when method is called

Example usage:
```python
from ai_summary import AISummaryGenerator

generator = AISummaryGenerator(
    api_key=Config.ANTHROPIC_API_KEY,
    model=Config.ANTHROPIC_MODEL,
    timeout=Config.ANTHROPIC_TIMEOUT_SECONDS
)
summary = generator.generate_summary(matches)
```

Do NOT implement actual API calling yet - just the structure.

Test:
- Import the module
- Create generator instance
- Call generate_summary with empty list
- Verify placeholder string returned
```

---

### Prompt 4: Implement Prompt Construction

```
Extend `ai_summary.py` to build the prompt for Anthropic.

Requirements:
- Add helper method `_build_prompt(matches_data)` that:
  - Accepts list of match dicts (each with all 9 fields from spec)
  - Constructs a JSON representation of the matches
  - Builds a system prompt with role: "You are a sports journalist"
  - Builds a user prompt that:
    - Includes the JSON match data
    - Requests 3-7 dramatic, headline-style summaries
    - Specifies the output should be plain text, one headline per line
    - Emphasizes covering all competitions (including UCL)
  - Returns both system and user prompts as strings

Prompt structure example:
```
System: You are a sports journalist creating dramatic headlines about recent football matches.

User: Based on these recent matches from the last 72 hours across the Premier League, La Liga, Bundesliga, Serie A, Ligue 1, and Champions League:

[JSON data here]

Generate 3-7 dramatic, headline-style summaries that capture the most interesting storylines. Output only the headlines, one per line, with no numbering or bullets.
```

- Add logging to show the full prompt being constructed
- Do NOT call the API yet

Test:
- Call _build_prompt with sample match data
- Verify system and user prompts are formatted correctly
- Check logs show the full prompt
```

---

### Prompt 5: Implement Anthropic API Call

```
Complete the `generate_summary()` method in `ai_summary.py`.

Requirements:
- Update `generate_summary(matches_data)` to:
  - Call `_build_prompt()` to get system and user prompts
  - Make API call to Anthropic using the SDK:
    - Use messages API
    - Pass system prompt
    - Pass user prompt
    - Set temperature to 0.7 (medium)
    - Use max_tokens of 1000
    - Include timeout from config
  - Extract text response from API
  - Log the full request and full response to logger
  - Return the raw text (no post-processing)
- Add error handling:
  - Catch API errors (timeout, authentication, rate limit)
  - Log the error
  - Return None on failure

Example API call structure:
```python
response = self.client.messages.create(
    model=self.model,
    max_tokens=1000,
    temperature=0.7,
    system=system_prompt,
    messages=[{"role": "user", "content": user_prompt}]
)
```

Test:
- Call with real match data
- Verify API call succeeds and returns text
- Check that full prompt and response are in app.log
- Test error handling by using invalid API key
```

---

### Prompt 6: Add Summary Route to Flask

```
Add a new API endpoint to `app.py` for generating summaries.

Requirements:
- Import `AISummaryGenerator` and `Config`
- Create global instance:
  ```python
  summary_generator = AISummaryGenerator(
      Config.ANTHROPIC_API_KEY,
      Config.ANTHROPIC_MODEL,
      Config.ANTHROPIC_TIMEOUT_SECONDS
  )
  ```
- Add new route `POST /generate-summary`:
  - Get current matches from `data_service.get_matches()`
  - Flatten the competitions dict into a single list of all matches
  - Call `summary_generator.generate_summary(matches_list)`
  - If summary generation succeeds:
    - Return JSON: `{"success": true, "summary": "text here", "generated_at": timestamp}`
  - If it fails:
    - Return JSON: `{"success": false, "error": "Failed to generate summary"}`
  - Log the request and outcome
- Add CORS handling if needed (for AJAX call)

Response format:
```json
{
  "success": true,
  "summary": "Headline 1\nHeadline 2\nHeadline 3",
  "generated_at": "2025-11-15T18:30:00Z"
}
```

Test:
- Make POST request to /generate-summary
- Verify JSON response with summary text
- Check logs show the generation process
```

---

### Prompt 7: Add Summary Button to Template

```
Update `templates/index.html` to add the Generate Summary button.

Requirements:
- In the header section, after the "Last updated" line, add:
  - A "Generate Summary" button
  - Button should have id="generate-summary-btn"
  - Button should be styled as a primary action button
  - Initial state: enabled
- Add a div for loading placeholder:
  - id="summary-loading"
  - Initially hidden
  - Content: "Generating summary…"
- Add a div for summary display:
  - id="summary-block"
  - Initially hidden
  - Will contain the summary text and timestamp
- Add a div for error messages:
  - id="summary-error"
  - Initially hidden

HTML structure:
```html
<div class="summary-controls">
  <div id="summary-loading" style="display: none;">Generating summary…</div>
  <div id="summary-error" style="display: none;"></div>
  <div id="summary-block" style="display: none;">
    <div id="summary-text"></div>
    <div id="summary-timestamp"></div>
  </div>
  <button id="generate-summary-btn">Generate Summary</button>
</div>
```

Position this section between the "Last updated" text and the matches list.

Do NOT add JavaScript yet - just the HTML structure.

Test:
- Verify button appears in UI
- Verify all containers are initially hidden
- Verify button is clickable (even if nothing happens yet)
```

---

### Prompt 8: Style Summary Display Block

```
Update `static/styles.css` to style the summary feature.

Requirements:
- **Summary controls section:**
  - Margin above and below to separate from header/matches
  - Center-aligned content
- **Generate Summary button:**
  - Primary button styling (colored background, white text)
  - Padding for comfortable click target
  - Hover effect
  - Disabled state styling (grayed out, no pointer)
- **Loading placeholder:**
  - Subtle color, centered text
  - Small spinner or pulsing animation (optional)
- **Summary block:**
  - Highlight background (accent color, e.g., light yellow or light blue)
  - Padding for readability
  - Border or subtle shadow
  - Rounded corners
- **Summary text:**
  - Each headline on its own line
  - Readable font size
  - Line height for breathing room
- **Summary timestamp:**
  - Small, muted text
  - Margin above to separate from headlines
- **Error message:**
  - Red text
  - Centered
  - Padding

Focus on making the summary block visually distinct and attention-grabbing.

Test:
- Manually toggle visibility of elements in browser dev tools
- Verify summary block stands out from match list
- Verify button states are clear
```

---

### Prompt 9: Add JavaScript for Button Interaction

```
Update `static/script.js` to handle summary generation.

Requirements:
- Add event listener for "Generate Summary" button click
- When clicked:
  - Change button text to "Generating…"
  - Disable button
  - Show loading placeholder
  - Hide summary block and error message
  - Make POST request to `/generate-summary`
  - Handle response:
    - On success:
      - Hide loading placeholder
      - Parse summary text (split by newlines)
      - Display each line in summary-text div
      - Show timestamp: "(Summary generated X minutes ago)"
      - Show summary block
      - Keep button disabled with text "Summary available after next update"
    - On failure:
      - Hide loading placeholder
      - Show error message: "Failed to generate summary. Please try again."
      - Re-enable button with original text
  - Log the interaction for debugging

Use fetch API for the POST request:
```javascript
fetch('/generate-summary', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'}
})
.then(response => response.json())
.then(data => { /* handle response */ })
```

Test:
- Click button and verify loading state appears
- Verify summary displays on success
- Verify button stays disabled after success
- Test error handling with network disconnected
```

---

### Prompt 10: Implement Button State Management

```
Extend the JavaScript in `static/script.js` to manage button state across page lifecycle.

Requirements:
- Add a flag to track if summary has been generated: `summaryGenerated = false`
- After successful summary generation:
  - Set `summaryGenerated = true`
  - Update button text to "Summary available after next update"
  - Keep button disabled
- Store this state in sessionStorage:
  - `sessionStorage.setItem('summaryGenerated', 'true')`
- On page load, check sessionStorage:
  - If 'summaryGenerated' is 'true', disable button with message
  - Clear sessionStorage when page is reloaded (indicates new data)
- The auto-refresh logic (from Phase 1) should NOT reload when summary is visible

Add function `checkSummaryState()` that:
- Checks if summary block is visible
- If visible, prevents auto-refresh
- Returns boolean

Update the existing auto-refresh timer to call this function first.

Test:
- Generate summary
- Verify button stays disabled
- Reload page manually
- Verify button is re-enabled
- Verify summary is hidden after reload
```

---

### Prompt 11: Add Auto-Refresh Override Logic

```
Update `static/script.js` to handle auto-refresh when summary is visible.

Requirements:
- Modify the existing 30-minute auto-refresh timer:
  - Before reloading, check if summary is visible
  - If summary block is displayed:
    - Do NOT auto-reload
    - Instead, show a banner with "New data available" message
    - Provide manual reload button
  - If summary is not visible:
    - Auto-reload as normal (existing Phase 1 behavior)
- Add function `showReloadBanner()` that:
  - Creates/shows a banner div
  - Banner contains: "New data available — reload now?"
  - Banner includes a "Reload" button
  - Button onclick calls `window.location.reload()`
- Position banner in template (we'll add the HTML next)

Updated timer logic:
```javascript
setTimeout(() => {
  if (document.getElementById('summary-block').style.display !== 'none') {
    showReloadBanner();
  } else {
    window.location.reload();
  }
}, REFRESH_INTERVAL);
```

Test:
- Generate summary
- Wait for 30-minute timer (or set to 10 seconds for testing)
- Verify banner appears instead of auto-reload
- Click reload button and verify page reloads
- Test without summary - verify auto-reload still works
```

---

### Prompt 12: Add Reload Banner to Template

```
Update `templates/index.html` to include the reload notification banner.

Requirements:
- Add a new div for reload banner:
  - id="reload-banner"
  - Initially hidden (style="display: none;")
  - Position: between header and summary section
  - Content:
    - Message: "New data available — reload now?"
    - Button: "Reload" with onclick handler
- Style the banner to be visually distinct:
  - Info color (blue background)
  - White text
  - Centered content
  - Padding
  - Full width across page

HTML structure:
```html
<div id="reload-banner" style="display: none;">
  <span>New data available — reload now?</span>
  <button onclick="window.location.reload()">Reload</button>
</div>
```

Update CSS:
- Style reload-banner with info coloring
- Style inline reload button to match theme
- Ensure banner is prominent but not overwhelming

Test:
- Manually show banner in browser dev tools
- Verify message and button are readable
- Verify button triggers reload
- Verify banner positioned correctly
```

---

### Prompt 13: Add Summary Logging

```
Enhance logging across the summary feature.

Requirements:
- In `ai_summary.py`:
  - Log full prompt before API call (already done in Prompt 5, verify it's complete)
  - Log full API response
  - Log token usage if available from API response
  - Log any errors with full stack trace
- In `app.py` `/generate-summary` route:
  - Log when summary generation is requested
  - Log number of matches being summarized
  - Log success/failure outcome
  - Log timestamp when summary is returned to client
- Use appropriate log levels:
  - INFO for normal operations
  - ERROR for failures
  - DEBUG for detailed match data (optional)

All logs should go to the existing `app.log` file.

Test:
- Generate a summary
- Open `app.log`
- Verify you see:
  - Request logged
  - Full prompt
  - Full response
  - Outcome message
- Trigger an error (invalid API key) and verify error is logged
```

---

### Prompt 14: Integration Testing and Edge Cases

```
Perform comprehensive testing and handle edge cases.

Requirements:
**Test scenarios to implement fixes for:**
1. **No matches scenario:**
   - If no matches in last 72 hours for all 6 competitions
   - Summary button should show: "No matches to summarize"
   - Button should be disabled
   
2. **UCL-specific errors:**
   - If UCL API fails but others succeed
   - UCL section shows cached data or error message
   - Other competitions unaffected
   - Summary still works with available data

3. **Anthropic API errors:**
   - Timeout: show user-friendly error
   - Rate limit: show specific message
   - Invalid key: log error, show generic message to user
   
4. **Multiple clicks:**
   - Prevent multiple simultaneous requests
   - Disable button immediately on click
   
5. **Browser refresh during generation:**
   - Handle incomplete state gracefully
   - Clear any stale sessionStorage
   
**Add defensive checks:**
- In `/generate-summary` route: check matches list is not empty
- In JavaScript: validate response has expected structure
- In template: handle missing data gracefully

**Update error messages to be user-friendly:**
- Instead of technical errors, show actionable messages
- Examples:
  - "Unable to connect to AI service. Please try again."
  - "Request timed out. Please try again in a moment."

Test each scenario and verify appropriate behavior.
```

---

### Prompt 15: Final Polish and Documentation

```
Add final touches and update documentation for Phase 2.

Requirements:

**Update README.md:**
- Add Phase 2 features section:
  - Champions League integration
  - AI-powered summary generation
- Update environment variables section:
  - Document ANTHROPIC_API_KEY (required)
  - Document ANTHROPIC_MODEL (optional)
  - Document ANTHROPIC_TIMEOUT_SECONDS (optional)
- Add usage instructions for summary feature
- Add note about cost control (one summary per refresh)

**Update dependencies:**
- Add `anthropic` to requirements list
- Update pip install command

**Code cleanup:**
- Add docstrings to all new functions
- Ensure consistent error handling patterns
- Remove any debug console.logs
- Verify all comments are accurate

**Final testing checklist:**
- [ ] UCL appears as 6th competition
- [ ] Generate Summary button works
- [ ] Summary displays in highlight block
- [ ] Button disables after use
- [ ] Button re-enables after data refresh
- [ ] Auto-refresh shows banner when summary visible
- [ ] Manual reload works from banner
- [ ] All errors handled gracefully
- [ ] Full logging in app.log
- [ ] No console errors in browser

**Create a Phase 2 testing guide:**
- Document how to test each feature
- Include example match data scenarios
- Include error scenarios to test

This completes Phase 2 implementation!
```

---

## Summary

This blueprint provides **15 iterative prompts** for Phase 2 that:

✅ Preserve all Phase 1 functionality  
✅ Add UCL integration safely  
✅ Implement AI summary feature incrementally  
✅ Handle button state management  
✅ Implement auto-refresh override  
✅ Include comprehensive error handling  
✅ Maintain logging standards  

Each prompt builds on Phase 1 and previous Phase 2 steps, ensuring no breaking changes and a working application at each stage.
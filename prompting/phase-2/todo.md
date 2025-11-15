# Football Matches Tracker - Phase 2 TODO Checklist

## Pre-Phase 2 Setup
- [ ] Verify Phase 1 is fully working
- [ ] Get Anthropic API key from console.anthropic.com
- [ ] Add `ANTHROPIC_API_KEY` to `.env` file
- [ ] Add `ANTHROPIC_MODEL=claude-sonnet-4-20250514` to `.env` (optional)
- [ ] Add `ANTHROPIC_TIMEOUT_SECONDS=30` to `.env` (optional)

---

## Step 1: Add UCL Competition Code
- [ ] Update `football_api.py` to add "CL" to COMPETITION_CODES
- [ ] Update comments referencing "5 competitions" to "6 competitions"
- [ ] Test: Run app and verify UCL section appears (if matches available)

## Step 2: Update Config for Anthropic API
- [ ] Update `config.py` to load ANTHROPIC_API_KEY (required)
- [ ] Add ANTHROPIC_MODEL (default: "claude-sonnet-4-20250514")
- [ ] Add ANTHROPIC_TIMEOUT_SECONDS (default: 30)
- [ ] Test: Import Config and verify new values accessible

## Step 3: Create AI Summary Module - Basic Structure
- [ ] Install anthropic SDK: `pip install anthropic`
- [ ] Create `ai_summary.py` with `AISummaryGenerator` class
- [ ] Add constructor with api_key, model, timeout parameters
- [ ] Add `generate_summary()` method stub (placeholder return)
- [ ] Test: Import module and call method with empty list

## Step 4: Implement Prompt Construction
- [ ] Add `_build_prompt(matches_data)` helper method
- [ ] Build system prompt with sports journalist role
- [ ] Build user prompt with JSON match data
- [ ] Request 3-7 headline-style summaries
- [ ] Log full prompt being constructed
- [ ] Test: Call method and verify prompt format

## Step 5: Implement Anthropic API Call
- [ ] Complete `generate_summary()` method
- [ ] Call Anthropic messages API with prompts
- [ ] Set temperature to 0.7, max_tokens to 1000
- [ ] Extract and return raw text response
- [ ] Add error handling (timeout, auth, rate limit)
- [ ] Log full request and response to app.log
- [ ] Test: Generate actual summary with real API key

## Step 6: Add Summary Route to Flask
- [ ] Create global `summary_generator` instance in `app.py`
- [ ] Add `POST /generate-summary` route
- [ ] Flatten matches dict into single list
- [ ] Call summary_generator and return JSON response
- [ ] Handle success/failure cases
- [ ] Test: POST to endpoint and verify JSON response

## Step 7: Add Summary Button to Template
- [ ] Add "Generate Summary" button to `index.html` header
- [ ] Add `summary-loading` div (initially hidden)
- [ ] Add `summary-block` div (initially hidden)
- [ ] Add `summary-error` div (initially hidden)
- [ ] Position between "Last updated" and matches list
- [ ] Test: Verify button appears and all divs are hidden

## Step 8: Style Summary Display Block
- [ ] Style summary controls section in `styles.css`
- [ ] Style Generate Summary button (primary action)
- [ ] Style loading placeholder
- [ ] Style summary block (highlight background, accent color)
- [ ] Style summary text (one headline per line)
- [ ] Style summary timestamp (small, muted)
- [ ] Style error message (red, centered)
- [ ] Test: Toggle visibility in dev tools to check styling

## Step 9: Add JavaScript for Button Interaction
- [ ] Add click event listener for Generate Summary button
- [ ] On click: change button text to "Generating…"
- [ ] Disable button and show loading placeholder
- [ ] Make POST request to `/generate-summary`
- [ ] On success: display summary with headlines and timestamp
- [ ] Update button text to "Summary available after next update"
- [ ] On failure: show error message and re-enable button
- [ ] Test: Click button and verify full interaction flow

## Step 10: Implement Button State Management
- [ ] Add `summaryGenerated` flag in JavaScript
- [ ] Store state in sessionStorage after successful generation
- [ ] Check sessionStorage on page load
- [ ] Clear sessionStorage on manual reload
- [ ] Add `checkSummaryState()` function
- [ ] Test: Verify button stays disabled across page interactions

## Step 11: Add Auto-Refresh Override Logic
- [ ] Modify 30-minute timer to check if summary is visible
- [ ] If visible: call `showReloadBanner()` instead of auto-reload
- [ ] If not visible: auto-reload as normal
- [ ] Implement `showReloadBanner()` function
- [ ] Test: Generate summary and wait for timer (use short interval)

## Step 12: Add Reload Banner to Template
- [ ] Add `reload-banner` div to `index.html`
- [ ] Position between header and summary section
- [ ] Add "New data available — reload now?" message
- [ ] Add Reload button with onclick handler
- [ ] Style banner (blue background, white text, centered)
- [ ] Test: Manually show banner and verify reload button works

## Step 13: Add Summary Logging
- [ ] Verify `ai_summary.py` logs full prompt and response
- [ ] Add token usage logging if available
- [ ] Log errors with stack trace
- [ ] Add logging to `/generate-summary` route
- [ ] Log request, match count, outcome, timestamp
- [ ] Test: Generate summary and check app.log for complete logs

## Step 14: Integration Testing and Edge Cases
- [ ] Handle no matches scenario (disable button with message)
- [ ] Handle UCL API failure gracefully
- [ ] Handle Anthropic API errors (timeout, rate limit, auth)
- [ ] Prevent multiple simultaneous requests
- [ ] Handle browser refresh during generation
- [ ] Add defensive checks in route and JavaScript
- [ ] Update error messages to be user-friendly
- [ ] Test: Verify each edge case handled properly

## Step 15: Final Polish and Documentation
- [ ] Update README.md with Phase 2 features
- [ ] Document new environment variables
- [ ] Add usage instructions for summary feature
- [ ] Update dependencies list with `anthropic`
- [ ] Add docstrings to all new functions
- [ ] Remove debug console.logs
- [ ] Verify all comments are accurate
- [ ] Create Phase 2 testing guide
- [ ] Test: Run through final testing checklist below

---

## Final Testing Checklist
- [ ] UCL appears as 6th competition (if matches available)
- [ ] Generate Summary button appears in header
- [ ] Button click shows loading state
- [ ] Summary displays in highlight block with headlines
- [ ] Summary timestamp shows relative time
- [ ] Button disables after successful generation
- [ ] Button text changes to "Summary available after next update"
- [ ] Button re-enables after data refresh (30 min or manual reload)
- [ ] Auto-refresh shows banner when summary visible
- [ ] Manual reload from banner works
- [ ] Summary disappears after manual reload
- [ ] All API errors handled gracefully with user-friendly messages
- [ ] Full prompt and response logged to app.log
- [ ] No console errors in browser
- [ ] No crashes with missing/invalid API key
- [ ] UCL section shows "No recent matches" when empty
- [ ] Summary covers all 6 competitions including UCL

---

## Dependencies
```bash
pip install anthropic
```

## Environment Variables
Add to `.env`:
```
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-sonnet-4-20250514
ANTHROPIC_TIMEOUT_SECONDS=30
```

---

## Phase 2 Complete! 🎉
All features implemented and tested.
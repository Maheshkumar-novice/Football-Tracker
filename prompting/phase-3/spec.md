# Football Matches Tracker — Phase 3 Specification

## 1. Phase 3 Scope
Phase 3 focuses on enhancing the **AI Summary** feature introduced in Phase 2.
The goal is to transform the output from simple "headlines" into a **richer "News Feed" experience**, and improve the UI to support this via **Markdown rendering**.

## 2. Functional Requirements

### 2.1 AI Content Format ("News Style")
- **Current Behavior**: AI generates a list of 3-7 one-line headlines.
- **New Behavior**: AI generates **3-5 short news stories**.
- **Structure per Story**:
    1.  **Headline**: Catchy, dramatic, bold.
    2.  **Body**: A short paragraph (2-3 sentences) providing context, key stats, or narrative details about the match(es).
- **Tone**: Professional sports journalism (dramatic but factual).

### 2.2 UI Improvements
- **Markdown Support**: The frontend must parse and render Markdown syntax returned by the AI.
    - **Bold** (`**text**`) for headlines or key emphasis.
    - *Italics* (`*text*`) for emphasis.
    - Lists (`- item`) if applicable.
- **Visual Styling**:
    - The summary container should look more like a "News Feed" or "Daily Briefing".
    - Distinct separation between stories (e.g., spacing or dividers).

### 2.3 Data Scope
- **Input Data**: Continue using the existing match data (last 7 days, 6 competitions).
- **No New API Calls**: Do not fetch standings or top scorers yet (deferred to future phases).

## 3. Technical Implementation

### 3.1 Backend (`ai_summary.py`)
- **Prompt Update**:
    - Modify `system_prompt` to instruct the AI to act as a "Sports News Editor".
    - Modify `user_prompt` to request the specific "Headline + Body" format.
    - **Markdown Instructions**: Explicitly tell the AI to use Markdown (e.g., "Format headlines in **bold**").

### 3.2 Frontend (`index.html`, `script.js`)
- **Markdown Library**: Import a lightweight Markdown parser (e.g., `marked.js`) via CDN.
- **Rendering**: Update the JavaScript that injects the summary to parse the raw text into HTML before displaying.
    ```javascript
    summaryElement.innerHTML = marked.parse(rawSummaryText);
    ```
- **CSS**: Add styles for the rendered Markdown elements (e.g., `p` tags, `strong` tags) to ensure they match the app's theme.

## 4. Acceptance Criteria
- [ ] Clicking "Generate Summary" produces a "News Feed" with multiple stories.
- [ ] Each story has a clear **Headline** and **Body**.
- [ ] Text is rendered with **Markdown** (headlines are bold/distinct).
- [ ] No raw Markdown syntax (like `**`) is visible to the user.
- [ ] Existing cost controls (one use per refresh) remain intact.

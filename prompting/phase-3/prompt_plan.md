# Phase 3 Prompt Plan: News Feed & Markdown UI

## 1. Goal
Upgrade the AI Summary feature to generate a **"News Feed"** (Headline + Body) instead of simple headlines, and enable **Markdown rendering** in the UI for a richer presentation.

## 2. Prompt Engineering (`ai_summary.py`)

### 2.1 System Prompt
**Current**: "You are a sports journalist creating dramatic, headline-style summaries..."
**New**:
> "You are a **Sports News Editor** for a top-tier football app. Your job is to curate a 'Daily Briefing' based on recent match results. You write in a professional, engaging, and dramatic journalistic tone. You **MUST** use Markdown formatting."

### 2.2 User Prompt
**Current**: "Generate 3-7 dramatic, headline-style summaries... Output only the headlines..."
**New**:
> "Based on the provided match data, generate **3 to 5 short news stories**.
>
> **Format for each story:**
> 1.  **Headline**: A punchy, dramatic title in **Bold** (e.g., `**City Crushes United in Derby**`).
> 2.  **Body**: A concise paragraph (2-3 sentences) explaining the result, key stats, or context.
>
> **Requirements:**
> -   Use **Markdown** for formatting.
> -   Separate stories with a horizontal rule (`---`).
> -   Focus on the most significant results (big wins, upsets, derbies).
> -   Do NOT use bullet points for the main stories; use the Headline/Body format."

## 3. Code Implementation Plan

### 3.1 Backend: `ai_summary.py`
-   **Update `_build_prompt` method**:
    -   Replace the `system_prompt` string.
    -   Replace the `user_prompt` construction logic to request the new format.

### 3.2 Frontend: `templates/index.html`
-   **Add Markdown Library**:
    -   Include `marked.js` via CDN in the `<head>` or before the closing `</body>` tag.
    -   `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>`

### 3.3 Frontend: `static/script.js`
-   **Update `generateSummary` function**:
    -   Locate the line where `summaryElement.textContent` is set.
    -   Change it to `summaryElement.innerHTML = marked.parse(data.summary)`.
    -   Ensure `marked.parse` is available before calling.

### 3.4 Frontend: `static/styles.css`
-   **Style the News Feed**:
    -   Target the summary container (e.g., `#summary-content`).
    -   Add spacing between paragraphs (`p { margin-bottom: 1rem; }`).
    -   Style strong tags (`strong { color: var(--accent-color); font-size: 1.1em; }`).
    -   Style horizontal rules (`hr { border: 0; border-top: 1px solid var(--border-color); margin: 1.5rem 0; }`).

## 4. Verification Steps
1.  **Start App**: `uv run app.py`
2.  **Generate Summary**: Click the button.
3.  **Verify Output**:
    -   Check for "Headline + Body" structure.
    -   Confirm text is **bold** where expected (not `**text**`).
    -   Confirm paragraphs are properly spaced.
    -   Check logs to see the new prompt and raw response.

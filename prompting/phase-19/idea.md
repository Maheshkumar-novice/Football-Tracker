# Phase 19: Mobile Disclaimer

## Goal
Add a message in the header advising mobile users to "Use desktop site".

## Context
We reverted the responsive table changes, so the tables are wide. On mobile, they scroll horizontally, which is fine, but the user wants a hint.

## Strategy
1.  **HTML**: Add a `div` or `span` in `templates/partials/header.html` with the message.
2.  **CSS**:
    -   By default (desktop), hide this message (`display: none`).
    -   On mobile (max-width: 768px), show it (`display: block`).
    -   Style it to be noticeable but not intrusive (e.g., small text, italic, maybe a light background).

## Content
"For best experience, use Desktop Site."

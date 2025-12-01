# Phase 19 Prompt Plan

## Goal
Add "Use Desktop Site" disclaimer for mobile.

## Steps

### 1. Update Template
-   Edit `templates/partials/header.html`.
-   Add `<div class="mobile-hint">For best experience, use Desktop Site</div>` inside `.compact-header`.

### 2. Update CSS
-   Edit `static/css/layout.css` (since it contains header styles).
-   Add `.mobile-hint` styles (hidden by default).
-   Add `@media (max-width: 768px)` block to show it and adjust header layout.

### 3. Verification
-   Restart app.
-   Check desktop (hidden).
-   Check mobile (visible).

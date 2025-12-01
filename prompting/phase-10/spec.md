# Phase 10 Specification

## 1. `templates/partials/header.html`
```html
<header class="compact-header">
    <div class="header-title-group">
        <h1>Football Tracker</h1>
        <span class="last-updated">{{ last_updated }}</span>
    </div>
    
    {% if enable_ai_summary %}
    <button id="generate-summary-btn" class="btn-compact">
        <span class="btn-text">✨ AI Summary</span>
        <span class="loader"></span>
    </button>
    {% endif %}
</header>
<!-- Error banner remains below -->
```

## 2. `templates/partials/ai_summary.html`
```html
{% if enable_ai_summary %}
<div id="summary-content" class="summary-content hidden">
    <!-- Content injected here -->
</div>
{% endif %}
```

## 3. `static/styles.css`
-   `.compact-header`:
    -   `display: flex`, `justify-content: space-between`, `align-items: center`.
    -   `padding: 10px 20px`.
    -   `background: white`, `box-shadow: ...`.
-   `h1`: Font size `1.2rem` or `1.4rem`.
-   `.last-updated`: Font size `0.8rem`, `color: #666`, `margin-left: 10px`.
-   `.btn-compact`:
    -   `padding: 6px 12px`.
    -   `font-size: 0.9rem`.

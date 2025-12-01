# Phase 19 Specification

## HTML (`templates/partials/header.html`)
Add:
```html
<div class="mobile-hint">
    <small>For best experience, use Desktop Site</small>
</div>
```
Place this inside the `.compact-header` or just below it. Inside seems better for integration.

## CSS (`static/css/layout.css` or `components.css`)
```css
.mobile-hint {
    display: none; /* Hidden on desktop */
    font-size: 0.8rem;
    color: #666;
    margin-top: 5px;
    font-style: italic;
}

@media (max-width: 768px) {
    .mobile-hint {
        display: block; /* Show on mobile */
    }
    
    /* Adjust header layout if needed to accommodate the extra line */
    .compact-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
    
    .header-title-group {
        width: 100%;
        justify-content: space-between;
    }
}
```
Wait, `.compact-header` is flex row. If I add a div, it might break layout.
Better to put it *under* the title or as a separate bar?
User said "mention in the header".
Let's put it inside `.header-title-group` or just append to the header.

Refined CSS:
```css
.mobile-hint {
    display: none;
}

@media (max-width: 768px) {
    .mobile-hint {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #fff3cd;
        color: #856404;
        padding: 5px;
        border-radius: 4px;
        margin-top: 10px;
        font-size: 0.85rem;
    }
    
    .compact-header {
        flex-wrap: wrap; /* Allow wrapping */
    }
}
```

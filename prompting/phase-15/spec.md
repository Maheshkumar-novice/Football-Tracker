# Phase 15 Specification

## File Structure
`static/`
  `styles.css` (Main entry)
  `css/`
    `variables.css`
    `reset.css`
    `layout.css`
    `components.css`
    `tables.css`
    `utils.css`

## File Contents

### `static/styles.css`
```css
@import 'css/variables.css';
@import 'css/reset.css';
@import 'css/layout.css';
@import 'css/components.css';
@import 'css/tables.css';
@import 'css/utils.css';
```

### `static/css/variables.css`
-   `:root` variables.

### `static/css/reset.css`
-   `*`, `body` styles.

### `static/css/layout.css`
-   `main`, `.container`, `header`, `footer`.
-   `.tabs`, `.tab-content`, `.left-col`.
-   Responsive media queries for layout.

### `static/css/components.css`
-   `.section`, `.competition-section`.
-   `.btn-compact`, `.btn-link`.
-   `.error-banner`.
-   `.team-info` (or maybe in tables?).

### `static/css/tables.css`
-   `.table-container`, `table`, `th`, `td`.
-   `.scorers-table` (if specific styles remain).
-   `.match-date`, `.status-*`.

### `static/css/utils.css`
-   `.hidden`, `.no-data`, `.font-bold`.
-   Status color classes.

## Cleanup
-   Remove `#summary-section`, `#generate-summary-btn`, etc.

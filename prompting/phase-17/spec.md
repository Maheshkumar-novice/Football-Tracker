# Phase 17 Specification

## CSS Changes (`static/css/utils.css` or `tables.css`)
```css
@media (max-width: 600px) {
    .hide-mobile {
        display: none;
    }
    
    th, td {
        padding: 8px 4px; /* Reduced padding */
        font-size: 0.85rem;
    }
    
    .team-crest-small {
        width: 16px;
        height: 16px;
    }
}
```

## HTML Changes

### `templates/partials/matches.html`
-   Add `.hide-mobile` to:
    -   Status column (`th` and `td`)
    -   Link column (`th` and `td`) (Maybe? Link is useful. Let's keep Link, hide Status).
    -   Actually, Status is useful too (Live vs Finished).
    -   Let's hide "Date" instead? No, date is critical.
    -   Let's hide "Status" text but keep color? No, table cell.
    -   *Decision*: Hide "Status" column on mobile. The "Result" column often implies status (score vs time).
    -   Also hide "Link" column? Users can search manually.

### `templates/partials/standings.html`
-   Add `.hide-mobile` to:
    -   GF (`th` and `td`)
    -   GA (`th` and `td`)
    -   GD (`th` and `td`)
    -   Maybe "Played" (`th` and `td`)? No, P is standard.

### `templates/partials/scorers.html`
-   Add `.hide-mobile` to:
    -   Assists (`th` and `td`)?
    -   Or just let it scroll. It's only 3 columns (Player, Goals, Assists). It fits.

## Refinement
-   Matches table: Date, Home, Away, Result, Status, Link. (6 cols)
-   Mobile: Date, Home, Away, Result. (4 cols).
-   This fits easily.

-   Standings: #, Team, P, W, D, L, GF, GA, GD, Pts. (10 cols)
-   Mobile: #, Team, P, W, D, L, Pts. (7 cols).
-   Hide GF, GA, GD.

# Mobile Responsiveness Roadmap

Use this checklist to prioritize and track improvements. Say “Do number X” to pick an item.

1. [x] Fluid typography with clamp()
   - Scale titles, breadcrumbs, table headers/cells with CSS `clamp()` for better readability across widths.
   - Files: `static/css/base.css`, `static/css/table.css`

2. [ ] Trim vertical spacing on phones
   - Reduce padding/margins for `.nav-header`, `.container-custom`, and page headers at ≤576px.
   - Files: `static/css/table.css`, `static/css/base.css`

3. [ ] Breadcrumb resilience
   - Allow soft-wrap on two lines and truncate long segments with ellipsis.
   - Files: `static/css/table.css`, `templates/base.html`

4. [ ] Compact attribution on mobile
   - Ensure small font, two-line split, and no overlap; min tap size for links.
   - Files: `static/css/base.css`, `templates/base.html`

5. [ ] Momentum scrolling for tables
   - Add `-webkit-overflow-scrolling: touch;` to `.table-responsive` and `scroll-behavior: smooth`.
   - Files: `static/css/table.css`

6. [ ] Table column alignment
   - Left‑align Name/Branch; center or right‑align numerics for scanability.
   - Files: `static/css/table.css`

7. [ ] Sticky first column on phones
   - Keep Name column visible while horizontal scrolling (use `position: sticky; left:0`).
   - Files: `static/css/table.css`

8. [ ] Increase tap targets to 44px
   - Buttons, sort chips, and filters should meet ~44px min height on phones.
   - Files: `static/css/table.css`, `templates/components/*.html`

9. [ ] Sticky “Show Filters & Search” button (xs)
   - Make the toggle sticky under the header for quick access while scrolling.
   - Files: `templates/table.html`, `static/css/table.css`

10. [ ] Full‑width inputs + larger placeholders (xs)
   - Inputs/selects span 100%; bump placeholder size slightly.
   - Files: `static/css/table.css`, `templates/components/search_filter.html`

11. [ ] Back‑to‑top safe‑area support
   - Respect iOS safe area: `bottom: calc(1rem + env(safe-area-inset-bottom));` and verify z-index.
   - Files: `static/css/table.css`

12. [ ] Fine‑tune mobile table density
   - Slightly increase horizontal cell padding; keep rows readable without crowding.
   - Files: `static/css/table.css`

13. [ ] Prefers‑reduced‑motion support
   - Disable animations/transforms on users preferring reduced motion.
   - Files: `static/css/base.css`, `static/css/table.css`

14. [ ] Visible focus states + contrast check
   - Ensure focus rings are visible; verify small text meets contrast on Nord palette.
   - Files: `static/css/*.css`

15. [ ] Theme color for mobile address bar
   - Add `<meta name="theme-color">` to match the header background.
   - Files: `templates/base.html`

16. [ ] Defer heavy icon fonts
   - Replace Font Awesome icons (arrow/info) with inline SVG; or defer FA loading.
   - Files: `templates/*.html`, remove FA where practical

17. [ ] Preload critical CSS
   - Preload main CSS; consider lazy-loading non-critical styles for faster first paint.
   - Files: `templates/base.html`

18. [ ] Column visibility presets (xs)
   - Optional: allow hiding low-value columns via toggles to keep tables concise.
   - Files: `templates/table.html`, small JS helper

19. [ ] Card view fallback for very narrow screens
   - Render each row as a stacked card (Rank, Name, Branch, key YGPA/avg), with expand for details.
   - Files: `templates/table.html`, `static/css/table.css`, small JS

20. [ ] Container queries (progressive enhancement)
   - Adapt table layout by container width (where supported), not just viewport.
   - Files: `static/css/table.css`

21. [ ] Lighthouse mobile audit + fixes
   - Run Lighthouse mobile; address CLS, TBT, tap target, and contrast issues surfaced.
   - Files: Various

22. [ ] E2E sanity checks on devices
   - Test on iOS Safari/Chrome and Android Chrome (notch safe-areas, sticky, scrolling).
   - Files: N/A (testing task)

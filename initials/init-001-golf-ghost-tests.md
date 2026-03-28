# init-001: Golf Ghost Test Suite

## App Under Test

**Name**: Golf Ghost Online
**URL**: https://ghost.jurigregg.com
**Stack**: Next.js 14 + TypeScript + AWS Lambda + DynamoDB + Cognito
**Repo**: github.com/greggjuri/golf-ghost-online

## What the App Does

Generates realistic golf scores based on a GHIN handicap index. User enters a handicap,
selects a course, submits a form, and the app calls a Lambda API which returns a full
hole-by-hole scorecard with color-coded scores (eagle=green through triple+=red).

## Why This App First

- **Form input** — handicap number field, course selector dropdown
- **Async API call** — Lambda returns scorecard data; Playwright must wait for it
- **DOM assertion** — 18 rows of scorecard data, color-coded cells
- **Public access** — no authentication required to generate a score
- **Real user journey** — covers the complete happy path end-to-end

## Test Scenarios

### 1. Page Load
- Page loads successfully at https://ghost.jurigregg.com
- Page title contains "Golf Ghost"
- Handicap input field is visible and enabled
- Course selector/dropdown is visible and populated with at least one course
- Generate button is visible

### 2. Score Generation — Happy Path
- Enter a valid handicap (e.g., `14.2`)
- Select a course from the dropdown
- Click the Generate Score button
- Wait for the scorecard to appear (async Lambda call)
- Scorecard contains 18 holes
- Total score is visible
- At least one score cell has a color applied (confirms color-coding rendered)

### 3. Scorecard Structure
- Scorecard displays hole numbers 1-18
- Par values are present for each hole
- Score values are present for each hole
- Course handicap row is present

### 4. Input Validation (if applicable)
- Observe behavior with no handicap entered
- Observe behavior with an out-of-range handicap (e.g., `60`)

### 5. Responsive Check
- Page renders correctly at mobile viewport (390x844 — iPhone 14)
- Form elements are visible and usable at mobile width

## POM Design

### File: `pages/golf_ghost_page.py`

Class: `GolfGhostPage(BasePage)`

Key locators to identify (Claude Code should inspect live DOM):
- Handicap input field
- Course selector/dropdown
- Generate Score button
- Scorecard container
- Individual hole rows
- Score cells with color classes
- Total score display

Key methods:
- `load()` — navigate and wait for networkidle
- `enter_handicap(value: str)` — fill handicap input
- `select_course(index: int = 0)` — select first available course
- `generate_score()` — click generate button
- `wait_for_scorecard()` — wait for scorecard to appear after API call
- `get_hole_count() -> int` — count scorecard rows
- `get_total_score() -> str` — read total score value
- `scorecard_is_visible() -> bool`

## Test File

### File: `tests/test_golf_ghost.py`

Classes:
- `TestGolfGhostLoad` — page load and initial state
- `TestGolfGhostScoreGeneration` — full happy path flow
- `TestGolfGhostScorecard` — scorecard structure assertions
- `TestGolfGhostResponsive` — mobile viewport checks

## Technical Notes

- The score generation involves an async Lambda API call — use
  `wait_for_load_state("networkidle")` or wait for the scorecard element
  explicitly. Do NOT use `time.sleep()`.
- Scorecard rendering is JS-driven — wait for the container element, not
  just page load.
- Color coding is applied via CSS classes or inline styles — check which
  and assert presence, not specific colors (colors could change).
- Course dropdown may be populated via an API call on load — wait for
  options to appear before selecting.
- Mobile viewport test: use `page.set_viewport_size({"width": 390, "height": 844})`

## Success Criteria

- [ ] `pages/golf_ghost_page.py` created with POM class
- [ ] `tests/test_golf_ghost.py` created with all test classes
- [ ] `pytest tests/test_golf_ghost.py --browser chromium` passes with zero failures
- [ ] At minimum 8 passing tests covering load, generation, and scorecard structure
- [ ] Committed with message: `feat: add Golf Ghost POM and test suite`

## Out of Scope for This Init

- Testing authenticated admin features (course CRUD)
- Testing specific score values (random generation — non-deterministic)
- Performance/timing assertions
- Firefox and WebKit (Phase 3)

## Open Questions

- None — app is publicly accessible, all test scenarios are read-only

## References

- `docs/DECISIONS.md` ADR-005 — why Golf Ghost was selected as the first target
- `docs/TESTING.md` — locator strategy, assertion standards, waiting patterns
- `CLAUDE.md` — POM class structure and conventions

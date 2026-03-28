# PRP-001: Golf Ghost Test Suite

**Created**: 2026-03-27
**Initial**: `initials/init-001-golf-ghost-tests.md`
**Status**: Complete

---

## Overview

### Problem Statement
Golf Ghost Online (ghost.jurigregg.com) is the first test target for the playwright-suite project. No test coverage currently exists for any app. This PRP also bootstraps the project foundation files (`base_page.py`, `conftest.py`, `pytest.ini`) since the project is brand new.

### Proposed Solution
Create the foundation infrastructure (`conftest.py`, `pytest.ini`, `BasePage`), then build a `GolfGhostPage` POM class and a comprehensive test suite covering page load, score generation (form + async Lambda API), scorecard structure validation, and responsive layout.

### Success Criteria
- [ ] `conftest.py` created with browser fixtures and screenshot-on-failure
- [ ] `pytest.ini` created with configuration and markers
- [ ] `pages/base_page.py` created with shared navigation and title methods
- [ ] `pages/golf_ghost_page.py` created with all locators and methods
- [ ] `tests/test_golf_ghost.py` created with all test classes
- [ ] `pytest tests/test_golf_ghost.py --browser chromium` passes with zero failures
- [ ] At minimum 8 passing tests covering load, generation, scorecard structure, and responsive
- [ ] Committed with message: `feat: add Golf Ghost POM and test suite`

---

## Context

### Related Documentation
- `docs/PLANNING.md` — Architecture overview, Phase 1 scope, test targets
- `docs/DECISIONS.md` — ADR-001 (Playwright), ADR-002 (sync API), ADR-003 (POM), ADR-004 (pinned deps), ADR-005 (target selection)
- `docs/TESTING.md` — Locator strategy priority, assertion standards, waiting patterns
- `CLAUDE.md` — POM class structure, coding conventions, commit rules

### Target App
- **URL**: https://ghost.jurigregg.com
- **Stack**: Next.js 14 + TypeScript + AWS Lambda + DynamoDB + Cognito
- **Auth required**: No (score generation is public)
- **Key behavior**: User enters handicap → selects course → clicks Generate → Lambda API returns hole-by-hole scorecard with color-coded cells

### Dependencies
- **Required**: Python packages installed from `requirements.txt` (playwright 1.58.0, pytest 8.4.2, pytest-playwright 0.7.1, pytest-html 4.2.0)
- **Required**: Browsers installed via `playwright install`
- **Note**: `base_page.py`, `conftest.py`, and `pytest.ini` do not yet exist — this PRP creates them

### Files to Create
```
conftest.py                      # NEW: pytest fixtures, browser setup, screenshot-on-failure
pytest.ini                       # NEW: pytest configuration and markers
pages/__init__.py                # NEW: package init
pages/base_page.py               # NEW: BasePage shared POM class
pages/golf_ghost_page.py         # NEW: GolfGhostPage POM class
tests/__init__.py                # NEW: package init
tests/test_golf_ghost.py         # NEW: Golf Ghost test suite
```

---

## Technical Specification

### conftest.py Design

```python
# conftest.py
import pytest
from pathlib import Path
from playwright.sync_api import Page

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 720}
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / f"{item.name}_{item.config.option.browser[0]}.png"
            page.screenshot(path=str(screenshot_path))
```

### pytest.ini Design

```ini
[pytest]
addopts = --browser chromium -v
markers =
    smoke: Quick sanity checks
    slow: Tests that involve API calls or longer waits
```

### BasePage Class Design

```python
# pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page
        self.base_url = "https://jurigregg.com"

    def navigate(self, path: str = "") -> None:
        self.page.goto(f"{self.base_url}{path}")

    def get_title(self) -> str:
        return self.page.title()
```

### GolfGhostPage POM Class Design

```python
# pages/golf_ghost_page.py
from pages.base_page import BasePage

class GolfGhostPage(BasePage):
    # Locators — class-level constants
    HANDICAP_INPUT = ...          # Identify via get_by_role or get_by_label
    COURSE_SELECTOR = ...         # Dropdown/select for course selection
    GENERATE_BUTTON = ...         # get_by_role("button", name=...) preferred
    SCORECARD_CONTAINER = ...     # Container element for rendered scorecard
    HOLE_ROWS = ...               # Individual hole rows within scorecard
    TOTAL_SCORE = ...             # Total score display element
    SCORE_CELLS = ...             # Individual score cells (for color check)

    def __init__(self, page):
        super().__init__(page)
        self.base_url = "https://ghost.jurigregg.com"

    def load(self) -> None:
        self.navigate()
        self.page.wait_for_load_state("networkidle")

    def enter_handicap(self, value: str) -> None:
        # Use get_by_role or get_by_label to find handicap input
        # Fill with provided value
        pass

    def select_course(self, index: int = 0) -> None:
        # Wait for course options to be populated (API-loaded)
        # Select course at given index
        pass

    def generate_score(self) -> None:
        # Click the generate button
        pass

    def wait_for_scorecard(self) -> None:
        # Wait for scorecard container to appear after Lambda API call
        # Use expect().to_be_visible(timeout=15000) for Lambda cold start
        pass

    def get_hole_count(self) -> int:
        # Count scorecard hole rows
        pass

    def get_total_score(self) -> str:
        # Read total score text content
        pass

    def scorecard_is_visible(self) -> bool:
        # Check if scorecard container is visible
        pass

    def has_colored_score_cells(self) -> bool:
        # Check if at least one score cell has a color class/style
        pass
```

**Note**: Exact locator selectors must be determined by inspecting the live DOM at https://ghost.jurigregg.com during implementation. The executor should use headed mode (`--headed`) or `page.pause()` to identify the correct selectors using the locator priority order (role > text > label > CSS).

### Test Class Structure

```python
# tests/test_golf_ghost.py
import pytest
from playwright.sync_api import expect
from pages.golf_ghost_page import GolfGhostPage

class TestGolfGhostLoad:
    """Tests for initial page load and visible state."""

    def test_page_loads(self, page): ...
    def test_page_title_contains_golf_ghost(self, page): ...
    def test_handicap_input_visible(self, page): ...
    def test_course_selector_visible(self, page): ...
    def test_generate_button_visible(self, page): ...

class TestGolfGhostScoreGeneration:
    """Tests for the full score generation happy path."""

    def test_generate_score_happy_path(self, page): ...
    def test_scorecard_has_18_holes(self, page): ...
    def test_total_score_displayed(self, page): ...
    def test_score_cells_have_color(self, page): ...

class TestGolfGhostScorecard:
    """Tests for scorecard structure and content."""

    def test_hole_numbers_1_through_18(self, page): ...
    def test_par_values_present(self, page): ...
    def test_course_handicap_row_present(self, page): ...

class TestGolfGhostResponsive:
    """Tests for mobile viewport rendering."""

    def test_mobile_page_renders(self, page): ...
    def test_mobile_form_elements_usable(self, page): ...
```

### Locator Strategy

| Element | Priority | Planned Approach |
|---------|----------|------------------|
| Handicap input | 1: `get_by_role` / 3: `get_by_label` | Look for input with role or associated label |
| Course dropdown | 3: `get_by_label` / 5: CSS | Select/dropdown element — label or CSS |
| Generate button | 1: `get_by_role("button")` | Button role with name text |
| Scorecard container | 5: CSS | Likely a div/table — CSS selector |
| Hole rows | 5: CSS | Table rows or repeated elements |
| Score cells | 5: CSS | Cells within rows — check class/style for color |
| Total score | 2: `get_by_text` / 5: CSS | Text content or labeled element |

**Final selectors will be confirmed against the live DOM during execution.**

---

## Implementation Steps

### Step 0: Create Foundation Files (Prerequisites)
**Files**: `conftest.py`, `pytest.ini`, `pages/__init__.py`, `pages/base_page.py`, `tests/__init__.py`

Since the project has no source files yet, create the foundational infrastructure:
1. Create `pytest.ini` with default Chromium browser and markers
2. Create `conftest.py` with the `page` fixture (viewport 1280x720) and screenshot-on-failure hook
3. Create `pages/__init__.py` (empty)
4. Create `pages/base_page.py` with `BasePage` class (navigate, get_title)
5. Create `tests/__init__.py` (empty)

**Validation**:
- [ ] `pytest --collect-only` runs without errors (even if no tests collected)
- [ ] `pages/base_page.py` follows CLAUDE.md POM pattern exactly

---

### Step 1: Inspect Live DOM
**Target**: https://ghost.jurigregg.com

Before writing the POM class, inspect the live app to identify actual element selectors:
1. Navigate to the app in headed mode or use `page.pause()`
2. Identify the handicap input (tag, role, label, placeholder)
3. Identify the course selector (select element? custom dropdown? API-loaded options?)
4. Identify the generate button (text, role)
5. Trigger a score generation and inspect the scorecard DOM structure
6. Identify scorecard container, hole rows, score cells, total score, and color mechanism (CSS classes vs inline styles)
7. Document all selectors for use in the POM class

**Validation**:
- [ ] All 7 key elements have confirmed selectors
- [ ] Color mechanism identified (class names or inline styles)

---

### Step 2: Create POM Class
**File**: `pages/golf_ghost_page.py`

Create the `GolfGhostPage` class inheriting from `BasePage`:
- Override `base_url` to `https://ghost.jurigregg.com`
- Define all locators as class-level constants using the selectors confirmed in Step 1
- Implement all methods: `load()`, `enter_handicap()`, `select_course()`, `generate_score()`, `wait_for_scorecard()`, `get_hole_count()`, `get_total_score()`, `scorecard_is_visible()`, `has_colored_score_cells()`
- Use Playwright auto-waiting and `expect()` where appropriate — **no `time.sleep()`**
- Use `timeout=15000` for scorecard appearance (Lambda cold start risk)

**Validation**:
- [ ] File under 500 lines
- [ ] All locators are class-level constants (none inline in methods)
- [ ] `load()` uses `wait_for_load_state("networkidle")`
- [ ] No `time.sleep()` anywhere
- [ ] `grep -r "time.sleep" pages/` returns nothing

---

### Step 3: Create Test Suite
**File**: `tests/test_golf_ghost.py`

Create test classes and methods covering all scenarios from the init spec:

**TestGolfGhostLoad** (5 tests):
1. `test_page_loads` — navigate, assert page reached networkidle
2. `test_page_title_contains_golf_ghost` — title contains "Golf Ghost"
3. `test_handicap_input_visible` — input field is visible and enabled
4. `test_course_selector_visible` — dropdown is visible with at least 1 option
5. `test_generate_button_visible` — button is visible

**TestGolfGhostScoreGeneration** (4 tests):
1. `test_generate_score_happy_path` — enter handicap 14.2, select course, click generate, scorecard appears
2. `test_scorecard_has_18_holes` — after generation, 18 hole rows present
3. `test_total_score_displayed` — total score is visible and non-empty
4. `test_score_cells_have_color` — at least one cell has color applied

**TestGolfGhostScorecard** (3 tests):
1. `test_hole_numbers_1_through_18` — hole number labels present
2. `test_par_values_present` — par values exist for each hole
3. `test_course_handicap_row_present` — handicap row exists in scorecard

**TestGolfGhostResponsive** (2 tests):
1. `test_mobile_page_renders` — page loads at 390x844 viewport
2. `test_mobile_form_elements_usable` — form elements visible at mobile width

Every `assert` must include a descriptive failure message.

**Validation**:
- [ ] `pytest tests/test_golf_ghost.py --browser chromium -v` passes
- [ ] All assertions have descriptive messages
- [ ] No `time.sleep()` anywhere
- [ ] File under 500 lines
- [ ] At least 8 tests (target: 14)

---

### Step 4: Run Full Suite and Confirm
**Command**:
```bash
pytest tests/ --browser chromium --html=reports/report.html -v
```

**Validation**:
- [ ] All tests pass with zero failures
- [ ] HTML report generated at `reports/report.html`
- [ ] `grep -r "time.sleep" tests/ pages/` returns nothing

---

### Step 5: Commit
```bash
git add conftest.py pytest.ini pages/ tests/
git commit -m "feat: add Golf Ghost POM and test suite"
```

---

## Testing Requirements

### Test Scenarios
| Class | Test Method | Scenario |
|-------|-------------|----------|
| `TestGolfGhostLoad` | `test_page_loads` | Page reaches networkidle at ghost.jurigregg.com |
| `TestGolfGhostLoad` | `test_page_title_contains_golf_ghost` | Title contains "Golf Ghost" |
| `TestGolfGhostLoad` | `test_handicap_input_visible` | Handicap input is visible and enabled |
| `TestGolfGhostLoad` | `test_course_selector_visible` | Course dropdown is visible with options |
| `TestGolfGhostLoad` | `test_generate_button_visible` | Generate button is visible |
| `TestGolfGhostScoreGeneration` | `test_generate_score_happy_path` | Full flow: handicap → course → generate → scorecard |
| `TestGolfGhostScoreGeneration` | `test_scorecard_has_18_holes` | Scorecard contains 18 hole entries |
| `TestGolfGhostScoreGeneration` | `test_total_score_displayed` | Total score is visible and non-empty |
| `TestGolfGhostScoreGeneration` | `test_score_cells_have_color` | At least one cell has color styling |
| `TestGolfGhostScorecard` | `test_hole_numbers_1_through_18` | Hole numbers 1-18 present in scorecard |
| `TestGolfGhostScorecard` | `test_par_values_present` | Par values shown for each hole |
| `TestGolfGhostScorecard` | `test_course_handicap_row_present` | Course handicap row exists |
| `TestGolfGhostResponsive` | `test_mobile_page_renders` | Page renders at 390x844 (iPhone 14) |
| `TestGolfGhostResponsive` | `test_mobile_form_elements_usable` | Form inputs accessible at mobile width |

### Waiting Patterns Required
- `wait_for_load_state("networkidle")` after initial navigation
- `expect(scorecard_container).to_be_visible(timeout=15000)` after clicking Generate (Lambda cold start)
- Wait for course dropdown options to be populated before selecting (may be API-loaded on page init)

---

## Integration Test Plan

After `pytest` passes:

| Step | Action | Expected Result | Pass? |
|------|--------|-----------------|-------|
| 1 | `pytest tests/test_golf_ghost.py --browser chromium -v` | All 14 tests green | ☐ |
| 2 | `pytest tests/test_golf_ghost.py --headed --slowmo 500` | Watch tests run visually, no errors | ☐ |
| 3 | Open `reports/report.html` | Report shows all passing | ☐ |

---

## Error Handling

### Known Flakiness Risks
| Risk | Cause | Mitigation |
|------|-------|------------|
| Scorecard slow to appear | Lambda cold start (first invocation after idle) | Use `timeout=15000` on scorecard visibility assertion |
| Course dropdown empty | API call to populate courses may be slow | Wait for at least 1 option element before selecting |
| Color assertion fragile | Color mechanism may use CSS classes or inline styles | Assert *presence* of any color styling, not specific values |
| Score values non-deterministic | Random generation by design | Never assert specific score values — only structure |

### Edge Cases
- **Input validation tests** (Scenario 4): These are observational — if the app has no validation, the tests should still pass by documenting the behavior rather than asserting specific error messages. Mark as `@pytest.mark.skip` with reason if validation doesn't exist.
- **Lambda cold start**: First test run of the day may be slower. The 15-second timeout accommodates this.

---

## Rollback Plan

Tests are purely additive — they do not modify the target app.

1. Delete `pages/golf_ghost_page.py`
2. Delete `tests/test_golf_ghost.py`
3. Optionally keep `conftest.py`, `pytest.ini`, and `base_page.py` (shared infrastructure)
4. Run `pytest tests/` to confirm remaining suite still passes (will be empty)

---

## Confidence Scores

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| Clarity | **9** | Init spec is detailed — 5 scenarios with specific assertions, POM design, and file structure |
| Feasibility | **7** | App is publicly accessible; locators unknown until live DOM inspection (Step 1). Next.js rendering could make some elements tricky to locate. Lambda cold start is a known timing risk. |
| Completeness | **9** | PRP covers foundation files, POM class, full test suite, responsive tests, and commit step |
| Alignment | **10** | Follows POM pattern (ADR-003), sync API (ADR-002), pinned deps (ADR-004), no `time.sleep()`, locator priority from TESTING.md |
| **Average** | **8.75** | Confidence is high. Primary risk is locator discovery on the live DOM. |

---

## Notes

- **This is the first PRP** — it also bootstraps `conftest.py`, `pytest.ini`, and `base_page.py` which future PRPs will depend on.
- **Locators are TBD** — the executor must inspect the live DOM at https://ghost.jurigregg.com during Step 1 before writing the POM class. Use `--headed` mode or `page.pause()`.
- **Score values are random** — never assert specific scores. Only assert structure (18 holes, totals present, colors applied).
- **Input validation tests** (Scenario 4 from init) are lower priority. If the app doesn't expose validation behavior, skip those tests with `@pytest.mark.skip(reason="no client-side validation detected")`.
- **Course dropdown** may load via API on page init — the POM's `select_course()` must wait for options to be available before selecting.

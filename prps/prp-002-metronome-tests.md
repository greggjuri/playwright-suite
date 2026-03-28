# PRP-002: Metronome Test Suite

**Created**: 2026-03-27
**Initial**: `initials/init-002-metronome-tests.md`
**Status**: Complete

---

## Overview

### Problem Statement
The Online Metronome (metronome.jurigregg.com) is the second test target for the playwright-suite project. It is a pure HTML/JS single-page app with no routing or API calls — testing it covers JS-rendered UI controls, keyboard interactions, theme toggling with localStorage persistence, and visual beat state changes.

### Proposed Solution
Build a `MetronomePage` POM class and a comprehensive test suite covering page load, BPM input, start/stop via button and spacebar, theme toggle with localStorage persistence, and responsive layout.

### Success Criteria
- [ ] `pages/metronome_page.py` created with all locators and methods
- [ ] `tests/test_metronome.py` created with all test classes
- [ ] `pytest tests/test_metronome.py --browser chromium` passes with zero failures
- [ ] At minimum 10 passing tests
- [ ] Full suite still passing: `pytest tests/ --browser chromium`
- [ ] Committed with message: `feat: add Metronome POM and test suite`

---

## Context

### Related Documentation
- `docs/PLANNING.md` — Architecture overview, Phase 2 scope
- `docs/DECISIONS.md` — ADR-001 (Playwright), ADR-002 (sync API), ADR-003 (POM), ADR-005 (target selection)
- `docs/TESTING.md` — Locator strategy priority, assertion standards, waiting patterns
- `CLAUDE.md` — POM class structure, coding conventions, commit rules

### Target App
- **URL**: https://metronome.jurigregg.com
- **Stack**: Single HTML file with embedded CSS/JS on S3 + CloudFront
- **Auth required**: No
- **Key behavior**: Set BPM → click Start (or press spacebar) → visual beat boxes highlight in sequence → click Stop to pause. Theme toggle switches dark/light and persists to localStorage.

### Dependencies
- **Required**: `pages/base_page.py` (exists)
- **Required**: `conftest.py` browser fixtures (exists)

### Files to Create
```
pages/metronome_page.py          # NEW: POM class for Metronome
tests/test_metronome.py          # NEW: Test suite for Metronome
```

---

## Technical Specification

### POM Class Design

```python
# pages/metronome_page.py
from pages.base_page import BasePage

class MetronomePage(BasePage):
    # Form/control locators (all confirmed from live DOM inspection)
    BPM_INPUT = '[aria-label="Beats per minute"]'
    START_BUTTON = '[aria-label="Start metronome"]'
    STOP_BUTTON = '[aria-label="Stop metronome"]'
    BEAT_COUNTER = '[aria-label="Beat counter"]'
    BEAT_BOXES = '.beat'
    ACTIVE_BEAT = '.beat.active'
    THEME_TOGGLE = '[aria-label="Toggle dark mode"]'
    CLEAR_BUTTON = '[aria-label="Clear"]'
    BACKSPACE_BUTTON = '[aria-label="Backspace"]'

    def __init__(self, page):
        super().__init__(page)
        self.base_url = "https://metronome.jurigregg.com"

    def load(self) -> None:
        self.navigate()
        self.page.wait_for_load_state("networkidle")

    def get_bpm(self) -> str:
        return self.page.locator(self.BPM_INPUT).input_value()

    def set_bpm(self, value: str) -> None:
        self.page.locator(self.BPM_INPUT).fill(value)

    def click_start(self) -> None:
        self.page.locator(self.START_BUTTON).click()

    def click_stop(self) -> None:
        self.page.locator(self.STOP_BUTTON).click()

    def press_spacebar(self) -> None:
        self.page.keyboard.press("Space")

    def is_running(self) -> bool:
        return self.page.locator(self.STOP_BUTTON).is_visible()

    def has_active_beat(self) -> bool:
        return self.page.locator(self.ACTIVE_BEAT).count() > 0

    def get_beat_box_count(self) -> int:
        return self.page.locator(self.BEAT_BOXES).count()

    def click_theme_toggle(self) -> None:
        self.page.locator(self.THEME_TOGGLE).click()

    def get_theme(self) -> str:
        return self.page.evaluate("document.documentElement.dataset.theme")

    def get_stored_theme(self) -> str:
        return self.page.evaluate("localStorage.getItem('metronome-theme')")

    def get_scroll_y(self) -> float:
        return self.page.evaluate("window.scrollY")
```

### Test Class Structure

```python
# tests/test_metronome.py
import pytest
from playwright.sync_api import expect
from pages.metronome_page import MetronomePage

class TestMetronomeLoad:
    """Tests for initial page load and visible state."""
    # test_page_loads
    # test_page_title_contains_metronome
    # test_bpm_input_visible_with_default
    # test_start_button_visible
    # test_beat_display_visible
    # test_theme_toggle_visible

class TestMetronomeBPM:
    """Tests for BPM input interactions."""
    # test_bpm_accepts_valid_value
    # test_default_bpm_in_range

class TestMetronomeControls:
    """Tests for start/stop via button and spacebar."""
    # test_start_button_changes_state
    # test_stop_button_returns_to_stopped
    # test_active_beat_when_running
    # test_no_active_beat_when_stopped
    # test_spacebar_starts_metronome
    # test_spacebar_stops_metronome
    # test_spacebar_does_not_scroll

class TestMetronomeTheme:
    """Tests for theme toggle and localStorage persistence."""
    # test_theme_toggle_changes_theme
    # test_theme_persists_after_reload

class TestMetronomeResponsive:
    """Tests for mobile viewport rendering."""
    # test_mobile_page_renders
    # test_mobile_controls_usable
```

### Locator Strategy

All locators confirmed from the live DOM inspection in the init spec.

| Element | Strategy | Selector | Priority |
|---------|----------|----------|----------|
| BPM input | aria-label | `[aria-label="Beats per minute"]` | 1 (role/aria) |
| Start button | aria-label | `[aria-label="Start metronome"]` | 1 (role/aria) |
| Stop button | aria-label | `[aria-label="Stop metronome"]` | 1 (role/aria) |
| Beat counter | aria-label | `[aria-label="Beat counter"]` | 1 (role/aria) |
| Beat boxes | CSS class | `.beat` | 5 (CSS) |
| Active beat | CSS class | `.beat.active` | 5 (CSS) |
| Theme toggle | aria-label | `[aria-label="Toggle dark mode"]` | 1 (role/aria) |
| Clear button | aria-label | `[aria-label="Clear"]` | 1 (role/aria) |

---

## Implementation Steps

### Step 1: Create POM Class
**File**: `pages/metronome_page.py`

Create the `MetronomePage` class inheriting from `BasePage`:
- Override `base_url` to `https://metronome.jurigregg.com`
- Define all locators as class-level constants using confirmed aria-label selectors
- Implement all methods from the POM Design section
- Use `page.evaluate()` for localStorage and dataset reads
- **No `time.sleep()`**

**Validation**:
- [ ] File under 500 lines
- [ ] All locators are class-level constants
- [ ] `load()` uses `wait_for_load_state("networkidle")`
- [ ] No `time.sleep()`

---

### Step 2: Create Test Suite
**File**: `tests/test_metronome.py`

**TestMetronomeLoad** (6 tests):
1. `test_page_loads` — URL contains metronome.jurigregg.com
2. `test_page_title_contains_metronome` — title contains "Metronome"
3. `test_bpm_input_visible_with_default` — BPM input visible, default value between 40-220
4. `test_start_button_visible` — Start button visible
5. `test_beat_display_visible` — Beat counter visible with 4 beat boxes
6. `test_theme_toggle_visible` — Theme toggle visible

**TestMetronomeBPM** (2 tests):
1. `test_bpm_accepts_valid_value` — fill "100", read back "100"
2. `test_default_bpm_in_range` — default BPM is between 40 and 220

**TestMetronomeControls** (7 tests):
1. `test_start_button_changes_state` — click Start, Stop button becomes visible
2. `test_stop_button_returns_to_stopped` — click Start then Stop, Start button returns
3. `test_active_beat_when_running` — start metronome, at least one `.beat.active` appears
4. `test_no_active_beat_when_stopped` — after stopping, no `.beat.active` exists
5. `test_spacebar_starts_metronome` — press Space, Stop button becomes visible
6. `test_spacebar_stops_metronome` — press Space twice, Start button returns
7. `test_spacebar_does_not_scroll` — scrollY stays 0 after spacebar press

**TestMetronomeTheme** (2 tests):
1. `test_theme_toggle_changes_theme` — toggle, dataset.theme changes
2. `test_theme_persists_after_reload` — toggle, reload, theme still matches

**TestMetronomeResponsive** (2 tests):
1. `test_mobile_page_renders` — page loads at 390x844
2. `test_mobile_controls_usable` — BPM input and Start button visible at mobile

Total: **19 tests**

Every `assert` must include a descriptive failure message.

**Validation**:
- [ ] `pytest tests/test_metronome.py --browser chromium -v` passes
- [ ] All assertions have descriptive messages
- [ ] No `time.sleep()`
- [ ] File under 500 lines

---

### Step 3: Run Full Suite and Confirm No Regressions
**Command**:
```bash
pytest tests/ --browser chromium --html=reports/report.html -v
```

**Validation**:
- [ ] All new Metronome tests pass
- [ ] All existing Golf Ghost tests still pass
- [ ] HTML report generated at `reports/report.html`
- [ ] `grep -r "time.sleep" tests/ pages/` returns nothing

---

### Step 4: Commit
```bash
git add pages/metronome_page.py tests/test_metronome.py
git commit -m "feat: add Metronome POM and test suite"
```

---

## Testing Requirements

### Test Scenarios
| Class | Test Method | Scenario |
|-------|-------------|----------|
| `TestMetronomeLoad` | `test_page_loads` | Page reaches networkidle at metronome.jurigregg.com |
| `TestMetronomeLoad` | `test_page_title_contains_metronome` | Title contains "Metronome" |
| `TestMetronomeLoad` | `test_bpm_input_visible_with_default` | BPM input visible with default 40-220 |
| `TestMetronomeLoad` | `test_start_button_visible` | Start button visible on load |
| `TestMetronomeLoad` | `test_beat_display_visible` | 4 beat boxes visible |
| `TestMetronomeLoad` | `test_theme_toggle_visible` | Theme toggle visible |
| `TestMetronomeBPM` | `test_bpm_accepts_valid_value` | Fill "100", read back "100" |
| `TestMetronomeBPM` | `test_default_bpm_in_range` | Default BPM is 40-220 |
| `TestMetronomeControls` | `test_start_button_changes_state` | Click Start → Stop button visible |
| `TestMetronomeControls` | `test_stop_button_returns_to_stopped` | Click Start then Stop → Start returns |
| `TestMetronomeControls` | `test_active_beat_when_running` | Running → `.beat.active` exists |
| `TestMetronomeControls` | `test_no_active_beat_when_stopped` | Stopped → no `.beat.active` |
| `TestMetronomeControls` | `test_spacebar_starts_metronome` | Space → Stop button visible |
| `TestMetronomeControls` | `test_spacebar_stops_metronome` | Space twice → Start button returns |
| `TestMetronomeControls` | `test_spacebar_does_not_scroll` | scrollY stays 0 after Space |
| `TestMetronomeTheme` | `test_theme_toggle_changes_theme` | Toggle → dataset.theme changes |
| `TestMetronomeTheme` | `test_theme_persists_after_reload` | Toggle → reload → theme persists |
| `TestMetronomeResponsive` | `test_mobile_page_renders` | Page loads at 390x844 |
| `TestMetronomeResponsive` | `test_mobile_controls_usable` | Controls visible at mobile width |

### Waiting Patterns Required
- `wait_for_load_state("networkidle")` after navigation
- `expect(stop_button).to_be_visible()` after clicking Start (brief delay for JS state change)
- `expect(active_beat).to_be_visible()` after starting — beat animation may take one beat cycle (~500ms at 120 BPM)
- After stopping: `expect(start_button).to_be_visible()` to confirm state returned

---

## Integration Test Plan

After `pytest` passes:

| Step | Action | Expected Result | Pass? |
|------|--------|-----------------|-------|
| 1 | `pytest tests/test_metronome.py --browser chromium -v` | All 19 tests green | ☐ |
| 2 | `pytest tests/ --browser chromium -v` | All tests green (Golf Ghost + Metronome) | ☐ |
| 3 | `pytest tests/test_metronome.py --headed --slowmo 500` | Watch tests run visually, no errors | ☐ |
| 4 | Open `reports/report.html` | Report shows all passing | ☐ |

---

## Error Handling

### Known Flakiness Risks
| Risk | Cause | Mitigation |
|------|-------|------------|
| Active beat not yet visible | Beat animation takes one cycle to highlight | Use `expect().to_be_visible(timeout=3000)` — at 120 BPM one beat = 500ms |
| Start/Stop state transition | JS event handler may have brief delay | Use `expect()` with auto-retry for button state assertions |
| Theme persistence test | Page reload timing | Use `wait_for_load_state("networkidle")` after reload |
| Web Audio context blocked | Browser autoplay policy may block audio | Tests only check UI state, not audio — unaffected |

### Edge Cases
- **Spacebar scroll**: Confirm `window.scrollY === 0` before and after pressing Space to verify `preventDefault` works
- **Theme toggle idempotency**: Don't assume initial theme is "dark" or "light" — read it first, then assert it changed after toggle

---

## Rollback Plan

Tests are purely additive — they do not modify the target app.

1. Delete `pages/metronome_page.py`
2. Delete `tests/test_metronome.py`
3. Run `pytest tests/` to confirm Golf Ghost suite still passes

---

## Confidence Scores

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| Clarity | **10** | Init spec includes confirmed DOM selectors from live inspection — no guesswork |
| Feasibility | **9** | All locators use aria-labels confirmed on the live DOM. Only risk is beat animation timing. |
| Completeness | **9** | PRP covers POM + 19 tests across 5 classes: load, BPM, controls, theme, responsive |
| Alignment | **10** | Follows POM pattern (ADR-003), sync API (ADR-002), no `time.sleep()`, aria-label locators (priority 1) |
| **Average** | **9.5** | High confidence. All selectors pre-confirmed. |

---

## Notes

- **All locators pre-confirmed** — the init spec includes live DOM inspection results with exact aria-labels, unlike PRP-001 which required runtime discovery.
- **Audio is untestable** — Web Audio API output cannot be asserted by Playwright. All tests focus on UI state changes only.
- **`page.fill()` for BPM** — although the app has an on-screen numpad, direct `page.fill()` on the input is simpler and more reliable for testing.
- **Theme test must be order-independent** — read the initial theme, toggle, assert it changed to the opposite. Don't hardcode "dark" or "light".

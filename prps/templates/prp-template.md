# PRP Template

## PRP-XXX: {Feature Name}

**Created**: {YYYY-MM-DD}  
**Initial**: `initials/init-{feature}.md`  
**Status**: Draft/Ready/In Progress/Complete

---

## Overview

### Problem Statement
{Which app is being tested and what gaps in test coverage does this address?}

### Proposed Solution
{High-level description of the POM class(es) and test suite being built.}

### Success Criteria
- [ ] `pages/{app}_page.py` created with all locators and methods
- [ ] `tests/test_{app}.py` created with all test classes
- [ ] `pytest tests/test_{app}.py --browser chromium` passes with zero failures
- [ ] {Specific test count or scenario criterion}
- [ ] Committed with message: `feat: add {App} POM and test suite`

---

## Context

### Related Documentation
- `docs/PLANNING.md` — Architecture overview and test targets
- `docs/DECISIONS.md` — ADR-003 (POM pattern), ADR-002 (sync API), ADR-004 (pinned deps)
- `docs/TESTING.md` — Locator strategy, assertion standards, waiting patterns
- `CLAUDE.md` — POM class structure and coding conventions

### Target App
- **URL**: {https://app.jurigregg.com}
- **Stack**: {Next.js / Pure HTML+JS / React / etc.}
- **Auth required**: No (all test scenarios are public)

### Dependencies
- **Required**: `pages/base_page.py` must exist
- **Required**: `conftest.py` browser fixtures must be working
- **Optional**: {Other POM classes if shared patterns exist}

### Files to Create
```
pages/{app}_page.py          # NEW: POM class for {App}
tests/test_{app}.py          # NEW: Test suite for {App}
```

---

## Technical Specification

### POM Class Design

```python
# pages/{app}_page.py
from pages.base_page import BasePage

class {App}Page(BasePage):
    # Locators — all as class-level constants
    {ELEMENT_NAME} = "{css-selector or role}"
    {ELEMENT_NAME} = "{css-selector or role}"

    def __init__(self, page):
        super().__init__(page)

    def load(self) -> None:
        """Navigate to app and wait for full load."""
        self.navigate("{/path}")
        self.page.wait_for_load_state("networkidle")

    def {action_method}(self) -> None:
        """Description."""
        pass

    def {query_method}(self) -> str:
        """Description."""
        return self.page.locator(self.{ELEMENT_NAME}).text_content()
```

### Test Class Structure

```python
# tests/test_{app}.py
import pytest
from playwright.sync_api import expect
from pages.{app}_page import {App}Page

class Test{App}Load:
    """Tests for initial page load and visible state."""

class Test{App}{Feature}:
    """Tests for {feature} functionality."""
```

### Locator Strategy
List the key elements and planned locator approach (in priority order):

| Element | Locator Strategy | Selector |
|---------|-----------------|----------|
| {Element} | get_by_role / CSS | {value} |
| {Element} | get_by_text | {value} |

---

## Implementation Steps

### Step 1: Create POM Class
**File**: `pages/{app}_page.py`

Create the Page Object Model class inheriting from `BasePage`. Define all locators
as class-level constants. Implement `load()` and all action/query methods.

**Validation**:
- [ ] File created under 500 lines
- [ ] All locators defined as class constants (none inline)
- [ ] `load()` uses `wait_for_load_state("networkidle")`
- [ ] No `time.sleep()` anywhere

---

### Step 2: Create Test Suite
**File**: `tests/test_{app}.py`

Create test classes and methods covering all scenarios from the init spec.
Every `assert` must include a descriptive failure message.

**Validation**:
- [ ] `pytest tests/test_{app}.py --browser chromium -v` passes
- [ ] All assertions have descriptive messages
- [ ] No `time.sleep()` anywhere
- [ ] File under 500 lines

---

### Step 3: Run Full Suite and Confirm No Regressions
**Command**:
```bash
pytest tests/ --browser chromium --html=reports/report.html -v
```

**Validation**:
- [ ] All new tests pass
- [ ] No existing tests broken
- [ ] HTML report generated at `reports/report.html`
- [ ] `grep -r "time.sleep" tests/ pages/` returns nothing

---

### Step 4: Commit
```bash
git add pages/{app}_page.py tests/test_{app}.py
git commit -m "feat: add {App} POM and test suite"
```

---

## Testing Requirements

### Test Scenarios
| Class | Test Method | Scenario |
|-------|-------------|----------|
| `Test{App}Load` | `test_page_loads` | Page reaches networkidle state |
| `Test{App}Load` | `test_{element}_visible` | Key element is present on load |
| `Test{App}{Feature}` | `test_{scenario}` | {Description} |

### Waiting Patterns Required
- {e.g., `wait_for_load_state("networkidle")` after navigation}
- {e.g., `expect(locator).to_be_visible(timeout=10000)` for async content}

---

## Integration Test Plan

After `pytest` passes:

| Step | Action | Expected Result | Pass? |
|------|--------|-----------------|-------|
| 1 | `pytest tests/test_{app}.py --browser chromium -v` | All tests green | ☐ |
| 2 | `pytest tests/test_{app}.py --headed --slowmo 500` | Watch tests run visually, no errors | ☐ |
| 3 | Open `reports/report.html` | Report shows all passing, no missing screenshots | ☐ |

---

## Error Handling

### Known Flakiness Risks
| Risk | Cause | Mitigation |
|------|-------|------------|
| {e.g., API-driven content} | {Lambda cold start} | {Use explicit timeout on locator} |

### Edge Cases
- {Edge case 1 and how it's handled in tests}

---

## Rollback Plan

Tests are purely additive — they do not modify the target app.

1. Delete `pages/{app}_page.py`
2. Delete `tests/test_{app}.py`
3. Run `pytest tests/` to confirm remaining suite still passes

---

## Confidence Scores

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| Clarity | X | {Are test scenarios unambiguous?} |
| Feasibility | X | {Can target elements be reliably located?} |
| Completeness | X | {Does PRP cover full POM + test file?} |
| Alignment | X | {Follows POM pattern, no time.sleep(), locator priority?} |
| **Average** | **X** | |

{If average < 7, list specific concerns before proceeding}

---

## Notes

{Any additional context — known DOM quirks, timing considerations, etc.}

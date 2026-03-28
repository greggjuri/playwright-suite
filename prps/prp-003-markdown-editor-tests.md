# PRP-003: Markdown Editor Test Suite

**Created**: 2026-03-28
**Initial**: `initials/init-003-markdown-editor-tests.md`
**Status**: Complete

---

## Overview

### Problem Statement
The Markdown Editor (jurigregg.com/md/) is the third and final Phase 2 test target. It is a feature-rich pure HTML/CSS/JS app with the widest variety of Playwright interactions: textarea input, live preview sync, toolbar buttons, keyboard shortcuts, theme toggle, auto-save to localStorage, word/character count, and a cheat sheet panel.

### Proposed Solution
Build a `MarkdownPage` POM class and a comprehensive test suite covering page load, editor-to-preview sync, word count, toolbar formatting, keyboard shortcuts, cheat sheet toggle, theme toggle with persistence, draft auto-save with persistence, clear draft, and responsive layout.

### Success Criteria
- [ ] `pages/markdown_page.py` created with all locators and methods
- [ ] `tests/test_markdown_editor.py` created with all test classes
- [ ] `pytest tests/test_markdown_editor.py --browser chromium` passes with zero failures
- [ ] At minimum 15 passing tests
- [ ] Full suite still passing: `pytest tests/ --browser chromium`
- [ ] Committed with message: `feat: add Markdown Editor POM and test suite`

---

## Context

### Related Documentation
- `docs/PLANNING.md` — Architecture overview, Phase 2 scope
- `docs/DECISIONS.md` — ADR-001 (Playwright), ADR-002 (sync API), ADR-003 (POM), ADR-005 (target selection)
- `docs/TESTING.md` — Locator strategy priority, assertion standards, waiting patterns
- `CLAUDE.md` — POM class structure, coding conventions, commit rules

### Target App
- **URL**: https://jurigregg.com/md/ (trailing slash required)
- **Stack**: Pure HTML/CSS/JS on S3 + CloudFront
- **Auth required**: No
- **Key behavior**: Type markdown in textarea → live HTML preview updates in real time. Toolbar buttons wrap selected text in markdown syntax. Theme and draft persist to localStorage.

### Dependencies
- **Required**: `pages/base_page.py` (exists)
- **Required**: `conftest.py` browser fixtures (exists)

### Files to Create
```
pages/markdown_page.py           # NEW: POM class for Markdown Editor
tests/test_markdown_editor.py    # NEW: Test suite for Markdown Editor
```

---

## Technical Specification

### POM Class Design

```python
# pages/markdown_page.py
from pages.base_page import BasePage

class MarkdownPage(BasePage):
    # Editor locators (confirmed from live DOM)
    EDITOR = "#markdown-input"
    PREVIEW = "#preview-output"
    AUTOSAVE_STATUS = "#autosave-status"
    WORD_COUNT = ".word-count"

    # Control locators
    THEME_TOGGLE = "#theme-toggle"
    CHEATSHEET_TOGGLE = "#cheatsheet-toggle"
    CHEATSHEET_PANEL = "#cheatsheet-panel"
    CLEAR_DRAFT = "#clear-draft"

    # Toolbar locators (no aria-labels — CSS + text match)
    TOOLBAR_BUTTONS = ".toolbar-btn"
    TOOLBAR_BOLD = 'button.toolbar-btn:has-text("B")'

    def __init__(self, page):
        super().__init__(page)
        self.base_url = "https://jurigregg.com"

    def load(self) -> None:
        self.navigate("/md/")
        self.page.wait_for_load_state("networkidle")

    def type_markdown(self, text: str) -> None:
        self.page.locator(self.EDITOR).fill(text)

    def get_editor_value(self) -> str:
        return self.page.locator(self.EDITOR).input_value()

    def get_preview_html(self) -> str:
        return self.page.locator(self.PREVIEW).inner_html()

    def get_word_count_text(self) -> str:
        return self.page.locator(self.WORD_COUNT).text_content()

    def get_autosave_status(self) -> str:
        return self.page.locator(self.AUTOSAVE_STATUS).text_content()

    def click_theme_toggle(self) -> None:
        self.page.locator(self.THEME_TOGGLE).click()

    def get_body_class(self) -> str:
        return self.page.evaluate("document.body.className")

    def is_dark_mode(self) -> bool:
        return "dark-mode" in self.get_body_class()

    def get_stored_theme(self) -> str:
        return self.page.evaluate(
            "localStorage.getItem('markdown-editor-theme')"
        )

    def get_stored_draft(self):
        return self.page.evaluate(
            "localStorage.getItem('markdown-editor-draft')"
        )

    def click_cheatsheet_toggle(self) -> None:
        self.page.locator(self.CHEATSHEET_TOGGLE).click()

    def is_cheatsheet_visible(self) -> bool:
        panel = self.page.locator(self.CHEATSHEET_PANEL)
        cls = panel.get_attribute("class") or ""
        return "hidden" not in cls

    def click_clear_draft(self) -> None:
        self.page.locator(self.CLEAR_DRAFT).click()

    def click_toolbar_bold(self) -> None:
        self.page.locator(self.TOOLBAR_BOLD).click()

    def select_all_editor(self) -> None:
        self.page.locator(self.EDITOR).press("Meta+A")

    def press_bold_shortcut(self) -> None:
        self.page.locator(self.EDITOR).press("Meta+B")
```

### Test Class Structure

```python
# tests/test_markdown_editor.py

class TestMarkdownLoad:             # 6 tests — page load, elements, initial state
class TestMarkdownEditorPreview:    # 3 tests — typing syncs to preview
class TestMarkdownWordCount:        # 2 tests — word/char count updates
class TestMarkdownToolbar:          # 1 test  — Bold button wraps text
class TestMarkdownKeyboard:         # 1 test  — Ctrl/Cmd+B shortcut
class TestMarkdownCheatSheet:       # 2 tests — toggle opens/closes
class TestMarkdownTheme:            # 2 tests — toggle + persistence
class TestMarkdownPersistence:      # 2 tests — draft auto-save + reload
class TestMarkdownClearDraft:       # 1 test  — clear draft empties editor
class TestMarkdownResponsive:       # 2 tests — mobile viewport
```

Total: **22 tests**

### Locator Strategy

| Element | Selector | Notes |
|---------|----------|-------|
| Editor textarea | `#markdown-input` | CSS ID (no aria-label) |
| Preview pane | `#preview-output` | CSS ID |
| Autosave status | `#autosave-status` | CSS ID |
| Word count | `.word-count` | CSS class |
| Theme toggle | `#theme-toggle` | CSS ID |
| Cheatsheet toggle | `#cheatsheet-toggle` | CSS ID |
| Cheatsheet panel | `#cheatsheet-panel` | CSS ID, check for `hidden` class |
| Clear draft | `#clear-draft` | CSS ID |
| Bold toolbar btn | `button.toolbar-btn:has-text("B")` | CSS + text (no aria-label) |
| All toolbar btns | `.toolbar-btn` | CSS class |

**Note**: This app uses CSS IDs throughout with no aria-labels on toolbar buttons. CSS ID selectors are stable and unique, which is acceptable per the locator strategy when no semantic alternative exists.

---

## Implementation Steps

### Step 1: Create POM Class
**File**: `pages/markdown_page.py`

Create the `MarkdownPage` class inheriting from `BasePage`:
- `base_url` stays as `https://jurigregg.com` (inherited), `load()` navigates to `/md/`
- Define all locators as class-level constants
- Implement all methods from POM Design section
- Use `page.evaluate()` for localStorage and body class reads
- The Bold toolbar button selector must be confirmed against the live DOM during execution (init spec notes toolbar buttons lack aria-labels)
- **No `time.sleep()`**

**Validation**:
- [ ] File under 500 lines
- [ ] All locators are class-level constants
- [ ] `load()` navigates to `/md/` with trailing slash
- [ ] No `time.sleep()`

---

### Step 2: Create Test Suite
**File**: `tests/test_markdown_editor.py`

**TestMarkdownLoad** (6 tests):
1. `test_page_loads` — URL contains `jurigregg.com/md`
2. `test_page_title` — title is "Markdown Editor - jurigregg.com"
3. `test_editor_visible` — `#markdown-input` is visible
4. `test_preview_visible` — `#preview-output` is visible
5. `test_toolbar_visible` — at least one `.toolbar-btn` exists
6. `test_word_count_initial` — shows "Words: 0 | Characters: 0" on empty editor

**TestMarkdownEditorPreview** (3 tests):
1. `test_heading_renders` — type `# Hello World`, preview contains `<h1>`
2. `test_bold_renders` — type `**bold text**`, preview contains `<strong>`
3. `test_preview_updates_in_realtime` — type text, preview updates without reload

**TestMarkdownWordCount** (2 tests):
1. `test_empty_editor_count` — "Words: 0 | Characters: 0"
2. `test_count_after_typing` — type "Hello World", count shows "Words: 2 | Characters: 11"

**TestMarkdownToolbar** (1 test):
1. `test_bold_button_wraps_text` — type "Hello", select all, click Bold, editor has `**Hello**`

**TestMarkdownKeyboard** (1 test):
1. `test_bold_shortcut` — type "Hello", select all, press Meta+B, editor has `**Hello**`

**TestMarkdownCheatSheet** (2 tests):
1. `test_cheatsheet_toggle_opens` — click toggle, panel visible
2. `test_cheatsheet_toggle_closes` — click toggle twice, panel hidden again

**TestMarkdownTheme** (2 tests):
1. `test_theme_toggle_changes_class` — toggle, body class changes
2. `test_theme_persists_after_reload` — toggle, reload, body class persists

**TestMarkdownPersistence** (2 tests):
1. `test_autosave_status_updates` — type text, wait for autosave status to update
2. `test_draft_persists_after_reload` — type text, wait for save, reload, editor has text

**TestMarkdownClearDraft** (1 test):
1. `test_clear_draft_empties_editor` — type text, click clear, editor is empty

**TestMarkdownResponsive** (2 tests):
1. `test_mobile_page_renders` — page loads at 390x844
2. `test_mobile_editor_visible` — editor and toolbar visible at mobile width

Every `assert` must include a descriptive failure message.

**Important**: Tests that check empty/initial state (word count, autosave) should clear localStorage first or rely on the fresh browser context provided by conftest.py (each test gets a new context, so localStorage is clean).

**Validation**:
- [ ] `pytest tests/test_markdown_editor.py --browser chromium -v` passes
- [ ] All assertions have descriptive messages
- [ ] No `time.sleep()`
- [ ] File under 500 lines
- [ ] At least 15 tests (target: 22)

---

### Step 3: Run Full Suite and Confirm No Regressions
**Command**:
```bash
pytest tests/ --browser chromium --html=reports/report.html -v
```

**Validation**:
- [ ] All new Markdown Editor tests pass
- [ ] All existing Golf Ghost + Metronome tests still pass
- [ ] HTML report generated at `reports/report.html`
- [ ] `grep -r "time.sleep" tests/ pages/` returns nothing

---

### Step 4: Commit
```bash
git add pages/markdown_page.py tests/test_markdown_editor.py
git commit -m "feat: add Markdown Editor POM and test suite"
```

---

## Testing Requirements

### Test Scenarios
| Class | Test Method | Scenario |
|-------|-------------|----------|
| `TestMarkdownLoad` | `test_page_loads` | Page loads at jurigregg.com/md/ |
| `TestMarkdownLoad` | `test_page_title` | Title is "Markdown Editor - jurigregg.com" |
| `TestMarkdownLoad` | `test_editor_visible` | Textarea visible |
| `TestMarkdownLoad` | `test_preview_visible` | Preview pane visible |
| `TestMarkdownLoad` | `test_toolbar_visible` | Toolbar buttons present |
| `TestMarkdownLoad` | `test_word_count_initial` | "Words: 0 \| Characters: 0" |
| `TestMarkdownEditorPreview` | `test_heading_renders` | `# Hello` → `<h1>` in preview |
| `TestMarkdownEditorPreview` | `test_bold_renders` | `**bold**` → `<strong>` in preview |
| `TestMarkdownEditorPreview` | `test_preview_updates_in_realtime` | Preview updates without reload |
| `TestMarkdownWordCount` | `test_empty_editor_count` | Empty → 0 words, 0 chars |
| `TestMarkdownWordCount` | `test_count_after_typing` | "Hello World" → 2 words, 11 chars |
| `TestMarkdownToolbar` | `test_bold_button_wraps_text` | Select all + Bold btn → `**...**` |
| `TestMarkdownKeyboard` | `test_bold_shortcut` | Select all + Meta+B → `**...**` |
| `TestMarkdownCheatSheet` | `test_cheatsheet_toggle_opens` | Click → panel visible |
| `TestMarkdownCheatSheet` | `test_cheatsheet_toggle_closes` | Click twice → panel hidden |
| `TestMarkdownTheme` | `test_theme_toggle_changes_class` | Toggle → body class changes |
| `TestMarkdownTheme` | `test_theme_persists_after_reload` | Toggle + reload → persists |
| `TestMarkdownPersistence` | `test_autosave_status_updates` | Type → status changes |
| `TestMarkdownPersistence` | `test_draft_persists_after_reload` | Type + wait + reload → text present |
| `TestMarkdownClearDraft` | `test_clear_draft_empties_editor` | Clear → editor empty |
| `TestMarkdownResponsive` | `test_mobile_page_renders` | Loads at 390x844 |
| `TestMarkdownResponsive` | `test_mobile_editor_visible` | Editor + toolbar visible |

### Waiting Patterns Required
- `wait_for_load_state("networkidle")` after navigation and reload
- `expect(autosave_status).to_contain_text("Saved", timeout=5000)` after typing — auto-save is debounced ~1 second
- No wait needed for preview sync — updates on `input` event synchronously after `fill()`
- Fresh browser context per test (conftest.py) means localStorage is clean — no explicit clear needed

---

## Integration Test Plan

After `pytest` passes:

| Step | Action | Expected Result | Pass? |
|------|--------|-----------------|-------|
| 1 | `pytest tests/test_markdown_editor.py --browser chromium -v` | All 22 tests green | ☐ |
| 2 | `pytest tests/ --browser chromium -v` | All tests green (Golf Ghost + Metronome + Markdown) | ☐ |
| 3 | `pytest tests/test_markdown_editor.py --headed --slowmo 500` | Watch tests run visually | ☐ |
| 4 | Open `reports/report.html` | Report shows all passing | ☐ |

---

## Error Handling

### Known Flakiness Risks
| Risk | Cause | Mitigation |
|------|-------|------------|
| Auto-save timing | Debounced ~1 second after typing stops | Use `expect().to_contain_text("Saved", timeout=5000)` |
| Toolbar Bold selector | No aria-labels on toolbar buttons | Use `button.toolbar-btn:has-text("B")` — confirm on live DOM |
| URL redirect without trailing slash | `jurigregg.com/md` redirects to `jurigregg.com/md/` | Always use trailing slash in `navigate("/md/")` |
| Existing draft in localStorage | Previous session may have saved state | Each test gets fresh browser context — localStorage is clean |
| Select All + Bold timing | Need text selected before bold applies | Use `locator.press("Meta+A")` then bold — Playwright serializes actions |

### Edge Cases
- **Toolbar button "B" vs "Blockquote"**: The Bold button text is "B" while other buttons may contain "B" (like "Blockquote"). The `:has-text("B")` selector matches exact substring — executor must confirm the most precise selector on the live DOM.
- **Meta+B vs Ctrl+B**: On macOS, Playwright uses `Meta+B` for Cmd+B. The tests should use `Meta+B` since the project runs on macOS.

---

## Rollback Plan

Tests are purely additive — they do not modify the target app.

1. Delete `pages/markdown_page.py`
2. Delete `tests/test_markdown_editor.py`
3. Run `pytest tests/` to confirm Golf Ghost + Metronome suites still pass

---

## Confidence Scores

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| Clarity | **9** | Init spec is detailed with 11 scenarios and confirmed DOM selectors |
| Feasibility | **8** | Most locators are stable CSS IDs. Toolbar Bold button selector needs live confirmation. Auto-save debounce timing needs `expect()` with timeout. |
| Completeness | **9** | 22 tests across 10 classes covering all init scenarios |
| Alignment | **10** | Follows POM pattern, sync API, no `time.sleep()`, locator conventions |
| **Average** | **9.0** | High confidence. Minor risk on toolbar button selector precision. |

---

## Notes

- **Trailing slash is critical**: `https://jurigregg.com/md/` not `https://jurigregg.com/md` — the redirect adds latency and may break `networkidle`.
- **Toolbar buttons lack aria-labels**: This is the only app where we rely on CSS + text matching for interactive elements. If the Bold button selector proves flaky, fall back to `page.locator(".toolbar-btn").first` or inspect `title` attributes.
- **Auto-save debounce**: The save happens ~1 second after typing stops. Use `expect()` to wait for the status text to change rather than any fixed delay.
- **Each test gets fresh context**: conftest.py creates a new browser context per test, so localStorage is always clean. No need to explicitly clear storage.
- **This completes Phase 2**: After PRP-003, all three target apps have test coverage and the project moves to Phase 3 (multi-browser + robustness).

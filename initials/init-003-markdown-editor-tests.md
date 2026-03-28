# init-003: Markdown Editor Test Suite

## App Under Test

**Name**: Markdown Editor
**URL**: https://jurigregg.com/md/ (trailing slash required — without it redirects)
**Stack**: Pure HTML/CSS/JS on S3 + CloudFront
**Repo**: github.com/greggjuri/markdown-editor

## What the App Does

A feature-rich browser-based markdown editor with live preview. User types markdown in
a textarea on the left, rendered HTML preview updates in real time on the right. Includes
a formatting toolbar, keyboard shortcuts, dark/light theme toggle, auto-save to
localStorage, word/character count, cheat sheet panel, and export options (.md download,
copy HTML, copy plain text).

## Why This App

- **Widest variety of interactions** — toolbar clicks, keyboard shortcuts, textarea input,
  toggle buttons, preview sync
- **localStorage state** — draft and theme both persist, teaches reload-based testing
- **Split-pane live preview** — typing in editor updates preview in real time
- **Pure static app** — no API calls, teaches testing JS-only apps

## Live DOM Inspection Results

Inspected live at https://jurigregg.com/md/ on 2026-03-27.

| Element | Selector | Notes |
|---------|----------|-------|
| Editor textarea | `#markdown-input` | TEXTAREA, accepts direct typing |
| Preview pane | `#preview-output` | DIV, updates on `input` event |
| Autosave status | `#autosave-status` | SPAN, text: "💾 Auto-save: Ready" |
| Word/char count | `.word-count` | SPAN, text: "Words: X \| Characters: X" |
| Theme toggle | `#theme-toggle` | Shows 🌙 in light mode, ☀️ in dark mode |
| Cheat sheet toggle | `#cheatsheet-toggle` | Button, title: "Toggle Cheat Sheet" |
| Cheat sheet panel | `#cheatsheet-panel` | DIV, class `cheatsheet-panel hidden` when closed |
| Clear draft | `#clear-draft` | Button, title: "Clear saved draft" |
| Generate TOC | `#generate-toc` | Button, title: "Generate Table of Contents" |
| Soft breaks toggle | `#soft-breaks-toggle` | Button, title: "Toggle Soft Line Breaks" |
| Download .md | `#download-md` | Button class `export-btn` |
| Copy HTML | `#copy-html` | Button class `export-btn` |
| Copy text | `#copy-text` | Button class `export-btn` |
| Toolbar buttons | `.toolbar-btn` | B, I, S, H1, H2, H3, etc. — no aria-labels |

**Theme implementation**:
- Dark mode: `body` gets class `dark-mode` → `body.dark-mode` CSS rules apply
- Light mode: `body` has no class
- localStorage key: `markdown-editor-theme` (values: `"dark"` / `"light"`)
- Draft localStorage key: `markdown-editor-draft`

## Test Scenarios

### 1. Page Load
- Page loads at https://jurigregg.com/md/
- Title is "Markdown Editor - jurigregg.com"
- `#markdown-input` textarea is visible
- `#preview-output` div is visible
- Toolbar is visible (at least one `.toolbar-btn` present)
- `#autosave-status` shows "Auto-save: Ready"
- `.word-count` shows "Words: 0 | Characters: 0" on fresh load

### 2. Editor → Preview Sync
- Type `# Hello World` into `#markdown-input`
- `#preview-output` contains `<h1>Hello World</h1>`
- Type `**bold text**` — preview contains `<strong>bold text</strong>`
- Preview updates without page reload (real-time sync)

### 3. Word and Character Count
- On empty editor: "Words: 0 | Characters: 0"
- After typing `Hello World`: "Words: 2 | Characters: 11"

### 4. Toolbar — Bold Button
- Type `Hello` into editor, select all (`Ctrl+A`)
- Click the **B** toolbar button
- Editor value wraps text in `**...**`
- Preview shows `<strong>Hello</strong>`

### 5. Keyboard Shortcut — Bold
- Type `Hello` into editor, select all
- Press `Ctrl+B` (Mac: `Meta+B`)
- Editor wraps text in `**...**`

### 6. Cheat Sheet Toggle
- `#cheatsheet-panel` has class `hidden` initially (or not — check on load)
- Click `#cheatsheet-toggle`
- `#cheatsheet-panel` class changes (hidden added/removed)
- Click again — toggles back

### 7. Theme Toggle
- Read initial theme from `body.className`
- Click `#theme-toggle`
- `body.className` changes between `dark-mode` and `""` (empty)
- `localStorage['markdown-editor-theme']` updates to match

### 8. Theme Persistence After Reload
- Toggle theme to dark
- `page.reload()`
- `body.className` still contains `dark-mode`
- `localStorage['markdown-editor-theme']` is still `"dark"`

### 9. Draft Auto-save and Persistence
- Type unique text into editor
- Wait for autosave (debounced — ~1 second after typing stops)
- `#autosave-status` shows "Saved" or similar
- `page.reload()`
- `#markdown-input` value contains the typed text (restored from localStorage)

### 10. Clear Draft
- Type text into editor
- Click `#clear-draft`
- `#markdown-input` value is empty (or cleared)
- `localStorage['markdown-editor-draft']` is null or empty

### 11. Responsive Check
- Page loads at 390x844 (iPhone 14)
- `#markdown-input` is visible
- Toolbar is visible

## POM Design

### File: `pages/markdown_page.py`

Class: `MarkdownPage(BasePage)`

```python
# Confirmed locators from live DOM inspection
EDITOR = '#markdown-input'
PREVIEW = '#preview-output'
AUTOSAVE_STATUS = '#autosave-status'
WORD_COUNT = '.word-count'
THEME_TOGGLE = '#theme-toggle'
CHEATSHEET_TOGGLE = '#cheatsheet-toggle'
CHEATSHEET_PANEL = '#cheatsheet-panel'
CLEAR_DRAFT = '#clear-draft'
GENERATE_TOC = '#generate-toc'
SOFT_BREAKS_TOGGLE = '#soft-breaks-toggle'
TOOLBAR_BOLD = 'button.toolbar-btn:has-text("B")'
TOOLBAR_ITALIC = 'button.toolbar-btn:has-text("I")'
TOOLBAR_H1 = 'button[title=""] :text("H1")'  # Claude Code to confirm exact selector
```

Key methods:
- `load()` — navigate to `https://jurigregg.com/md/` and wait for networkidle
- `type_markdown(text: str)` — fill `#markdown-input`
- `get_preview_html() -> str` — return `#preview-output` innerHTML
- `get_word_count() -> str` — return `.word-count` text
- `get_autosave_status() -> str` — return `#autosave-status` text
- `click_theme_toggle()` — click `#theme-toggle`
- `get_body_class() -> str` — return `document.body.className` via evaluate
- `get_stored_theme() -> str` — return `localStorage['markdown-editor-theme']` via evaluate
- `get_stored_draft() -> str` — return `localStorage['markdown-editor-draft']` via evaluate
- `click_cheatsheet_toggle()` — click `#cheatsheet-toggle`
- `is_cheatsheet_visible() -> bool` — check if `hidden` NOT in `#cheatsheet-panel` class
- `click_clear_draft()` — click `#clear-draft`
- `press_bold_shortcut()` — `page.keyboard.press("Meta+B")` (Mac) or `Ctrl+B`

## Test File

### File: `tests/test_markdown_editor.py`

Classes:
- `TestMarkdownLoad` — page load, elements visible, initial state
- `TestMarkdownEditorPreview` — typing syncs to preview in real time
- `TestMarkdownWordCount` — word/char count updates correctly
- `TestMarkdownToolbar` — Bold button wraps text correctly
- `TestMarkdownKeyboard` — Ctrl/Cmd+B keyboard shortcut
- `TestMarkdownCheatSheet` — toggle opens/closes panel
- `TestMarkdownTheme` — theme toggle and body class change
- `TestMarkdownPersistence` — theme and draft survive page reload
- `TestMarkdownClearDraft` — clear draft empties editor and localStorage
- `TestMarkdownResponsive` — mobile viewport rendering

## Technical Notes

- **URL must include trailing slash**: `https://jurigregg.com/md/` — without it the
  redirect may affect test timing.
- **Toolbar button locators**: Most toolbar buttons have no `aria-label` or `id`.
  Use `page.locator('button.toolbar-btn', has_text="B")` — Claude Code to confirm
  the most reliable selector on the live DOM.
- **Auto-save is debounced**: After typing, wait for `#autosave-status` to show
  "Saved" text before reloading for persistence tests. Use `expect()` with timeout.
- **Theme is `body.dark-mode` class**: Not a data attribute. Read via
  `page.evaluate("document.body.className")`.
- **Keyboard shortcuts**: On Mac, Playwright uses `Meta+B` for Cmd+B. Use
  `page.keyboard.press("Meta+B")` not `Ctrl+B` for Mac compatibility.
- **Preview sync is immediate**: The `input` event fires on every keystroke.
  No explicit wait needed after `page.fill()` — preview updates synchronously.
- **Existing draft in localStorage**: Tests that check word count or empty state
  should clear localStorage first or use a fresh browser context.

## Success Criteria

- [ ] `pages/markdown_page.py` created with POM class
- [ ] `tests/test_markdown_editor.py` created with all test classes
- [ ] `pytest tests/test_markdown_editor.py --browser chromium` passes with zero failures
- [ ] At minimum 15 passing tests
- [ ] Full suite still passing: `pytest tests/ --browser chromium`
- [ ] Committed with message: `feat: add Markdown Editor POM and test suite`

## Out of Scope for This Init

- Testing actual file download (`.md` file download — browser file system)
- Testing clipboard copy (HTML/text copy buttons — clipboard API)
- Testing all toolbar buttons (focus on Bold as representative example)
- Firefox and WebKit (Phase 3)

## Open Questions

- None — app is fully public and client-side only

## References

- `docs/DECISIONS.md` ADR-005 — why Markdown Editor was selected
- `docs/TESTING.md` — locator strategy, keyboard interaction patterns
- `CLAUDE.md` — POM class structure and conventions
- `pages/base_page.py` — BasePage to inherit from

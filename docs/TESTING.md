# playwright-suite - Testing Standards

## Testing Approach

This project IS the test suite — there are no unit tests of the framework itself.
All tests are E2E tests running against live AWS-hosted production web properties.

```
        /\
       /  \     E2E — Playwright against live apps (this entire project)
      /----\
     /      \   Visual — Screenshot diffing (future phase)
    /--------\
   /          \ Network — Interception/API response testing (Phase 3)
  --------------
```

## Running Tests

```bash
# All tests, Chromium only (standard run)
pytest tests/ --browser chromium --html=reports/report.html

# All tests, all browsers
pytest tests/ --browser chromium --browser firefox --browser webkit

# Specific app
pytest tests/test_blog.py -v
pytest tests/test_metronome.py -v
pytest tests/test_sports.py -v

# Headed mode (watch the browser — use for debugging)
pytest tests/ --headed --slowmo 500

# Single test
pytest tests/test_blog.py::TestBlogHomepage::test_homepage_loads -v

# Show print output during run
pytest tests/ -s -v
```

## Locator Strategy (Priority Order)

Always use the highest-priority locator that works. Never skip down without reason.

| Priority | Method | Example | Use When |
|----------|--------|---------|----------|
| 1 | `get_by_role()` | `page.get_by_role("button", name="Start")` | ARIA roles available |
| 2 | `get_by_text()` | `page.get_by_text("Latest Posts")` | Unique visible text |
| 3 | `get_by_label()` | `page.get_by_label("BPM")` | Form inputs with labels |
| 4 | `get_by_placeholder()` | `page.get_by_placeholder("Search...")` | Input placeholders |
| 5 | `locator("css")` | `page.locator("nav.main-navigation")` | No semantic option exists |
| ❌ | XPath | Never | Avoid entirely |

## Page Object Model Standards

### File naming
- Page classes: `pages/{app}_page.py` (snake_case)
- Test files: `tests/test_{app}.py`

### Class structure
```python
# pages/blog_page.py
from pages.base_page import BasePage

class BlogPage(BasePage):
    # ✅ Locators as class-level constants — never inline in methods
    NAV_MENU = "nav.main-navigation"
    LATEST_POST = "article.post:first-child"
    POST_TITLE = "h2.entry-title"

    def __init__(self, page):
        super().__init__(page)

    def load(self) -> None:
        """Navigate to app and wait for full load."""
        self.navigate()
        self.page.wait_for_load_state("networkidle")

    # ✅ Action methods return self for chaining where logical
    # ✅ Query methods return values
    def get_latest_post_title(self) -> str:
        return self.page.locator(self.LATEST_POST).locator(self.POST_TITLE).text_content()
```

### Test class structure
```python
# tests/test_blog.py
import pytest
from pages.blog_page import BlogPage

class TestBlogHomepage:
    """Tests for jurigregg.com homepage."""

    def test_page_title_contains_site_name(self, page):
        """Page title should identify the site."""
        blog = BlogPage(page)
        blog.load()
        assert "Juri" in blog.get_title(), \
            f"Expected 'Juri' in title, got: {blog.get_title()}"

    def test_navigation_is_visible(self, page):
        """Main navigation should be present and visible."""
        blog = BlogPage(page)
        blog.load()
        assert page.locator(BlogPage.NAV_MENU).is_visible(), \
            "Main navigation menu should be visible on page load"
```

## Assertion Standards

- **Always include a descriptive failure message** in every `assert`
- Use `expect()` (Playwright's built-in assertion) when it applies — it auto-retries
- Use Python `assert` for simple value checks after data extraction

```python
# ✅ Playwright expect — auto-retries, built-in timeout
from playwright.sync_api import expect
expect(page.locator("nav")).to_be_visible()
expect(page.locator("h1")).to_contain_text("Golf")

# ✅ Python assert with message
assert page.title() != "", "Page title should not be empty"
assert "jurigregg" in page.url, f"Expected jurigregg.com URL, got: {page.url}"

# ❌ Assert without message — useless failure output
assert page.title() != ""
```

## Waiting Standards

**Never use `time.sleep()`.** Playwright has built-in waiting for every scenario.

```python
# ✅ Wait for network to settle after navigation
page.goto("https://jurigregg.com")
page.wait_for_load_state("networkidle")

# ✅ Wait for a specific element
page.locator("article.post").wait_for()

# ✅ Custom timeout for slow external API content (Sports page)
expect(page.locator(".sport-highlight")).to_be_visible(timeout=15000)

# ❌ Never do this
import time
time.sleep(3)
```

## Screenshot Standards

Screenshots on failure are automatic via conftest.py. Do not add manual screenshot calls to tests.

- Stored in: `reports/screenshots/`
- Named: `{test_name}_{browser}_{timestamp}.png`
- Attached automatically to pytest-html report

## Browser Matrix

| Browser | When to Run | Notes |
|---------|-------------|-------|
| Chromium | Every run (default) | Primary browser, fastest |
| Firefox | Before commits | Catches Firefox-specific rendering |
| WebKit | Before commits | Safari proxy — catches Safari issues |

## Test Organization

Group tests by app, then by concern:

```
tests/
├── test_blog.py
│   ├── TestBlogHomepage      # Page load, title, meta tags
│   ├── TestBlogNavigation    # Menu items, links, routing
│   └── TestBlogContent       # Post loading, images, structure
├── test_metronome.py
│   ├── TestMetronomeLoad     # Page renders, controls visible
│   ├── TestMetronomeControls # BPM input, start/stop button
│   └── TestMetronomeAudio    # Web Audio API context (JS checks)
└── test_sports.py
    ├── TestSportsLoad        # Page renders, API content loads
    └── TestSportsContent     # Team highlights, schedule data
```

## Debugging Workflow

1. **Run headed with slowmo** to watch the failure live:
   ```bash
   pytest tests/test_blog.py::failing_test --headed --slowmo 1000 -v
   ```
2. **Check the screenshot** in `reports/screenshots/` for visual state at failure
3. **Add `page.pause()`** to freeze the browser at a specific point for inspection
4. **Check the HTML report** at `reports/report.html` for full context
5. **Add print statements** and run with `-s` to see output during execution

## Common Issues and Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Content not loaded yet | `locator not found` on JS-rendered content | Add `wait_for_load_state("networkidle")` after navigation |
| ESPN API slow to respond | Sports content assertions fail intermittently | Use `timeout=15000` on those specific assertions |
| Metronome audio context blocked | Web Audio API not initialized | Check for browser autoplay policy — may need a click first |
| Flaky on CI | Tests pass locally, fail in GitHub Actions | Add explicit waits, check for headless vs headed differences |

## Pre-Commit Checklist

- [ ] `pytest tests/ --browser chromium` passes with zero failures
- [ ] No `time.sleep()` introduced
- [ ] All new assertions have descriptive messages
- [ ] New locators are class-level constants in the POM, not inline strings
- [ ] `pip freeze > requirements.txt` if any packages were added

## Lessons Learned

| Bug | Root Cause | Prevention |
|-----|------------|------------|
| Golf Ghost: Next.js SSR doesn't expose full DOM in page source | Client-side hydration renders form/scorecard elements | Always use Playwright to inspect rendered DOM, not raw HTML fetches |
| Golf Ghost: Score colors use inline styles, not CSS classes | `style="color: rgb(34, 211, 238);"` not class names | Assert `td[style*='color']` presence, never specific color values |
| Golf Ghost: Scorecard table has 21 rows not 18 | OUT/IN/TOT summary rows included | Filter by `first_cell.isdigit()` to count only hole rows |
| Metronome: Start/Stop button aria-label swaps | Running state shows `aria-label="Stop metronome"`, stopped shows `aria-label="Start metronome"` | Use separate locators for each state; use `expect().to_be_visible()` after state transitions |
| Metronome: Theme test must be order-independent | Initial theme may be dark or light depending on prior localStorage | Read initial theme first, then assert it changed to the opposite after toggle |
| Markdown Editor: `page.fill()` does not trigger preview or word count | App listens on `input` event but `fill()` bypasses native DOM events; preview is debounced (150ms) | Use `fill()` + `page.evaluate("updatePreview()")` — `updatePreview()` also calls `updateWordCount()` |
| Markdown Editor: `Meta+B` (uppercase) fails for bold shortcut | JS checks `e.key === 'b'` (lowercase); Playwright `Meta+B` sends uppercase `B` | Use `Meta+b` (lowercase) in `locator.press()` for keyboard shortcuts |
| Markdown Editor: `:has-text("B")` matches multiple toolbar buttons | "Soft Breaks" button also contains "B" in its text | Use `[data-action="bold"]` attribute selector instead |

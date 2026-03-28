# CLAUDE.md - Claude Code Instructions

This file provides project-specific instructions and conventions for Claude Code.

## Project Overview

**playwright-suite**: End-to-end test automation framework for jurigregg.com AWS-hosted web properties using Python Playwright + pytest.

**Tech Stack**: Python 3.x | Playwright | pytest | pytest-html | Page Object Model

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Run all tests (Chromium)
pytest tests/ --browser chromium --html=reports/report.html

# Run all tests (all browsers)
pytest tests/ --browser chromium --browser firefox --browser webkit

# Run tests for a specific app
pytest tests/test_blog.py -v
pytest tests/test_metronome.py -v
pytest tests/test_sports.py -v

# Run with headed browser (visible - useful for debugging)
pytest tests/ --headed --slowmo 500

# Run single test
pytest tests/test_blog.py::test_homepage_loads -v
```

## File Structure

```
playwright-suite/
├── CLAUDE.md                    # This file
├── PROJECT-INSTRUCTIONS.md      # Claude.ai project system prompt
├── README.md                    # Project overview
├── conftest.py                  # pytest fixtures and browser setup
├── requirements.txt             # Python dependencies
├── pytest.ini                   # pytest configuration
├── docs/
│   ├── PLANNING.md              # Architecture overview and test strategy
│   ├── TASK.md                  # Current tasks and sprint tracking
│   ├── DECISIONS.md             # ADRs
│   └── TESTING.md               # Testing standards and conventions
├── initials/                    # Feature specifications
├── prps/                        # Implementation plans
│   └── templates/
│       └── prp-template.md
├── .claude/
│   └── commands/
│       ├── generate-prp.md
│       └── execute-prp.md
├── pages/                       # Page Object Model classes
│   ├── base_page.py             # Shared base class
│   ├── blog_page.py             # jurigregg.com
│   ├── metronome_page.py        # metronome.jurigregg.com
│   └── sports_page.py           # jurigregg.com/sports
├── tests/                       # Test suites
│   ├── test_blog.py
│   ├── test_metronome.py
│   └── test_sports.py
└── reports/                     # Generated HTML test reports
```

## Critical Rules

### 1. File Size Limit
- **Maximum 500 lines per file**
- When approaching limit: split into modules
- Prefer many small files over few large files

### 2. Commit Strategy
- **Commit after every feature** - atomic, working commits
- Use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`
- Each commit should leave the test suite in a passing state

### 3. Testing Requirements
- All tests must pass before committing
- Use `assert` with descriptive messages
- Screenshot on failure is mandatory (configured in conftest.py)
- No `time.sleep()` — use Playwright's built-in auto-waiting

### 4. Documentation
- Update `docs/TASK.md` when starting/completing tasks
- Create ADR in `docs/DECISIONS.md` for architectural choices
- Add learnings to `docs/TESTING.md` when debugging flaky tests

## Coding Conventions

### Page Object Model Pattern

```python
# pages/base_page.py - All POMs inherit from this
class BasePage:
    def __init__(self, page):
        self.page = page
        self.base_url = "https://jurigregg.com"

    def navigate(self, path: str = "") -> None:
        """Navigate to a path relative to base_url."""
        self.page.goto(f"{self.base_url}{path}")

    def get_title(self) -> str:
        return self.page.title()
```

```python
# pages/blog_page.py - Example POM class
from pages.base_page import BasePage

class BlogPage(BasePage):
    # Locators as class attributes
    NAV_MENU = "nav.main-navigation"
    LATEST_POST = "article.post:first-child"
    
    def __init__(self, page):
        super().__init__(page)

    def load(self) -> None:
        self.navigate()
        self.page.wait_for_load_state("networkidle")

    def get_latest_post_title(self) -> str:
        return self.page.locator(self.LATEST_POST).text_content()
```

```python
# tests/test_blog.py - Test file pattern
import pytest
from pages.blog_page import BlogPage

class TestBlogHomepage:
    def test_homepage_loads(self, page):
        blog = BlogPage(page)
        blog.load()
        assert "Juri" in blog.get_title(), "Page title should contain 'Juri'"

    def test_navigation_visible(self, page):
        blog = BlogPage(page)
        blog.load()
        assert page.locator(BlogPage.NAV_MENU).is_visible()
```

### conftest.py Pattern

```python
# conftest.py
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 720}
    )
    page = context.new_page()
    yield page
    # Screenshot on failure handled by pytest-playwright
    context.close()
```

### Locator Strategy (in priority order)

1. `page.get_by_role()` — ARIA roles, most resilient
2. `page.get_by_text()` — visible text
3. `page.get_by_label()` — form labels
4. `page.locator("css-selector")` — CSS, last resort
5. **Never use XPath unless absolutely necessary**

## Error Handling Patterns

- Always use `expect()` for assertions where possible (auto-retry built in)
- Use `page.wait_for_load_state("networkidle")` after navigation
- Wrap flaky network-dependent assertions in `expect(locator).to_be_visible(timeout=10000)`
- Log failures with context: URL, browser, viewport

## PRP Workflow

### Generating PRPs
```bash
/generate-prp initials/init-{feature}.md
```

This command:
1. Reads `docs/PLANNING.md`, `docs/DECISIONS.md`, `docs/TESTING.md`
2. Reads the init specification
3. Researches existing pages/ and tests/ for patterns
4. Generates comprehensive PRP with implementation steps
5. Scores confidence and lists concerns

### Executing PRPs
```bash
/execute-prp prps/prp-{feature}.md
```

This command:
1. Reads the PRP
2. Implements each step sequentially
3. Runs `pytest` after each step
4. Reports progress and handles errors

## DO NOT

- Use `time.sleep()` — use Playwright auto-waiting
- Hardcode URLs in test files — use BasePage or conftest fixtures
- Write tests without descriptive assert messages
- Commit with failing tests
- Commit secrets or API keys
- Create files over 500 lines
- Contradict existing ADRs without discussion

## Reference Documents

- `docs/PLANNING.md` - Architecture, test targets, phases
- `docs/DECISIONS.md` - Past decisions to respect
- `docs/TASK.md` - Current work status
- `docs/TESTING.md` - Testing standards and locator conventions

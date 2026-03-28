# playwright-suite - Architecture Decisions

## ADR-001: Python Playwright over Selenium or Cypress

**Date**: 2026-03-27
**Status**: Accepted

### Context
Need to choose a browser automation/E2E testing tool. Three realistic options exist: Selenium (the long-standing standard), Cypress (popular modern alternative), and Playwright (Microsoft, 2020).

### Decision
Use **Python Playwright** with **pytest-playwright**.

### Rationale
- Python is the primary language already in use across all projects
- Playwright has built-in auto-waiting, eliminating the `time.sleep()` anti-pattern that plagued Selenium
- Playwright bundles its own browsers — no external driver management (ChromeDriver, GeckoDriver, etc.)
- Playwright supports Chromium, Firefox, and WebKit from a single API
- pytest-playwright integrates cleanly with the existing pytest knowledge base
- Playwright is rapidly replacing Selenium on job postings for QA/SDET roles

### Alternatives Considered
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Selenium | Industry legacy, huge community | Slow, flaky, requires driver management, Python but dated patterns | Rejected |
| Cypress | Fast, great DX, popular | JavaScript only — doesn't fit Python-first approach | Rejected |
| Playwright | Fast, auto-wait, multi-browser, Python native | Newer, smaller community than Selenium | **Selected** |

### Consequences

**Positive:**
- Modern, fast test execution
- No driver management overhead
- Multi-browser from day one
- Directly marketable skill on resume

**Negative:**
- Smaller community than Selenium (fewer Stack Overflow answers)
- Some learning curve on async vs sync API (we use sync)

---

## ADR-002: Sync API over Async Playwright

**Date**: 2026-03-27
**Status**: Accepted

### Context
Playwright offers both a synchronous (`sync_api`) and asynchronous (`async_api`) Python API. Must choose one as the standard for the project.

### Decision
Use the **synchronous API** (`from playwright.sync_api import sync_playwright`).

### Rationale
- pytest is synchronous by default — sync Playwright integrates with zero friction
- Async Playwright requires `pytest-asyncio` and `async def` test functions, adding complexity
- No performance benefit for E2E testing against live web apps (network I/O dominates, not Python threading)
- Simpler code is easier to maintain and explain in interviews

### Consequences

**Positive:**
- Clean, readable test code
- Standard pytest patterns work without modification

**Negative:**
- Cannot easily run tests in parallel within a single process (use pytest-xdist if needed later)

---

## ADR-003: Page Object Model (POM) Pattern

**Date**: 2026-03-27
**Status**: Accepted

### Context
Test code can be written as flat scripts or organized with an abstraction pattern. POM is the industry-standard pattern for maintainable E2E test suites.

### Decision
Use the **Page Object Model** with a `BasePage` class that all app-specific page classes inherit from.

### Rationale
- POM separates test logic (what to assert) from page interaction logic (how to find elements)
- When the UI changes, only the POM class needs updating — not every test that touches that page
- Industry-standard pattern — explicitly named in most QA/SDET job postings
- Locators defined as class attributes in one place, not scattered across test files

### Consequences

**Positive:**
- Maintainable as the target apps evolve
- Resume-worthy architecture pattern
- Easier to onboard someone else to the project

**Negative:**
- More upfront structure than flat scripts
- Small overhead for a single-developer project (worth it for the learning)

---

## ADR-004: Fully Pinned Dependencies (Security Standard)

**Date**: 2026-03-27
**Status**: Accepted

### Context
On March 24, 2026, the LiteLLM supply chain attack compromised environments using unpinned dependencies. Projects with strict lockfiles were immune.

### Decision
All Python dependencies pinned to exact versions via `pip freeze > requirements.txt`. GitHub Actions (when added) pinned to immutable commit hashes, not tags.

### Rationale
- Mutable version ranges (`>=`, `~=`, `latest`) allow compromised packages to be pulled automatically
- `pip freeze` captures every transitive dependency at the exact version in the working environment
- GitHub Actions tags are mutable — the Trivy attack rewrote tags to point to malware; commit hashes are immutable

### Consequences

**Positive:**
- Reproducible environments across machines and CI
- Immune to the class of supply chain attack seen in March 2026

**Negative:**
- Manual effort required to upgrade dependencies (intentional — forces conscious review)

### References
- `dependency-pinning-guide.md` — full security standard document

---

---

## ADR-005: Test Target Selection — Golf Ghost, Metronome, Markdown Editor

**Date**: 2026-03-27
**Status**: Accepted

### Context
Six apps plus games are hosted on jurigregg.com AWS properties. Need to select 3-4 that provide
the best coverage of Playwright skills and are actually testable via DOM automation.

### Decision
Target **Golf Ghost**, **Metronome**, and **Markdown Editor** for Phase 1-3. Defer others.

### Rationale
- **Golf Ghost** (ghost.jurigregg.com): Next.js app with a form, async API call to Lambda, and
  a rendered scorecard with color-coded cells — covers form filling, async waiting, and visual
  assertions in one app. Highest teaching value.
- **Metronome** (metronome.jurigregg.com): Pure JS single page with UI controls — teaches testing
  JS-rendered apps with no traditional navigation or routing.
- **Markdown Editor** (jurigregg.com/md): Toolbar buttons, keyboard shortcuts, split-pane live
  preview sync, dark/light toggle, localStorage persistence — covers the widest variety of
  Playwright interaction techniques.

### Alternatives Considered
| App | Verdict | Reason |
|-----|---------|--------|
| Pulsar | Rejected | Three.js canvas — DOM largely inaccessible to Playwright |
| Automation Platform | Deferred | Public read-only list is low interactivity; good future candidate |
| Sports Schedules | Deferred | Good future candidate for network interception; deprioritized for Phase 1 |
| Games | Deferred | Need to review repos; likely canvas-based like Pulsar |

### Consequences

**Positive:**
- Three apps cover a wide range of Playwright techniques
- All three are publicly accessible without authentication
- Golf Ghost API calls provide natural network interception opportunities in Phase 3

**Negative:**
- Pulsar (most visually impressive app) is not testable
- Sports Schedules ESPN API interception deferred to future phase

---

## ADR-006: Browser Specified on CLI, Not in pytest.ini

**Date**: 2026-03-28
**Status**: Accepted

### Context
Initially `pytest.ini` included `addopts = --browser chromium -v` so that `pytest tests/` would default to Chromium. However, when running multi-browser tests via `pytest tests/ --browser chromium --browser firefox --browser webkit`, the `--browser chromium` in addopts stacked with the CLI flag, causing every test to run twice on Chromium.

### Decision
Remove `--browser chromium` from `pytest.ini` addopts. Browsers are now specified explicitly on the command line.

### Rationale
- Eliminates accidental double-runs when Chromium is specified both in addopts and on CLI
- Makes the browser matrix explicit and visible in the command
- Keeps `pytest.ini` focused on non-browser config (`-v`, markers)

### Consequences

**Positive:**
- Clean test counts: `--browser chromium` = 55, all three browsers = 165
- No hidden defaults that conflict with explicit CLI flags

**Negative:**
- Running `pytest tests/` without `--browser` will fail (no browser specified) — this is intentional, forcing explicit browser selection

---

## ADR-007: Multi-Browser Validation — All Tests Pass Across Chromium, Firefox, and WebKit

**Date**: 2026-03-28
**Status**: Accepted

### Context
Phase 3 required validating the full 55-test suite across Chromium, Firefox, and WebKit to confirm cross-browser compatibility.

### Decision
All 55 tests pass across all three browsers with zero failures and zero flaky tests. The test suite is cross-browser clean as of Phase 3 completion.

### Rationale
- 165 total test executions (55 x 3 browsers), 0 failures
- No browser-specific locator workarounds needed
- `Meta+b` keyboard shortcut works identically across all three engines
- `page.evaluate()` for localStorage and DOM reads works identically across all three engines
- Responsive viewport tests (390x844) pass in all browsers

### Consequences

**Positive:**
- Confidence that all three target apps render and behave consistently across browser engines
- Test suite can be used for ongoing cross-browser regression detection

**Negative:**
- Network interception tests (Golf Ghost Lambda API) deferred to future phase — not required for Phase 3 completion

---

## Template for New Decisions

```markdown
## ADR-XXX: Title

**Date**: YYYY-MM-DD
**Status**: Proposed/Accepted/Deprecated/Superseded

### Context
What is the issue motivating this decision?

### Decision
What are we doing?

### Rationale
- Reason 1
- Reason 2

### Alternatives Considered (optional)
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|

### Consequences

**Positive:**
- Benefit 1

**Negative:**
- Tradeoff 1

### References (optional)
- PRP: `prps/prp-xxx.md`
- Init: `initials/init-xxx.md`
```

## Key Principles

1. **Sync over async**: Keep test code simple — sync Playwright + standard pytest
2. **POM everywhere**: No raw locators in test files — always go through a page class
3. **Auto-wait only**: Never use `time.sleep()` — Playwright's waiting mechanisms always
4. **Pin everything**: Exact versions in requirements.txt, commit hashes in GitHub Actions

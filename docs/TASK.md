# playwright-suite - Task Tracker

## Current Sprint: Complete

### All Phases Done
Project has reached its planned scope. See Future section for potential next steps.

---

## Recently Completed

- [x] Project scaffold and repo setup on MacBook
- [x] `conftest.py` — browser fixtures, screenshot-on-failure
- [x] `pytest.ini` — configuration, markers, default Chromium
- [x] `pages/base_page.py` — BasePage POM class with shared navigation
- [x] `init-001-golf-ghost-tests.md` — Golf Ghost POM + 14 passing tests (load, generation, scorecard, responsive)
- [x] `init-002-metronome-tests.md` — Metronome POM + 19 passing tests (load, BPM, controls, theme, responsive)
- [x] `init-003-markdown-editor-tests.md` — Markdown Editor POM + 22 passing tests (load, preview, word count, toolbar, keyboard, cheatsheet, theme, persistence, responsive)
- [x] Phase 3: Multi-browser validation — 55 tests passing across Chromium, Firefox, and WebKit (165 total)
- [x] Removed `--browser chromium` from `pytest.ini` addopts — browsers now specified explicitly on CLI
- [x] Phase 4: GitHub Actions CI — workflow on push/weekly/manual, pinned action hashes, HTML report artifact, README badge

---

## Backlog

### Phase 1 — Foundation
- [x] `conftest.py` — browser fixtures, screenshot-on-failure, base setup
- [x] `pytest.ini` — configuration, markers, default browser option
- [x] `requirements.txt` — fully pinned via `pip freeze`
- [x] `pages/base_page.py` — BasePage POM class with shared navigation
- [x] `init-001-golf-ghost-tests.md` — Golf Ghost test suite (first real tests)

### Phase 2 — Full App Coverage
- [x] `init-002-metronome-tests.md` — Metronome test suite
- [x] `init-003-markdown-editor-tests.md` — Markdown Editor test suite
- [x] Screenshot-on-failure wired into conftest.py
- [x] pytest-html report confirmed working

### Phase 3 — Multi-Browser + Robustness
- [x] Firefox and WebKit test matrix — all 55 tests pass across all 3 browsers
- [x] Responsive/viewport tests — included in each app's test suite (iPhone 14 390x844)
- [x] Flakiness audit — zero flaky tests across full 3-browser run
- [ ] Network interception tests for Golf Ghost Lambda API calls (deferred to future)

### Phase 4 — CI/CD Integration
- [x] GitHub Actions workflow file (`.github/workflows/playwright.yml`)
- [x] Actions pinned to commit hashes (checkout v4, setup-python v5, upload-artifact v4)
- [x] Weekly scheduled runs (Monday 06:00 UTC) + push to main + manual dispatch
- [x] README badge showing test status

### Future
- [ ] Automation Platform tests (workflow list, public read-only state)
- [ ] Sports Schedules network interception tests
- [ ] Playwright scraping module (feeds into fantasy football app project)

---

## Completed

- [x] Phase 1 foundation: conftest.py, pytest.ini, base_page.py, pages/__init__.py, tests/__init__.py
- [x] PRP-001: Golf Ghost test suite — `pages/golf_ghost_page.py` + `tests/test_golf_ghost.py` (14 tests)
- [x] PRP-002: Metronome test suite — `pages/metronome_page.py` + `tests/test_metronome.py` (19 tests)
- [x] PRP-003: Markdown Editor test suite — `pages/markdown_page.py` + `tests/test_markdown_editor.py` (22 tests)
- [x] Phase 3: Multi-browser (Chromium + Firefox + WebKit) — 55 tests x 3 browsers, 0 failures
- [x] Phase 4: GitHub Actions CI — push/schedule/manual triggers, pinned hashes, artifact upload, README badge

---

## Notes

### Environment
- **MacBook** — primary development machine
- **Python**: confirm with `python3 --version`
- **Claude Code**: `npm install -g @anthropic-ai/claude-code`
- **Browsers installed via**: `playwright install`

### Security Standard
- All packages pinned exactly: `pip freeze > requirements.txt`
- GitHub Actions will use commit hashes, not tags
- No `curl | bash` installs
- See `dependency-pinning-guide.md` (post-LiteLLM March 2026 incident)

### Known Issues
- None yet

---

*Last updated: 2026-03-28 (Phase 4 complete — all planned phases done)*

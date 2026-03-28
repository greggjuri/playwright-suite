# playwright-suite - Task Tracker

## Current Sprint: Phase 1 — Foundation

### In Progress
*Nothing currently in progress.*

### Up Next
- [ ] `init-002-metronome-tests.md` — UI controls and JS rendering tests
- [ ] `init-003-markdown-editor-tests.md` — Toolbar, keyboard shortcuts, live preview tests

---

## Recently Completed

- [x] Project scaffold and repo setup on MacBook
- [x] `conftest.py` — browser fixtures, screenshot-on-failure
- [x] `pytest.ini` — configuration, markers, default Chromium
- [x] `pages/base_page.py` — BasePage POM class with shared navigation
- [x] `init-001-golf-ghost-tests.md` — Golf Ghost POM + 14 passing tests (load, generation, scorecard, responsive)

---

## Backlog

### Phase 1 — Foundation
- [ ] `conftest.py` — browser fixtures, screenshot-on-failure, base setup
- [ ] `pytest.ini` — configuration, markers, default browser option
- [ ] `requirements.txt` — fully pinned via `pip freeze`
- [ ] `pages/base_page.py` — BasePage POM class with shared navigation
- [ ] `init-001-golf-ghost-tests.md` — Golf Ghost test suite (first real tests)

### Phase 2 — Full App Coverage
- [ ] `init-002-metronome-tests.md` — Metronome test suite
- [ ] `init-003-markdown-editor-tests.md` — Markdown Editor test suite
- [ ] Screenshot-on-failure wired into conftest.py
- [ ] pytest-html report confirmed working

### Phase 3 — Multi-Browser + Robustness
- [ ] Firefox and WebKit test matrix
- [ ] Network interception tests for Golf Ghost Lambda API calls
- [ ] Responsive/viewport tests (Markdown Editor mobile layout)
- [ ] Flakiness audit and fixes

### Phase 4 — CI/CD Integration
- [ ] GitHub Actions workflow file
- [ ] Actions pinned to commit hashes (not tags — security standard)
- [ ] Scheduled nightly runs against production
- [ ] README badge showing test status

### Future
- [ ] Automation Platform tests (workflow list, public read-only state)
- [ ] Sports Schedules network interception tests
- [ ] Playwright scraping module (feeds into fantasy football app project)

---

## Completed

- [x] Phase 1 foundation: conftest.py, pytest.ini, base_page.py, pages/__init__.py, tests/__init__.py
- [x] PRP-001: Golf Ghost test suite — `pages/golf_ghost_page.py` + `tests/test_golf_ghost.py` (14 tests)

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

*Last updated: 2026-03-27 (project kickoff)*

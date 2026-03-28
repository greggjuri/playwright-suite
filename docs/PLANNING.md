# playwright-suite - Project Planning

## Project Vision

A professional end-to-end test automation framework targeting jurigregg.com AWS-hosted web properties.
Built with Python Playwright + pytest using the Page Object Model pattern to demonstrate real-world
test automation skills applicable to QA engineering, SDET, and Senior Systems Engineer roles.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TEST SUITES                                   │
│              tests/test_golf_ghost.py                                │
│              tests/test_markdown_editor.py                           │
│              tests/test_metronome.py                                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PAGE OBJECT MODEL                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐        │
│  │ golf_ghost_page  │  │ metronome_page   │  │ markdown_page   │        │
│  └──────────┬───────┘  └────────┬─────────┘  └────────┬────────┘        │
│         └─────────────────►│◄───────────────────┘                  │
│                       base_page.py                                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PYTEST + PLAYWRIGHT                               │
│              conftest.py (fixtures, browser setup)                  │
│              pytest.ini (config, markers, options)                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Chromium     │  │    Firefox      │  │    WebKit       │
│  (primary)      │  │  (secondary)    │  │  (Safari proxy) │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TEST TARGETS (Live AWS)                        │
│  ghost.jurigregg.com  │  metronome.jurigregg.com  │  jurigregg.com/md│
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    REPORTS + ARTIFACTS                               │
│              reports/report.html (pytest-html)                      │
│              reports/screenshots/ (on failure)                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Test Targets

| App | Base URL | Stack | Key Test Areas |
|-----|----------|-------|----------------|
| Golf Ghost | ghost.jurigregg.com | Next.js 14 + AWS Lambda + DynamoDB | Form input, handicap calculation, scorecard rendering, color-coded results, API response |
| Metronome | metronome.jurigregg.com | Single HTML/JS on S3+CloudFront | UI controls, BPM input, start/stop, JS rendering |
| Markdown Editor | jurigregg.com/md | Pure HTML/JS on S3+CloudFront | Toolbar buttons, keyboard shortcuts, live preview sync, dark/light toggle, localStorage |

## Apps Evaluated But Not Selected

| App | Reason Not Selected |
|-----|---------------------|
| Pulsar (pulsar.jurigregg.com) | Three.js canvas — DOM largely inaccessible to Playwright |
| Automation Platform (automations.jurigregg.com) | Public read-only list is low interactivity; good future candidate |
| Sports Schedules (jurigregg.com/sports) | Good future candidate for network interception tests |

## Tech Stack

- **Language**: Python 3.x
- **Test Framework**: pytest + pytest-playwright
- **Browser Automation**: Microsoft Playwright
- **Reporting**: pytest-html
- **Pattern**: Page Object Model (POM)
- **Browsers**: Chromium (primary), Firefox, WebKit
- **Dependency Management**: pip with fully pinned requirements.txt (pip freeze)
- **CI/CD**: GitHub Actions (future phase) — actions pinned to commit hashes

## Project Structure

```
playwright-suite/
├── CLAUDE.md                    # Claude Code conventions
├── PROJECT-INSTRUCTIONS.md      # Claude.ai project system prompt
├── README.md                    # Project overview
├── conftest.py                  # pytest fixtures and browser setup
├── requirements.txt             # Fully pinned Python dependencies
├── pytest.ini                   # pytest configuration and markers
├── docs/
│   ├── PLANNING.md              # This file
│   ├── TASK.md                  # Sprint/task tracking
│   ├── DECISIONS.md             # Architecture Decision Records
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
│   ├── golf_ghost_page.py       # ghost.jurigregg.com
│   ├── metronome_page.py        # metronome.jurigregg.com
│   └── markdown_page.py         # jurigregg.com/md
├── tests/                       # Test suites
│   ├── test_golf_ghost.py
│   ├── test_metronome.py
│   └── test_markdown_editor.py
└── reports/                     # Generated HTML test reports + screenshots
```

## Development Phases

### Phase 1: Foundation (Current)
- [ ] Project structure and repo setup on MacBook
- [ ] conftest.py with browser fixtures
- [ ] pytest.ini configuration
- [ ] requirements.txt (fully pinned via pip freeze)
- [ ] base_page.py POM base class
- [ ] init-001: Golf Ghost test suite (form, API, scorecard)

### Phase 2: Full App Coverage
- [ ] init-002: Metronome test suite (UI controls, JS rendering)
- [ ] init-003: Markdown Editor test suite (toolbar, shortcuts, preview sync)
- [ ] Screenshot-on-failure confirmed working
- [ ] pytest-html report generation confirmed

### Phase 3: Multi-Browser + Robustness
- [ ] Firefox and WebKit test matrix
- [ ] Network interception tests (Golf Ghost Lambda API calls)
- [ ] Responsive/viewport tests (Markdown Editor mobile layout)
- [ ] Flakiness audit and fixes

### Phase 4: CI/CD Integration
- [ ] GitHub Actions workflow
- [ ] Actions pinned to commit hashes (security standard — never tags)
- [ ] Scheduled nightly runs against production
- [ ] README badge showing test status

### Future Phases
- Automation Platform tests (workflow list, public read-only state)
- Sports Schedules network interception tests
- Visual regression testing (screenshot diffing)
- Playwright scraping module (feeds into fantasy football app)

## Key Constraints

1. **No `time.sleep()`** — Playwright auto-waiting only, always
2. **500-line file limit** — Split into modules when approaching
3. **Commit after each feature** — Atomic, passing commits only
4. **Pinned dependencies** — `pip freeze > requirements.txt`, no unpinned packages
5. **Tests run against live production** — No mocking of the target apps

## Success Criteria

1. [ ] All three apps have passing test suites in Chromium
2. [ ] Tests run cleanly across Chromium, Firefox, and WebKit
3. [ ] HTML report generated with screenshots on failure
4. [ ] GitHub repo is public and linkable on a resume
5. [ ] GitHub Actions runs the suite on every push (Phase 4)

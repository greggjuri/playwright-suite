# playwright-suite

End-to-end test automation framework for [jurigregg.com](https://jurigregg.com) AWS-hosted web properties. Built with Python Playwright + pytest using the Page Object Model pattern.

## Test Targets

| App | URL |
|-----|-----|
| Golf Blog | jurigregg.com |
| Metronome | metronome.jurigregg.com |
| Sports Schedule | jurigregg.com/sports |

## Tech Stack

- **Python 3.x** + **Playwright** + **pytest**
- **Page Object Model** architecture
- **pytest-html** reporting
- Multi-browser: Chromium, Firefox, WebKit

## Project Structure

```
playwright-suite/
├── CLAUDE.md                    # Claude Code conventions
├── PROJECT-INSTRUCTIONS.md      # Claude.ai project system prompt
├── README.md                    # This file
├── conftest.py                  # pytest fixtures and browser setup
├── requirements.txt             # Python dependencies
├── pytest.ini                   # pytest configuration
├── docs/
│   ├── PLANNING.md              # Architecture and test strategy
│   ├── TASK.md                  # Sprint/task tracking
│   ├── DECISIONS.md             # Architecture Decision Records
│   └── TESTING.md               # Testing standards and conventions
├── initials/                    # Feature specifications (CE workflow)
├── prps/                        # Implementation plans (CE workflow)
│   └── templates/
├── .claude/
│   └── commands/
│       ├── generate-prp.md
│       └── execute-prp.md
├── pages/                       # Page Object Model classes
│   ├── base_page.py
│   ├── blog_page.py
│   ├── metronome_page.py
│   └── sports_page.py
├── tests/                       # Test suites
│   ├── test_blog.py
│   ├── test_metronome.py
│   └── test_sports.py
└── reports/                     # Generated HTML test reports
```

## Setup

```bash
# Clone the repo
git clone https://github.com/greggjuri/playwright-suite.git
cd playwright-suite

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
playwright install
```

## Running Tests

```bash
# Run all tests (Chromium)
pytest tests/ --browser chromium --html=reports/report.html

# Run all tests across all browsers
pytest tests/ --browser chromium --browser firefox --browser webkit

# Run a specific app's tests
pytest tests/test_blog.py -v
pytest tests/test_metronome.py -v
pytest tests/test_sports.py -v

# Run with visible browser (debugging)
pytest tests/ --headed --slowmo 500

# Run a single test
pytest tests/test_blog.py::test_homepage_loads -v
```

## Development Workflow (Context Engineering)

This project uses the Claude.ai + Claude Code CE workflow:

```
Claude.ai                          Claude Code
─────────                          ───────────
Create initials/init-{feature}.md
                              →    /generate-prp initials/init-{feature}.md
Review generated PRP
                              →    /execute-prp prps/prp-{feature}.md
                                   Run tests, commit
```

See `docs/PLANNING.md` for full architecture and `docs/TASK.md` for current status.

## Reports

After each test run, open `reports/report.html` in a browser for a full HTML report with pass/fail status, screenshots on failure, and timing data.

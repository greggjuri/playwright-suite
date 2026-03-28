# init-004: GitHub Actions CI/CD Workflow

## Feature Overview

Add a GitHub Actions workflow that automatically runs the full Playwright test suite
against the three live production apps on every push to main and on a weekly schedule.

## Why This Matters

- **Automated safety net** — every push triggers 165 tests across 3 browsers
- **Weekly monitoring** — catches AWS outages or app breakage even without code changes
- **Resume artifact** — green badge on public repo signals professional-grade CI/CD
- **Phase 4 completion** — finishes the playwright-suite project

## File to Create

```
.github/workflows/playwright.yml     # NEW: GitHub Actions workflow
```

## Workflow Requirements

### Triggers
- `push` to `main` branch
- `schedule` — weekly on Monday at 06:00 UTC (`cron: '0 6 * * 1'`)
- `workflow_dispatch` — manual trigger from GitHub UI (useful for debugging)

### Job: test
- **Runner**: `ubuntu-latest`
- **Python**: 3.11 (pin to exact version)
- **Steps**:
  1. Checkout repo
  2. Set up Python 3.11
  3. Install dependencies from `requirements.txt` (pinned — `pip install -r requirements.txt`)
  4. Install Playwright browsers — Chromium only for CI (Firefox and WebKit add time/cost, Chromium is primary)
  5. Run pytest — Chromium only, generate HTML report
  6. Upload HTML report as workflow artifact (available for download from GitHub UI)

### Security Requirements (post-LiteLLM March 2026 standard)
- All `uses:` actions pinned to **commit hashes**, not tags
- Actions to use:
  - `actions/checkout` — pin to commit hash
  - `actions/setup-python` — pin to commit hash
  - `actions/upload-artifact` — pin to commit hash

### Commit hash lookup
Claude Code must look up the current commit hashes for these actions before writing
the workflow. Use `gh api` or check the GitHub releases page for each action:
- `actions/checkout` latest stable tag → get its commit SHA
- `actions/setup-python` latest stable tag → get its commit SHA
- `actions/upload-artifact` latest stable tag → get its commit SHA

### Pytest Command for CI
```bash
pytest tests/ --browser chromium --html=reports/report.html -v
```

### Report Artifact
- Upload `reports/` directory as artifact named `playwright-report`
- Retention: 7 days

## README Badge

After the workflow is created, add a badge to `README.md`:

```markdown
![Playwright Tests](https://github.com/greggjuri/playwright-suite/actions/workflows/playwright.yml/badge.svg)
```

Place it directly under the main heading in README.md.

## pytest.ini Check

Confirm `--browser chromium` is NOT in `addopts` (already fixed in Phase 3).
CI command specifies browser explicitly.

## Success Criteria

- [ ] `.github/workflows/playwright.yml` created with pinned action hashes
- [ ] Workflow triggers on push to main, weekly schedule, and manual dispatch
- [ ] `pip install -r requirements.txt` used (not loose pip install)
- [ ] Playwright browsers installed via `playwright install chromium` (not `--with-deps` unless needed on ubuntu)
- [ ] pytest runs and passes in CI environment
- [ ] HTML report uploaded as downloadable artifact
- [ ] README.md updated with workflow badge
- [ ] All `uses:` lines use commit hashes not tags
- [ ] Committed and pushed — workflow appears in GitHub Actions tab
- [ ] At least one successful workflow run visible on GitHub

## Technical Notes

- **Headless by default** — Playwright runs headless in CI automatically, no `--headless` flag needed
- **No secrets required** — all three test targets are public, no auth tokens needed
- **`playwright install chromium`** — installs only Chromium to keep CI fast. Full `playwright install` installs all browsers unnecessarily.
- **Ubuntu runner** — Playwright on Ubuntu may need system dependencies. If install fails use `playwright install --with-deps chromium`
- **Report artifact** — even if tests pass, the HTML report is useful to inspect. Upload unconditionally, not just on failure.
- **`if: always()`** — use on the upload step so the report uploads even when tests fail

## Out of Scope

- Firefox and WebKit in CI (adds ~2x runtime — Chromium is sufficient for automated runs)
- Slack/email notifications (can be added later)
- Matrix builds across Python versions
- Caching pip packages (nice to have, not required for Phase 4)

## Open Questions

- None

## References

- `docs/DECISIONS.md` ADR-004 — dependency pinning security standard (commit hashes)
- `docs/PLANNING.md` Phase 4 — CI/CD integration
- `requirements.txt` — fully pinned dependencies to install in CI

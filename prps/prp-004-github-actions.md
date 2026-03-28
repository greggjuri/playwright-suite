# PRP-004: GitHub Actions CI/CD Workflow

**Created**: 2026-03-28
**Initial**: `initials/init-004-github-actions.md`
**Status**: Complete

---

## Overview

### Problem Statement
The playwright-suite has 55 tests passing across 3 browsers locally, but no automated CI/CD exists. Every push to main should trigger automated test runs, and a weekly schedule should catch AWS outages or app breakage without code changes.

### Proposed Solution
Create a GitHub Actions workflow that runs the full Playwright test suite on Chromium against live production apps on every push to main, on a weekly schedule, and on manual dispatch. Upload the HTML report as a downloadable artifact. Add a status badge to README.md.

### Success Criteria
- [ ] `.github/workflows/playwright.yml` created with pinned action commit hashes
- [ ] Workflow triggers on push to main, weekly schedule, and manual dispatch
- [ ] `pip install -r requirements.txt` used (pinned deps per ADR-004)
- [ ] Playwright browsers installed via `playwright install --with-deps chromium`
- [ ] pytest runs Chromium only with HTML report generation
- [ ] HTML report uploaded as downloadable artifact (retention: 7 days)
- [ ] Report uploads even on test failure (`if: always()`)
- [ ] README.md updated with workflow status badge
- [ ] All `uses:` lines use commit hashes, not tags (ADR-004)
- [ ] Committed and pushed — workflow runs in GitHub Actions tab

---

## Context

### Related Documentation
- `docs/DECISIONS.md` — ADR-004 (pinned deps, commit hashes for Actions)
- `docs/PLANNING.md` — Phase 4 scope
- `docs/TASK.md` — Phase 4 backlog items

### Pinned Action Commit Hashes (looked up 2026-03-28)
| Action | Tag | Commit SHA |
|--------|-----|------------|
| `actions/checkout` | v4 | `34e114876b0b11c390a56381ad16ebd13914f8d5` |
| `actions/setup-python` | v5 | `a26af69be951a213d495a4c3e4e4022e16d87065` |
| `actions/upload-artifact` | v4 | `ea165f8d65b6e75b540449e92b4886f43607fa02` |

### Dependencies
- **Required**: `requirements.txt` (fully pinned, exists)
- **Required**: Tests passing locally on Chromium (confirmed: 55 pass)

### Files to Create/Modify
```
.github/workflows/playwright.yml    # NEW: CI workflow
README.md                           # MODIFY: add status badge
```

---

## Technical Specification

### Workflow Design

```yaml
name: Playwright Tests

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'     # Weekly Monday 06:00 UTC
  workflow_dispatch:          # Manual trigger

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Install Playwright browsers
        run: playwright install --with-deps chromium
      - name: Run tests
        run: pytest tests/ --browser chromium --html=reports/report.html -v
      - name: Upload report
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4
        if: always()
        with:
          name: playwright-report
          path: reports/
          retention-days: 7
```

### README Badge
```markdown
![Playwright Tests](https://github.com/greggjuri/playwright-suite/actions/workflows/playwright.yml/badge.svg)
```
Placed directly under the main heading in README.md.

---

## Implementation Steps

### Step 1: Create Workflow File
**File**: `.github/workflows/playwright.yml`

Create the GitHub Actions workflow with:
- Three triggers: push to main, weekly cron, manual dispatch
- Ubuntu latest runner with Python 3.11
- Pinned action commit hashes (not tags)
- `pip install -r requirements.txt` for pinned dependencies
- `playwright install --with-deps chromium` for Chromium + system deps on Ubuntu
- pytest command: `pytest tests/ --browser chromium --html=reports/report.html -v`
- Upload report artifact with `if: always()` and 7-day retention

**Validation**:
- [ ] All `uses:` lines have commit hashes with `# vX` comment
- [ ] No unpinned tags
- [ ] `--with-deps` flag on playwright install (Ubuntu needs system deps)

---

### Step 2: Add README Badge
**File**: `README.md`

Add the workflow status badge directly under the main heading.

**Validation**:
- [ ] Badge markdown is syntactically correct
- [ ] Points to correct workflow file path

---

### Step 3: Commit and Push
```bash
git add .github/workflows/playwright.yml README.md
git commit -m "feat: add GitHub Actions CI workflow with weekly schedule"
git push
```

The push to main will trigger the workflow — verify it passes in the GitHub Actions tab.

---

### Step 4: Verify Workflow Run
- Check GitHub Actions tab for a successful run
- Download the `playwright-report` artifact and verify it contains `report.html`
- Confirm the README badge shows green/passing

---

## Testing Requirements

This PRP does not create tests — it creates CI infrastructure to run existing tests.

| Check | Method | Expected Result |
|-------|--------|-----------------|
| Workflow triggers on push | Push commit to main | Workflow run appears in Actions tab |
| Tests pass in CI | Check workflow run log | 55 tests pass on Chromium |
| Report artifact exists | Download from workflow run | `reports/report.html` present |
| Badge shows status | View README on GitHub | Green "passing" badge |

---

## Error Handling

### Known Risks
| Risk | Cause | Mitigation |
|------|-------|------------|
| Playwright install fails on Ubuntu | Missing system dependencies | Use `--with-deps` flag |
| Tests fail due to network in CI | GitHub runner can't reach jurigregg.com | Tests target public AWS CloudFront — should be accessible |
| Rate limiting on live apps | 55 tests hitting production rapidly | No rate limiting expected — static S3/CloudFront + one Lambda app |
| `pip install` fails | Version mismatch on Python 3.11 vs 3.9 locally | requirements.txt is compatible — pure Python packages + Playwright |

---

## Rollback Plan

1. Delete `.github/workflows/playwright.yml`
2. Revert README.md badge addition
3. Push — workflow disappears from Actions tab

---

## Confidence Scores

| Dimension | Score (1-10) | Notes |
|-----------|--------------|-------|
| Clarity | **10** | Init spec is explicit — exact triggers, exact commands, exact actions to pin |
| Feasibility | **9** | Standard GitHub Actions setup. Only risk: system deps on Ubuntu (mitigated with `--with-deps`) |
| Completeness | **9** | Covers workflow, badge, commit hashes, artifact upload, all triggers |
| Alignment | **10** | Follows ADR-004 (pinned commit hashes), uses `requirements.txt`, Chromium only for CI |
| **Average** | **9.5** | |

---

## Notes

- **Chromium only in CI** — Firefox and WebKit are validated locally in Phase 3. CI runs Chromium to keep costs/time low.
- **`--with-deps`** — Ubuntu runners need system dependencies for Playwright browsers. The `--with-deps` flag handles this automatically.
- **`if: always()`** on upload — ensures the HTML report is available for debugging even when tests fail.
- **No secrets needed** — all three test targets are public AWS apps.
- **Python 3.11 in CI vs 3.9 locally** — the test suite uses standard Python with no 3.9-specific features. 3.11 is the current stable on ubuntu-latest.

# Execute PRP

Execute a Project Requirement Plan step-by-step.

## Arguments
- `$ARGUMENTS` - Path to PRP file (e.g., `prps/prp-blog-tests.md`)

## Instructions

You are executing a PRP (Project Requirement Plan) for the **playwright-suite** project —
a Python Playwright + pytest E2E test automation framework targeting jurigregg.com AWS-hosted web properties.

### Step 0: Pre-flight Checks

Before starting:
1. Read `CLAUDE.md` for coding conventions and POM patterns
2. Read the PRP at `$ARGUMENTS` completely
3. Verify the virtual environment is active and dependencies are installed
4. Check that confidence score is ≥ 7 (if not, stop and report concerns)
5. Confirm you understand the target app URL and test scenarios

```bash
# Verify environment
python --version
pytest --version
playwright --version
```

### Step 1: Execute Implementation Steps

For each implementation step in the PRP:

1. **Announce**: State which step you're starting
2. **Implement**: Write the POM class or test file
3. **Follow conventions**: Match POM pattern from `CLAUDE.md` exactly
4. **Validate**: Run pytest after each step
5. **Commit**: After tests pass, commit with conventional message

```bash
# After each step — always run against Chromium first
pytest tests/{test_file}.py --browser chromium -v

# Commit when passing
git add .
git commit -m "{type}: {description}"
```

### Step 2: Enforce These Rules During Implementation

- **No `time.sleep()`** — use `wait_for_load_state()`, `wait_for()`, or `expect()` with timeout
- **Locators as class constants** — never inline locator strings in test methods
- **Locator priority**: `get_by_role()` → `get_by_text()` → `get_by_label()` → CSS
- **Assert messages** — every `assert` must have a descriptive failure message
- **500-line limit** — split files if approaching

### Step 3: Handle Failures

If a test step fails:

1. **Diagnose**: Run with `--headed --slowmo 500` to watch the failure live
2. **Check screenshot**: Look in `reports/screenshots/` for visual state at failure
3. **Fix**: Make minimal changes to resolve — adjust locator, add wait, update assertion
4. **Document**: Note the issue in commit message
5. **Continue**: Only proceed when pytest passes

If unable to locate an element reliably:
1. Report the locator strategy attempted
2. Suggest alternative approaches
3. Ask for guidance before continuing

### Step 4: Run Full Test Validation

After all implementation steps:

```bash
# Full suite for the new tests — Chromium
pytest tests/{test_file}.py --browser chromium --html=reports/report.html -v

# Verify report generated
open reports/report.html
```

Record pass/fail for each test case. All must pass before proceeding.

### Step 5: Final Validation

```bash
# Run full suite to check for regressions
pytest tests/ --browser chromium -v
```

Verify:
- All new tests pass
- No existing tests broken
- HTML report generated cleanly
- No `time.sleep()` introduced (grep to confirm)

```bash
grep -r "time.sleep" tests/ pages/
# Should return nothing
```

### Step 6: Update Documentation

1. Update `docs/TASK.md`:
   - Move task from "In Progress" to "Recently Completed"
   - Add any locator learnings or flakiness notes to "Lessons Learned" in `docs/TESTING.md`

2. If new architectural decisions were made:
   - Add ADR to `docs/DECISIONS.md`

### Step 7: Report Completion

```
## PRP Execution Complete

**PRP**: prps/prp-{feature}.md
**Status**: Complete/Partial/Blocked

### Commits Made
- {commit hash}: {message}
- {commit hash}: {message}

### Tests
- New tests: X passing
- Full suite: X passing, 0 failing

### Success Criteria
- [x] Criterion 1
- [x] Criterion 2
- [ ] Criterion 3 (if incomplete, explain why)

### Issues Encountered
{List any locator issues, timing issues, or flakiness found and how resolved}

### Follow-up Items
{Any tests that should be added next, flakiness to monitor, etc.}
```

## Example Usage

```
/execute-prp prps/prp-blog-tests.md
```

## Commit Message Format

Use conventional commits:
- `feat: add BlogPage POM class with navigation locators`
- `test: add blog homepage and navigation test suite`
- `fix: update sports page locator for ESPN content container`
- `refactor: extract shared wait logic to BasePage`
- `docs: update TESTING.md with sports page flakiness note`

## Quality Standards

- **No file over 500 lines**: Split if approaching
- **No `time.sleep()`**: Zero tolerance — use Playwright waiting
- **All assertions have messages**: No bare `assert` statements
- **Locators are class constants**: Never inline in methods
- **Working commits**: Each commit has passing pytest

## Emergency Stop

If you encounter:
- A target app that is down or returning errors (not a test bug)
- A locator that cannot be made reliable without `time.sleep()`
- A requirement contradicting an existing ADR
- Unclear test scope

**STOP** and report before proceeding.

## Notes

- Take your time — a passing, well-structured test is worth more than a fast, flaky one
- `--headed --slowmo 500` is your best debugging tool
- It's okay to deviate from the PRP if you find a better locator strategy, but document why
- Leave the codebase better than you found it

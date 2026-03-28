# Generate PRP

Generate a comprehensive Project Requirement Plan (PRP) for a feature.

## Arguments
- `$ARGUMENTS` - Path to initial file (e.g., `initials/init-feature-name.md`)

## Instructions

You are generating a PRP (Project Requirement Plan) for the **playwright-suite** project —
a Python Playwright + pytest E2E test automation framework targeting jurigregg.com AWS-hosted web properties.

### Step 1: Gather Context

Read and internalize the following project documentation:
1. `CLAUDE.md` - Coding conventions, POM patterns, locator strategy, commit rules
2. `docs/PLANNING.md` - Architecture overview, test targets, phases
3. `docs/DECISIONS.md` - Past architecture decisions (do NOT contradict these)
4. `docs/TASK.md` - Current task status and backlog
5. `docs/TESTING.md` - Testing standards, locator priority, assertion patterns

### Step 2: Read the Initial File

Read the initial specification at `$ARGUMENTS`:
1. Understand which app is being tested (blog, metronome, sports)
2. Note the specific test scenarios requested
3. Identify what POM class(es) are needed
4. Check that all open questions are answered before proceeding

### Step 3: Research Codebase

Based on the feature description, research the existing codebase:
1. Check `pages/` for existing POM classes to extend or reference
2. Check `tests/` for existing test patterns to follow
3. Check `conftest.py` for available fixtures
4. Check `examples/` folder if present for reference patterns

### Step 4: Generate PRP

Create a new PRP file at `prps/prp-{feature-slug}.md` where:
- feature-slug matches the initial file name (e.g., `init-blog-tests.md` → `prp-blog-tests.md`)

Use the template at `prps/templates/prp-template.md` as the structure.

Fill in all sections:
1. **Overview**: Which app is being tested and what scenarios are covered
2. **Success Criteria**: Specific tests that must pass, browsers that must work
3. **Context**: Links to relevant docs, target URL, existing POM classes
4. **Technical Specification**: POM class design, locators, test class structure
5. **Implementation Steps**: Ordered, atomic tasks with exact file paths
   - Step 1 is always: create or extend the POM class in `pages/`
   - Step 2 is always: create the test file in `tests/`
   - Step 3 is always: run `pytest` and confirm passing
6. **Testing Requirements**: Which browsers to validate, what assertions to include
7. **Integration Test Plan**: Run commands and expected output
8. **Error Handling**: Known flaky scenarios (e.g., ESPN API latency on sports page)
9. **Open Questions**: Anything needing clarification before execution
10. **Rollback Plan**: Tests are additive — rollback = delete the new files

### Step 5: Score Confidence

Score confidence (1-10) on each dimension:
- **Clarity**: Are the test scenarios well-defined?
- **Feasibility**: Can the target app elements be reliably located?
- **Completeness**: Does the PRP cover the full POM + test file?
- **Alignment**: Does it follow POM pattern, locator priority, no `time.sleep()`?

Calculate overall confidence as the average.

If overall confidence is below 7:
- List specific concerns (e.g., "unable to identify reliable locator for X element")
- Ask clarifying questions
- Do NOT proceed until concerns are addressed

### Step 6: Output

1. Create the PRP file in `prps/` folder
2. Report the file path created
3. Display confidence scores
4. List any open questions or concerns

## Example Usage

```
/generate-prp initials/init-blog-tests.md
```

This would:
1. Read all context files
2. Read `initials/init-blog-tests.md`
3. Check `pages/` and `tests/` for existing patterns
4. Generate `prps/prp-blog-tests.md`
5. Report confidence and concerns

## Quality Checklist

Before completing, verify:
- [ ] Every implementation step has specific file paths
- [ ] POM class locators use the correct priority (role > text > label > CSS)
- [ ] No `time.sleep()` anywhere in the plan
- [ ] All assertions include descriptive failure messages
- [ ] Steps are atomic and can be validated individually with `pytest`
- [ ] No ADRs are contradicted (sync API, POM pattern, pinned deps)
- [ ] Rollback plan exists

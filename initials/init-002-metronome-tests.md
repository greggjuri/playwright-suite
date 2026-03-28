# init-002: Metronome Test Suite

## App Under Test

**Name**: Online Metronome
**URL**: https://metronome.jurigregg.com
**Stack**: Single HTML file with embedded CSS/JS on S3 + CloudFront
**Repo**: github.com/greggjuri/metronome

## What the App Does

A browser-based metronome using the Web Audio API for precise timing. User sets a BPM
value, starts the metronome, and hears clicks at the specified tempo. Beat 1 has an
accented (higher pitch) click. A visual beat display shows 4 boxes highlighting the
active beat in sequence. Includes a dark/light theme toggle and supports keyboard
shortcuts including spacebar for start/stop and numpad for BPM entry.

## Why This App

- **JS-rendered single page** — no routing, no API calls, teaches testing pure JS apps
- **UI controls** — BPM input, start/stop button, theme toggle
- **Keyboard interactions** — spacebar, numpad — Playwright keyboard simulation
- **State changes** — running vs stopped state, active beat highlighting
- **Theme persistence** — dark/light preference saved to localStorage

## Test Scenarios

### 1. Page Load
- Page loads at https://metronome.jurigregg.com
- Page title contains "Metronome"
- BPM input field is visible and has a default value
- Start/Stop button is visible
- Beat display (4 boxes) is visible
- Theme toggle button is visible

### 2. BPM Input
- BPM input accepts a valid value (e.g., `120`)
- BPM input accepts numpad entry (type `100` into field)
- BPM display updates to reflect entered value
- Default BPM is a reasonable value (between 40 and 220)

### 3. Start/Stop via Button
- Clicking Start button changes button state (text or appearance changes to indicate running)
- Clicking Stop button (or Start again) returns button to stopped state
- Beat display becomes active when running (at least one box highlighted)
- Beat display becomes inactive when stopped

### 4. Start/Stop via Spacebar
- Pressing spacebar starts the metronome (same as clicking Start)
- Pressing spacebar again stops the metronome
- Page does not scroll when spacebar is pressed (preventDefault confirmed)

### 5. Theme Toggle
- Clicking theme toggle button changes the visual theme
- Theme preference persists after page reload (localStorage)
- Both dark and light themes render without visual errors

### 6. Responsive Check
- Page renders correctly at mobile viewport (390x844 — iPhone 14)
- BPM input and Start/Stop button are visible and usable at mobile width

## Live DOM Inspection Results

Inspected live at https://metronome.jurigregg.com on 2026-03-27.

| Element | ARIA Label / Selector | Notes |
|---------|----------------------|-------|
| BPM input | `aria-label="Beats per minute"` | type="text", default value "120" |
| Start button (stopped) | `aria-label="Start metronome"` | text "Start" |
| Stop button (running) | `aria-label="Stop metronome"` | text "Stop" — aria-label changes when running |
| Beat counter container | `aria-label="Beat counter"` | Contains 4 `.beat` divs |
| Beat boxes | `.beat` with `data-beat="1"` through `data-beat="4"` | Active beat gets class `beat active` |
| Theme toggle | `aria-label="Toggle dark mode"` | Stays "Toggle dark mode" regardless of current theme |
| Number pad | `aria-label="Number pad"` (group) | Buttons 0-9, Clear, Backspace |
| Clear button | `aria-label="Clear"` text "C" | Clears BPM input |
| Backspace button | `aria-label="Backspace"` text "⌫" | Removes last digit |
| Theme storage key | `localStorage['metronome-theme']` | Values: "light" / "dark" |
| Theme data attribute | `document.documentElement.dataset.theme` | Values: "light" / "dark" |
| Spacebar hint | `aria-label="Press to start/stop"` | Static hint element |

## POM Design

### File: `pages/metronome_page.py`

Class: `MetronomePage(BasePage)`

Confirmed locators:
```python
BPM_INPUT = '[aria-label="Beats per minute"]'
START_BUTTON = '[aria-label="Start metronome"]'
STOP_BUTTON = '[aria-label="Stop metronome"]'
BEAT_COUNTER = '[aria-label="Beat counter"]'
BEAT_BOXES = '.beat'
ACTIVE_BEAT = '.beat.active'
THEME_TOGGLE = '[aria-label="Toggle dark mode"]'
NUMBER_PAD = '[aria-label="Number pad"]'
CLEAR_BUTTON = '[aria-label="Clear"]'
BACKSPACE_BUTTON = '[aria-label="Backspace"]'
```

Key methods:
- `load()` — navigate and wait for networkidle
- `get_bpm() -> str` — read BPM input value
- `set_bpm(value: str)` — click Clear then type new value via numpad buttons
- `click_start()` — click `[aria-label="Start metronome"]`
- `click_stop()` — click `[aria-label="Stop metronome"]`
- `press_spacebar()` — `page.keyboard.press("Space")`
- `is_running() -> bool` — check if `[aria-label="Stop metronome"]` is visible
- `has_active_beat() -> bool` — check if `.beat.active` exists
- `click_theme_toggle()` — click theme toggle button
- `get_theme() -> str` — read `document.documentElement.dataset.theme` via `page.evaluate()`
- `get_stored_theme() -> str` — read `localStorage['metronome-theme']` via `page.evaluate()`

## Test File

### File: `tests/test_metronome.py`

Classes:
- `TestMetronomeLoad` — page load and initial state
- `TestMetronomeBPM` — BPM input interactions
- `TestMetronomeControls` — start/stop via button and spacebar
- `TestMetronomeTheme` — theme toggle and persistence
- `TestMetronomeResponsive` — mobile viewport check

## Technical Notes — Confirmed from Live DOM

- **Button aria-label changes** — stopped state: `aria-label="Start metronome"`, running state: `aria-label="Stop metronome"`. Use this to detect running state reliably.
- **Active beat** — running beat gets CSS class `beat active` on the `.beat` div. `data-beat` attribute is "1" through "4".
- **Theme storage key** — `localStorage['metronome-theme']` (not `'theme'`). Values: `"light"` / `"dark"`.
- **Theme data attribute** — `document.documentElement.dataset.theme`. Read via `page.evaluate("document.documentElement.dataset.theme")`.
- **BPM entry via numpad** — the app has a custom on-screen numpad (buttons 0-9, Clear, Backspace). The text input also accepts direct keyboard typing. Use direct `page.fill()` on the input for simplicity.
- **Web Audio API** — Playwright cannot assert audio. Test UI state changes only.
- **No API calls** — fully static app. `wait_for_load_state("networkidle")` on load is sufficient.
- **Spacebar** — `page.keyboard.press("Space")` simulates spacebar. Confirm no scroll by checking `page.evaluate("window.scrollY")` before and after.

## Success Criteria

- [ ] `pages/metronome_page.py` created with POM class
- [ ] `tests/test_metronome.py` created with all test classes
- [ ] `pytest tests/test_metronome.py --browser chromium` passes with zero failures
- [ ] At minimum 10 passing tests
- [ ] Full suite still passing: `pytest tests/ --browser chromium`
- [ ] Committed with message: `feat: add Metronome POM and test suite`

## Out of Scope for This Init

- Asserting actual audio output (Web Audio API is not accessible to Playwright)
- Testing BPM accuracy/timing precision
- Testing numpad hardware keys (simulate via keyboard input only)
- Firefox and WebKit (Phase 3)

## Open Questions

- None — app is fully public, all scenarios are client-side only

## References

- `docs/DECISIONS.md` ADR-005 — why Metronome was selected as a test target
- `docs/TESTING.md` — keyboard interaction patterns, localStorage testing approach
- `CLAUDE.md` — POM class structure and conventions
- `pages/base_page.py` — BasePage to inherit from

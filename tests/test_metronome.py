import pytest
from playwright.sync_api import expect

from pages.metronome_page import MetronomePage


class TestMetronomeLoad:
    """Tests for initial page load and visible state."""

    def test_page_loads(self, page):
        """Page should load successfully at metronome.jurigregg.com."""
        metro = MetronomePage(page)
        metro.load()
        assert "metronome.jurigregg.com" in page.url, \
            f"Expected metronome.jurigregg.com in URL, got: {page.url}"

    def test_page_title_contains_metronome(self, page):
        """Page title should contain 'Metronome'."""
        metro = MetronomePage(page)
        metro.load()
        assert "Metronome" in metro.get_title(), \
            f"Expected 'Metronome' in title, got: {metro.get_title()}"

    def test_bpm_input_visible_with_default(self, page):
        """BPM input should be visible with a default value."""
        metro = MetronomePage(page)
        metro.load()
        bpm_input = page.locator(MetronomePage.BPM_INPUT)
        expect(bpm_input).to_be_visible()
        bpm = metro.get_bpm()
        assert bpm.isdigit(), \
            f"Default BPM should be a number, got: {bpm}"
        bpm_val = int(bpm)
        assert 40 <= bpm_val <= 220, \
            f"Default BPM should be between 40-220, got: {bpm_val}"

    def test_start_button_visible(self, page):
        """Start button should be visible on load."""
        metro = MetronomePage(page)
        metro.load()
        expect(page.locator(MetronomePage.START_BUTTON)).to_be_visible()

    def test_beat_display_visible(self, page):
        """Beat counter should be visible with 4 beat boxes."""
        metro = MetronomePage(page)
        metro.load()
        expect(page.locator(MetronomePage.BEAT_COUNTER)).to_be_visible()
        assert metro.get_beat_box_count() == 4, \
            f"Expected 4 beat boxes, got: {metro.get_beat_box_count()}"

    def test_theme_toggle_visible(self, page):
        """Theme toggle button should be visible."""
        metro = MetronomePage(page)
        metro.load()
        expect(page.locator(MetronomePage.THEME_TOGGLE)).to_be_visible()


class TestMetronomeBPM:
    """Tests for BPM input interactions."""

    def test_bpm_accepts_valid_value(self, page):
        """BPM input should accept and display a typed value."""
        metro = MetronomePage(page)
        metro.load()
        metro.set_bpm("100")
        assert metro.get_bpm() == "100", \
            f"Expected BPM to be '100' after fill, got: {metro.get_bpm()}"

    def test_default_bpm_in_range(self, page):
        """Default BPM should be a reasonable value between 40 and 220."""
        metro = MetronomePage(page)
        metro.load()
        bpm = int(metro.get_bpm())
        assert 40 <= bpm <= 220, \
            f"Default BPM should be between 40-220, got: {bpm}"


class TestMetronomeControls:
    """Tests for start/stop via button and spacebar."""

    def test_start_button_changes_state(self, page):
        """Clicking Start should switch to running state (Stop button visible)."""
        metro = MetronomePage(page)
        metro.load()
        metro.click_start()
        expect(page.locator(MetronomePage.STOP_BUTTON)).to_be_visible(
            timeout=3000
        )

    def test_stop_button_returns_to_stopped(self, page):
        """Clicking Stop should return to stopped state (Start button visible)."""
        metro = MetronomePage(page)
        metro.load()
        metro.click_start()
        expect(page.locator(MetronomePage.STOP_BUTTON)).to_be_visible(
            timeout=3000
        )
        metro.click_stop()
        expect(page.locator(MetronomePage.START_BUTTON)).to_be_visible(
            timeout=3000
        )

    def test_active_beat_when_running(self, page):
        """At least one beat box should be active when metronome is running."""
        metro = MetronomePage(page)
        metro.load()
        metro.click_start()
        expect(page.locator(MetronomePage.ACTIVE_BEAT)).to_be_visible(
            timeout=3000
        )

    def test_no_active_beat_when_stopped(self, page):
        """No beat box should be active after stopping the metronome."""
        metro = MetronomePage(page)
        metro.load()
        metro.click_start()
        expect(page.locator(MetronomePage.STOP_BUTTON)).to_be_visible(
            timeout=3000
        )
        metro.click_stop()
        expect(page.locator(MetronomePage.START_BUTTON)).to_be_visible(
            timeout=3000
        )
        expect(page.locator(MetronomePage.ACTIVE_BEAT)).to_have_count(0)

    def test_spacebar_starts_metronome(self, page):
        """Pressing spacebar should start the metronome."""
        metro = MetronomePage(page)
        metro.load()
        metro.press_spacebar()
        expect(page.locator(MetronomePage.STOP_BUTTON)).to_be_visible(
            timeout=3000
        )

    def test_spacebar_stops_metronome(self, page):
        """Pressing spacebar twice should stop the metronome."""
        metro = MetronomePage(page)
        metro.load()
        metro.press_spacebar()
        expect(page.locator(MetronomePage.STOP_BUTTON)).to_be_visible(
            timeout=3000
        )
        metro.press_spacebar()
        expect(page.locator(MetronomePage.START_BUTTON)).to_be_visible(
            timeout=3000
        )

    def test_spacebar_does_not_scroll(self, page):
        """Pressing spacebar should not scroll the page."""
        metro = MetronomePage(page)
        metro.load()
        scroll_before = metro.get_scroll_y()
        metro.press_spacebar()
        scroll_after = metro.get_scroll_y()
        assert scroll_before == scroll_after, \
            f"Page scrolled after spacebar: before={scroll_before}, after={scroll_after}"


class TestMetronomeTheme:
    """Tests for theme toggle and localStorage persistence."""

    def test_theme_toggle_changes_theme(self, page):
        """Clicking theme toggle should change the theme."""
        metro = MetronomePage(page)
        metro.load()
        initial_theme = metro.get_theme()
        metro.click_theme_toggle()
        new_theme = metro.get_theme()
        assert new_theme != initial_theme, \
            f"Theme should change after toggle, got '{new_theme}' both times"
        expected = "light" if initial_theme == "dark" else "dark"
        assert new_theme == expected, \
            f"Expected theme '{expected}' after toggle, got: {new_theme}"

    def test_theme_persists_after_reload(self, page):
        """Theme preference should persist in localStorage after reload."""
        metro = MetronomePage(page)
        metro.load()
        initial_theme = metro.get_theme()
        metro.click_theme_toggle()
        toggled_theme = metro.get_theme()
        assert toggled_theme != initial_theme, \
            "Theme should change after toggle"
        page.reload(wait_until="networkidle")
        reloaded_theme = metro.get_theme()
        assert reloaded_theme == toggled_theme, \
            f"Theme should persist after reload: expected '{toggled_theme}', got '{reloaded_theme}'"


class TestMetronomeResponsive:
    """Tests for mobile viewport rendering."""

    def test_mobile_page_renders(self, page):
        """Page should load successfully at iPhone 14 viewport (390x844)."""
        page.set_viewport_size({"width": 390, "height": 844})
        metro = MetronomePage(page)
        metro.load()
        assert "Metronome" in metro.get_title(), \
            f"Expected 'Metronome' in title at mobile viewport, got: {metro.get_title()}"

    def test_mobile_controls_usable(self, page):
        """BPM input and Start button should be visible at mobile width."""
        page.set_viewport_size({"width": 390, "height": 844})
        metro = MetronomePage(page)
        metro.load()
        expect(page.locator(MetronomePage.BPM_INPUT)).to_be_visible()
        expect(page.locator(MetronomePage.START_BUTTON)).to_be_visible()

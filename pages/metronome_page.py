from playwright.sync_api import expect

from pages.base_page import BasePage


class MetronomePage(BasePage):
    # Control locators (confirmed from live DOM — aria-labels)
    BPM_INPUT = '[aria-label="Beats per minute"]'
    START_BUTTON = '[aria-label="Start metronome"]'
    STOP_BUTTON = '[aria-label="Stop metronome"]'
    BEAT_COUNTER = '[aria-label="Beat counter"]'
    BEAT_BOXES = '.beat'
    ACTIVE_BEAT = '.beat.active'
    THEME_TOGGLE = '[aria-label="Toggle dark mode"]'
    CLEAR_BUTTON = '[aria-label="Clear"]'
    BACKSPACE_BUTTON = '[aria-label="Backspace"]'

    def __init__(self, page):
        super().__init__(page)
        self.base_url = "https://metronome.jurigregg.com"

    def load(self) -> None:
        """Navigate to Metronome and wait for full load."""
        self.navigate()
        self.page.wait_for_load_state("networkidle")

    def get_bpm(self) -> str:
        """Read the current BPM input value."""
        return self.page.locator(self.BPM_INPUT).input_value()

    def set_bpm(self, value: str) -> None:
        """Set the BPM input to a specific value."""
        self.page.locator(self.BPM_INPUT).fill(value)

    def click_start(self) -> None:
        """Click the Start metronome button."""
        self.page.locator(self.START_BUTTON).click()

    def click_stop(self) -> None:
        """Click the Stop metronome button."""
        self.page.locator(self.STOP_BUTTON).click()

    def press_spacebar(self) -> None:
        """Press the spacebar key."""
        self.page.keyboard.press("Space")

    def is_running(self) -> bool:
        """Check if metronome is running (Stop button visible)."""
        return self.page.locator(self.STOP_BUTTON).is_visible()

    def has_active_beat(self) -> bool:
        """Check if any beat box is currently active."""
        return self.page.locator(self.ACTIVE_BEAT).count() > 0

    def get_beat_box_count(self) -> int:
        """Count the number of beat boxes."""
        return self.page.locator(self.BEAT_BOXES).count()

    def click_theme_toggle(self) -> None:
        """Click the theme toggle button."""
        self.page.locator(self.THEME_TOGGLE).click()

    def get_theme(self) -> str:
        """Read the current theme from the document data attribute."""
        return self.page.evaluate("document.documentElement.dataset.theme")

    def get_stored_theme(self) -> str:
        """Read the theme stored in localStorage."""
        return self.page.evaluate(
            "localStorage.getItem('metronome-theme')"
        )

    def get_scroll_y(self) -> float:
        """Read the current vertical scroll position."""
        return self.page.evaluate("window.scrollY")

from playwright.sync_api import expect

from pages.base_page import BasePage


class MarkdownPage(BasePage):
    # Editor locators (confirmed from live DOM)
    EDITOR = "#markdown-input"
    PREVIEW = "#preview-output"
    AUTOSAVE_STATUS = "#autosave-status"
    WORD_COUNT = ".word-count"

    # Control locators
    THEME_TOGGLE = "#theme-toggle"
    CHEATSHEET_TOGGLE = "#cheatsheet-toggle"
    CHEATSHEET_PANEL = "#cheatsheet-panel"
    CLEAR_DRAFT = "#clear-draft"

    # Toolbar locators (no aria-labels — use data-action)
    TOOLBAR_BUTTONS = ".toolbar-btn"
    TOOLBAR_BOLD = '[data-action="bold"]'

    def __init__(self, page):
        super().__init__(page)

    def load(self) -> None:
        """Navigate to Markdown Editor and wait for full load."""
        self.navigate("/md/")
        self.page.wait_for_load_state("networkidle")

    def type_markdown(self, text: str) -> None:
        """Set editor value and trigger preview + word count update.

        Uses fill() then calls updatePreview() which also updates word
        count. The app's preview is debounced (150ms) on native input
        events, so calling updatePreview() directly is more reliable.
        """
        self.page.locator(self.EDITOR).fill(text)
        self.page.evaluate("updatePreview()")

    def get_editor_value(self) -> str:
        """Read the current editor textarea value."""
        return self.page.locator(self.EDITOR).input_value()

    def get_preview_html(self) -> str:
        """Read the preview pane innerHTML."""
        return self.page.locator(self.PREVIEW).inner_html()

    def get_word_count_text(self) -> str:
        """Read the word/character count display text."""
        return self.page.locator(self.WORD_COUNT).text_content()

    def get_autosave_status(self) -> str:
        """Read the autosave status text."""
        return self.page.locator(self.AUTOSAVE_STATUS).text_content()

    def click_theme_toggle(self) -> None:
        """Click the theme toggle button."""
        self.page.locator(self.THEME_TOGGLE).click()

    def is_dark_mode(self) -> bool:
        """Check if body has dark-mode class."""
        return "dark-mode" in self.get_body_class()

    def get_body_class(self) -> str:
        """Read body element className."""
        return self.page.evaluate("document.body.className")

    def get_stored_theme(self) -> str:
        """Read theme from localStorage."""
        return self.page.evaluate(
            "localStorage.getItem('markdown-editor-theme')"
        )

    def get_stored_draft(self):
        """Read draft from localStorage."""
        return self.page.evaluate(
            "localStorage.getItem('markdown-editor-draft')"
        )

    def click_cheatsheet_toggle(self) -> None:
        """Click the cheat sheet toggle button."""
        self.page.locator(self.CHEATSHEET_TOGGLE).click()

    def is_cheatsheet_visible(self) -> bool:
        """Check if cheat sheet panel is visible (no 'hidden' class)."""
        cls = self.page.locator(self.CHEATSHEET_PANEL).get_attribute("class") or ""
        return "hidden" not in cls

    def click_clear_draft(self) -> None:
        """Click the clear draft button (accepts confirm dialog)."""
        self.page.on("dialog", lambda d: d.accept())
        self.page.locator(self.CLEAR_DRAFT).click()

    def click_toolbar_bold(self) -> None:
        """Click the Bold toolbar button."""
        self.page.locator(self.TOOLBAR_BOLD).click()

    def select_all_editor(self) -> None:
        """Select all text in the editor."""
        self.page.locator(self.EDITOR).press("Meta+A")

    def press_bold_shortcut(self) -> None:
        """Press Cmd+B keyboard shortcut in the editor."""
        self.page.locator(self.EDITOR).press("Meta+b")

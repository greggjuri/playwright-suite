import pytest
from playwright.sync_api import expect

from pages.markdown_page import MarkdownPage


class TestMarkdownLoad:
    """Tests for initial page load and visible state."""

    def test_page_loads(self, page):
        """Page should load at jurigregg.com/md/."""
        md = MarkdownPage(page)
        md.load()
        assert "jurigregg.com/md" in page.url, \
            f"Expected jurigregg.com/md in URL, got: {page.url}"

    def test_page_title(self, page):
        """Page title should be 'Markdown Editor - jurigregg.com'."""
        md = MarkdownPage(page)
        md.load()
        assert md.get_title() == "Markdown Editor - jurigregg.com", \
            f"Unexpected title: {md.get_title()}"

    def test_editor_visible(self, page):
        """Editor textarea should be visible."""
        md = MarkdownPage(page)
        md.load()
        expect(page.locator(MarkdownPage.EDITOR)).to_be_visible()

    def test_preview_visible(self, page):
        """Preview pane should be visible."""
        md = MarkdownPage(page)
        md.load()
        expect(page.locator(MarkdownPage.PREVIEW)).to_be_visible()

    def test_toolbar_visible(self, page):
        """At least one toolbar button should be present."""
        md = MarkdownPage(page)
        md.load()
        count = page.locator(MarkdownPage.TOOLBAR_BUTTONS).count()
        assert count > 0, \
            f"Expected toolbar buttons, found: {count}"

    def test_word_count_initial(self, page):
        """Word count should show zeros on fresh load."""
        md = MarkdownPage(page)
        md.load()
        wc = md.get_word_count_text()
        assert "Words: 0" in wc, \
            f"Expected 'Words: 0' on empty editor, got: {wc}"
        assert "Characters: 0" in wc, \
            f"Expected 'Characters: 0' on empty editor, got: {wc}"


class TestMarkdownEditorPreview:
    """Tests for editor-to-preview live sync."""

    def test_heading_renders(self, page):
        """Typing '# Hello World' should render an <h1> in preview."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("# Hello World")
        preview = md.get_preview_html()
        assert "<h1>" in preview.lower(), \
            f"Expected <h1> in preview, got: {preview[:100]}"
        assert "Hello World" in preview, \
            f"Expected 'Hello World' in preview, got: {preview[:100]}"

    def test_bold_renders(self, page):
        """Typing '**bold text**' should render <strong> in preview."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("**bold text**")
        preview = md.get_preview_html()
        assert "<strong>" in preview.lower(), \
            f"Expected <strong> in preview, got: {preview[:100]}"

    def test_preview_updates_in_realtime(self, page):
        """Preview should update without page reload after typing."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("## Live Update")
        preview = md.get_preview_html()
        assert "<h2>" in preview.lower(), \
            f"Expected <h2> in preview after typing, got: {preview[:100]}"


class TestMarkdownWordCount:
    """Tests for word and character count updates."""

    def test_empty_editor_count(self, page):
        """Empty editor should show 0 words and 0 characters."""
        md = MarkdownPage(page)
        md.load()
        wc = md.get_word_count_text()
        assert "Words: 0" in wc, \
            f"Expected 'Words: 0', got: {wc}"

    def test_count_after_typing(self, page):
        """Typing 'Hello World' should show 2 words and 11 characters."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("Hello World")
        wc = md.get_word_count_text()
        assert "Words: 2" in wc, \
            f"Expected 'Words: 2', got: {wc}"
        assert "Characters: 11" in wc, \
            f"Expected 'Characters: 11', got: {wc}"


class TestMarkdownToolbar:
    """Tests for toolbar button interactions."""

    def test_bold_button_wraps_text(self, page):
        """Selecting text and clicking Bold should wrap in **...**."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("Hello")
        md.select_all_editor()
        md.click_toolbar_bold()
        val = md.get_editor_value()
        assert "**Hello**" in val, \
            f"Expected '**Hello**' after Bold button, got: {val}"


class TestMarkdownKeyboard:
    """Tests for keyboard shortcut interactions."""

    def test_bold_shortcut(self, page):
        """Selecting text and pressing Cmd+B should wrap in **...**."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("World")
        md.select_all_editor()
        md.press_bold_shortcut()
        val = md.get_editor_value()
        assert "**World**" in val, \
            f"Expected '**World**' after Cmd+B, got: {val}"


class TestMarkdownCheatSheet:
    """Tests for cheat sheet panel toggle."""

    def test_cheatsheet_toggle_opens(self, page):
        """Clicking cheat sheet toggle should open the panel."""
        md = MarkdownPage(page)
        md.load()
        assert not md.is_cheatsheet_visible(), \
            "Cheat sheet should be hidden on initial load"
        md.click_cheatsheet_toggle()
        assert md.is_cheatsheet_visible(), \
            "Cheat sheet should be visible after clicking toggle"

    def test_cheatsheet_toggle_closes(self, page):
        """Clicking cheat sheet toggle twice should close the panel."""
        md = MarkdownPage(page)
        md.load()
        md.click_cheatsheet_toggle()
        assert md.is_cheatsheet_visible(), \
            "Cheat sheet should be visible after first toggle"
        md.click_cheatsheet_toggle()
        assert not md.is_cheatsheet_visible(), \
            "Cheat sheet should be hidden after second toggle"


class TestMarkdownTheme:
    """Tests for theme toggle and body class changes."""

    def test_theme_toggle_changes_class(self, page):
        """Clicking theme toggle should change the body class."""
        md = MarkdownPage(page)
        md.load()
        initial_dark = md.is_dark_mode()
        md.click_theme_toggle()
        toggled_dark = md.is_dark_mode()
        assert toggled_dark != initial_dark, \
            f"Theme should change after toggle: was dark={initial_dark}, now dark={toggled_dark}"

    def test_theme_persists_after_reload(self, page):
        """Theme should persist in localStorage after page reload."""
        md = MarkdownPage(page)
        md.load()
        initial_dark = md.is_dark_mode()
        md.click_theme_toggle()
        toggled_dark = md.is_dark_mode()
        assert toggled_dark != initial_dark, \
            "Theme should change after toggle"
        page.reload(wait_until="networkidle")
        reloaded_dark = md.is_dark_mode()
        assert reloaded_dark == toggled_dark, \
            f"Theme should persist: expected dark={toggled_dark}, got dark={reloaded_dark}"


class TestMarkdownPersistence:
    """Tests for draft auto-save and persistence."""

    def test_autosave_status_updates(self, page):
        """Autosave status should update after typing."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("Auto-save test content")
        expect(page.locator(MarkdownPage.AUTOSAVE_STATUS)).to_contain_text(
            "Saved", timeout=5000
        )

    def test_draft_persists_after_reload(self, page):
        """Draft should be restored from localStorage after reload."""
        md = MarkdownPage(page)
        md.load()
        test_text = "Persistence test 12345"
        md.type_markdown(test_text)
        expect(page.locator(MarkdownPage.AUTOSAVE_STATUS)).to_contain_text(
            "Saved", timeout=5000
        )
        page.reload(wait_until="networkidle")
        restored = md.get_editor_value()
        assert test_text in restored, \
            f"Expected '{test_text}' in editor after reload, got: {restored[:50]}"


class TestMarkdownClearDraft:
    """Tests for clear draft functionality."""

    def test_clear_draft_empties_editor(self, page):
        """Clicking Clear Draft should empty the editor and localStorage."""
        md = MarkdownPage(page)
        md.load()
        md.type_markdown("Text to be cleared")
        expect(page.locator(MarkdownPage.AUTOSAVE_STATUS)).to_contain_text(
            "Saved", timeout=5000
        )
        md.click_clear_draft()
        val = md.get_editor_value()
        assert val == "", \
            f"Editor should be empty after clear, got: {val[:50]}"


class TestMarkdownResponsive:
    """Tests for mobile viewport rendering."""

    def test_mobile_page_renders(self, page):
        """Page should load at iPhone 14 viewport (390x844)."""
        page.set_viewport_size({"width": 390, "height": 844})
        md = MarkdownPage(page)
        md.load()
        assert "Markdown Editor" in md.get_title(), \
            f"Expected 'Markdown Editor' in title, got: {md.get_title()}"

    def test_mobile_editor_visible(self, page):
        """Editor and toolbar should be visible at mobile width."""
        page.set_viewport_size({"width": 390, "height": 844})
        md = MarkdownPage(page)
        md.load()
        expect(page.locator(MarkdownPage.EDITOR)).to_be_visible()
        assert page.locator(MarkdownPage.TOOLBAR_BUTTONS).count() > 0, \
            "Toolbar buttons should be present at mobile viewport"

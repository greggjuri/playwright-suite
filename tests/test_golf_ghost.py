import pytest
from playwright.sync_api import expect

from pages.golf_ghost_page import GolfGhostPage


class TestGolfGhostLoad:
    """Tests for initial page load and visible state."""

    def test_page_loads(self, page):
        """Page should load successfully at ghost.jurigregg.com."""
        ghost = GolfGhostPage(page)
        ghost.load()
        assert "ghost.jurigregg.com" in page.url, \
            f"Expected ghost.jurigregg.com in URL, got: {page.url}"

    def test_page_title_contains_golf_ghost(self, page):
        """Page title should contain 'Golf Ghost'."""
        ghost = GolfGhostPage(page)
        ghost.load()
        assert "Golf Ghost" in ghost.get_title(), \
            f"Expected 'Golf Ghost' in title, got: {ghost.get_title()}"

    def test_handicap_input_visible(self, page):
        """Handicap input field should be visible and enabled."""
        ghost = GolfGhostPage(page)
        ghost.load()
        handicap = page.locator(GolfGhostPage.HANDICAP_INPUT)
        expect(handicap).to_be_visible()
        expect(handicap).to_be_enabled()

    def test_course_selector_visible(self, page):
        """Course dropdown should be visible with at least one course option."""
        ghost = GolfGhostPage(page)
        ghost.load()
        select = page.locator(GolfGhostPage.COURSE_SELECT)
        expect(select).to_be_visible()
        options = select.locator("option")
        assert options.count() > 1, \
            f"Expected at least 2 options (placeholder + course), got: {options.count()}"

    def test_generate_button_visible(self, page):
        """Generate Round button should be visible."""
        ghost = GolfGhostPage(page)
        ghost.load()
        button = page.get_by_role("button", name="Generate Round")
        expect(button).to_be_visible()


class TestGolfGhostScoreGeneration:
    """Tests for the full score generation happy path."""

    def test_generate_score_happy_path(self, page):
        """Entering handicap, selecting course, and clicking Generate should produce a scorecard."""
        ghost = GolfGhostPage(page)
        ghost.load()
        ghost.generate_full_round("14.2")
        assert ghost.scorecard_is_visible(), \
            "Scorecard should be visible after generating a round"

    def test_scorecard_has_18_holes(self, page):
        """Scorecard should contain exactly 18 hole rows."""
        ghost = GolfGhostPage(page)
        ghost.load()
        ghost.generate_full_round("14.2")
        hole_count = ghost.get_hole_count()
        assert hole_count == 18, \
            f"Expected 18 hole rows, got: {hole_count}"

    def test_total_score_displayed(self, page):
        """Total gross score should be visible and non-empty."""
        ghost = GolfGhostPage(page)
        ghost.load()
        ghost.generate_full_round("14.2")
        total = ghost.get_total_score()
        assert total != "", "Total score should not be empty"
        assert total.isdigit(), \
            f"Total score should be a number, got: {total}"

    def test_score_cells_have_color(self, page):
        """At least one score cell should have color styling applied."""
        ghost = GolfGhostPage(page)
        ghost.load()
        ghost.generate_full_round("14.2")
        assert ghost.has_colored_score_cells(), \
            "At least one score cell should have an inline color style"


class TestGolfGhostScorecard:
    """Tests for scorecard structure and content."""

    def test_hole_numbers_1_through_18(self, page):
        """Scorecard should display hole numbers 1 through 18."""
        ghost = GolfGhostPage(page)
        ghost.load()
        ghost.generate_full_round("14.2")
        first_cells = ghost.get_row_first_cells()
        hole_numbers = [c for c in first_cells if c.isdigit()]
        expected = [str(i) for i in range(1, 19)]
        assert hole_numbers == expected, \
            f"Expected holes 1-18, got: {hole_numbers}"

    def test_par_values_present(self, page):
        """Par values should be present for all 18 holes."""
        ghost = GolfGhostPage(page)
        ghost.load()
        ghost.generate_full_round("14.2")
        pars = ghost.get_par_values()
        assert len(pars) == 18, \
            f"Expected 18 par values, got: {len(pars)}"
        for i, par in enumerate(pars, start=1):
            assert par.isdigit() and int(par) in (3, 4, 5), \
                f"Hole {i} par should be 3, 4, or 5, got: {par}"

    def test_scorecard_has_expected_columns(self, page):
        """Scorecard should have Hole, Yds, Par, Hcp, Str, Gross, Net columns."""
        ghost = GolfGhostPage(page)
        ghost.load()
        ghost.generate_full_round("14.2")
        headers = ghost.get_column_headers()
        expected = ["Hole", "Yds", "Par", "Hcp", "Str", "Gross", "Net"]
        assert headers == expected, \
            f"Expected columns {expected}, got: {headers}"


class TestGolfGhostResponsive:
    """Tests for mobile viewport rendering."""

    def test_mobile_page_renders(self, page):
        """Page should load successfully at iPhone 14 viewport (390x844)."""
        page.set_viewport_size({"width": 390, "height": 844})
        ghost = GolfGhostPage(page)
        ghost.load()
        assert "Golf Ghost" in ghost.get_title(), \
            f"Expected 'Golf Ghost' in title at mobile viewport, got: {ghost.get_title()}"

    def test_mobile_form_elements_usable(self, page):
        """Form elements should be visible and usable at mobile width."""
        page.set_viewport_size({"width": 390, "height": 844})
        ghost = GolfGhostPage(page)
        ghost.load()
        expect(page.locator(GolfGhostPage.HANDICAP_INPUT)).to_be_visible()
        expect(page.locator(GolfGhostPage.COURSE_SELECT)).to_be_visible()
        expect(page.get_by_role("button", name="Generate Round")).to_be_visible()

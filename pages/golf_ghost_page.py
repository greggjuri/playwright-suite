from playwright.sync_api import expect

from pages.base_page import BasePage


class GolfGhostPage(BasePage):
    # Form locators
    HANDICAP_INPUT = "#handicap-input"
    COURSE_SELECT = "#course-select"

    # Scorecard locators
    SCORECARD_TABLE = "table"
    HOLE_ROWS = "table tbody tr"
    SCORE_CELLS_WITH_COLOR = "td[style*='color']"

    def __init__(self, page):
        super().__init__(page)
        self.base_url = "https://ghost.jurigregg.com"

    def load(self) -> None:
        """Navigate to Golf Ghost and wait for full load."""
        self.navigate()
        self.page.wait_for_load_state("networkidle")

    def enter_handicap(self, value: str) -> None:
        """Fill the handicap input field."""
        self.page.locator(self.HANDICAP_INPUT).fill(value)

    def select_course(self, index: int = 1) -> None:
        """Select a course by option index (0 is placeholder)."""
        self.page.locator(self.COURSE_SELECT).select_option(index=index)

    def generate_score(self) -> None:
        """Click the Generate Round button."""
        self.page.get_by_role("button", name="Generate Round").click()

    def wait_for_scorecard(self) -> None:
        """Wait for the scorecard table to appear after Lambda API call."""
        expect(self.page.locator(self.SCORECARD_TABLE)).to_be_visible(
            timeout=15000
        )

    def get_hole_rows(self):
        """Return all tbody rows in the scorecard table."""
        return self.page.locator(self.HOLE_ROWS)

    def get_hole_count(self) -> int:
        """Count individual hole rows (excludes OUT/IN/TOT summary rows)."""
        rows = self.get_hole_rows()
        count = 0
        for i in range(rows.count()):
            first_cell = rows.nth(i).locator("td").first.text_content()
            if first_cell.isdigit():
                count += 1
        return count

    def get_total_score(self) -> str:
        """Read the gross score from the TOT row."""
        rows = self.get_hole_rows()
        for i in range(rows.count()):
            first_cell = rows.nth(i).locator("td").first.text_content()
            if first_cell == "TOT":
                # Gross score is the 6th column (index 5)
                return rows.nth(i).locator("td").nth(5).text_content()
        return ""

    def scorecard_is_visible(self) -> bool:
        """Check if the scorecard table is visible."""
        return self.page.locator(self.SCORECARD_TABLE).is_visible()

    def has_colored_score_cells(self) -> bool:
        """Check if at least one score cell has an inline color style."""
        return self.page.locator(self.SCORE_CELLS_WITH_COLOR).count() > 0

    def get_column_headers(self) -> list[str]:
        """Return the scorecard table column headers."""
        headers = self.page.locator("table thead th")
        return [headers.nth(i).text_content() for i in range(headers.count())]

    def get_row_first_cells(self) -> list[str]:
        """Return the first cell text of every tbody row."""
        rows = self.get_hole_rows()
        return [
            rows.nth(i).locator("td").first.text_content()
            for i in range(rows.count())
        ]

    def get_par_values(self) -> list[str]:
        """Return par values for all 18 hole rows (3rd column, index 2)."""
        rows = self.get_hole_rows()
        pars = []
        for i in range(rows.count()):
            first_cell = rows.nth(i).locator("td").first.text_content()
            if first_cell.isdigit():
                par = rows.nth(i).locator("td").nth(2).text_content()
                pars.append(par)
        return pars

    def generate_full_round(self, handicap: str = "14.2") -> None:
        """Convenience: select course, enter handicap, generate, wait."""
        self.select_course(index=1)
        self.enter_handicap(handicap)
        self.generate_score()
        self.wait_for_scorecard()

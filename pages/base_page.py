class BasePage:
    def __init__(self, page):
        self.page = page
        self.base_url = "https://jurigregg.com"

    def navigate(self, path: str = "") -> None:
        """Navigate to a path relative to base_url."""
        self.page.goto(f"{self.base_url}{path}")

    def get_title(self) -> str:
        return self.page.title()

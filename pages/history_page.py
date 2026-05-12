from pages.base_page import BasePage

class HistoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.rows = page.locator("tr")
        self.fee_cells = page.locator("td:nth-child(5)")
        self.clear_history_btn = page.get_by_role("button", name="Clear All History")

    def navigate(self):
        self.logger.info("Opening history page")
        super().navigate("/history")

    def get_row_by_plate(self, plate: str):
        self.logger.info(f"Finding history row for plate={plate}")
        return self.rows.filter(has_text=plate).last
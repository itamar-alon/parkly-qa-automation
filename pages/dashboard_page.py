from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.plate_input = page.locator("#car_plate")
        self.slot_input = page.locator("#slot")
        self.vehicle_type_select = page.locator("#vehicle_type_id")
        self.file_input = page.locator("#image")
        
        self.start_btn = page.locator("#submit")
        
    def navigate(self):
        self.logger.info("Opening dashboard page")
        super().navigate("/")
        
    def start_parking(self, plate: str, slot: str):
        self.logger.info(f"Starting parking for plate={plate}, slot={slot}")
        self.plate_input.fill(plate)
        
        self.slot_input.fill(slot)
        
        self.vehicle_type_select.select_option(index=0)
        
        self.start_btn.click()
        
    def get_active_row(self, plate: str):
        self.logger.info(f"Locating active row for plate={plate}")
        return self.page.locator("tr").filter(has_text=plate)
        
    def end_parking(self, plate: str):
        self.logger.info(f"Ending parking for plate={plate}")
        row = self.get_active_row(plate)
        row.get_by_role("button").click()
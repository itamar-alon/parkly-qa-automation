import os
import pytest
from playwright.sync_api import expect
import logging
import pytest_check as check

class TestE2EFlows:

    @pytest.fixture(autouse=True)
    def setup_login(self, login_page):
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        login_page.page.wait_for_url(f"{login_page.base_url}/")
        login_page.console_errors.clear()
        
    def test_e2e_full_parking_and_system_audit(self, dashboard_page, history_page, users_page):
        """
        Scenario 1: Happy Path - Full Parking Lifecycle + System Audit
        Reasoning: Validates the core flow and ensures all main modules (Dashboard, History, Users) 
        are accessible and healthy after a business action.
        """
        logging.info("Starting Full System Audit: Parking Lifecycle to User Management")
        car_plate = "77778888"
        slot_id = "55"

        dashboard_page.start_parking(car_plate, slot_id)
        logging.info(f"Started parking for plate {car_plate} at slot {slot_id}")
        
        active_row = dashboard_page.get_active_row(car_plate)
        expect(active_row).to_be_visible(timeout=5000)
        
        end_btn = active_row.locator("button, input[type='submit']").last
        expect(end_btn).to_be_enabled(timeout=5000)
        end_btn.click()
        logging.info("Clicked End Parking button")
        
        history_page.navigate()
        history_row = history_page.get_row_by_plate(car_plate).first
        expect(history_row).to_be_visible(timeout=5000)

        slot_text = history_row.locator("td").nth(1).inner_text()
        assert slot_text == slot_id, f"Data Mismatch: Expected slot {slot_id} but found {slot_text}"

        img_locator = history_row.locator("img")
        if img_locator.count() > 0:
            assert not history_page.is_image_broken(img_locator), "Found a broken image in history row"

        users_page.navigate()
        logging.info("Navigated to Users page for audit")
        expect(users_page.get_user_row("admin")).to_be_visible()
        
        all_errors = users_page.check_for_console_errors()
        filtered_errors = [e for e in all_errors if "favicon" not in e.lower()]
        check.equal(len(filtered_errors), 0, f"Critical JS errors found during audit: {filtered_errors}")

    def test_e2e_duplicate_parking_prevention(self, dashboard_page):
        """
        Scenario 2: Negative Path - Duplicate Parking Prevention
        """
        logging.info("Starting Negative test: Duplicate Parking Prevention")
        car_plate = "55556666"

        dashboard_page.start_parking(car_plate, "10")
        expect(dashboard_page.get_active_row(car_plate)).to_be_visible()

        dashboard_page.start_parking(car_plate, "11")
        logging.info("Attempted duplicate parking - checking for error feedback")
        
        error_message = dashboard_page.get_toast_message()
        expect(error_message).to_be_visible(timeout=5000)
        
        all_errors = dashboard_page.check_for_console_errors()
        filtered_errors = [e for e in all_errors if "favicon" not in e.lower()]
        check.equal(len(filtered_errors), 0, f"Unexpected JS errors during negative test: {filtered_errors}")
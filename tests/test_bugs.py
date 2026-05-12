import os
import pytest
from playwright.sync_api import expect
import logging

class TestBugsFound:

    def test_bug_001_forgot_password_link_redirect(self, login_page):
        """
        Bug: Forgot password link redirects to a cat picture instead of recovery page.
        """
        login_page.navigate()
        login_page.forgot_password_link.click()
        expect(login_page.page).not_to_have_url("https://cataas.com/cat")

    def test_bug_002_deferred_login_failure_feedback(self, login_page):
        """
        Bug: Submitting invalid credentials shows no error message on the Login page. 
        RCA: Messages are stored in the session but only displayed after a subsequent successful login.
        """
        login_page.navigate()
        login_page.login("wrong_user", "wrong_pass")
        
        error_locator = login_page.get_toast_message()
        expect(error_locator).to_be_visible()

    def test_bug_003_slot_zero_accepted(self, login_page, dashboard_page):
        """
        Bug: System allows starting a parking session in slot 0.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        
        dashboard_page.start_parking("11223344", "0")
        active_parking = dashboard_page.get_active_row("0")
        expect(active_parking).not_to_be_visible()

    def test_bug_004_license_plate_validation_failure(self, login_page, dashboard_page):
        """
        Bug: The system accepts invalid license plates (too short, too long, or with letters).
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        
        invalid_plates = ["123", "123456789012345", "ABCDEFGH"]
        for plate in invalid_plates:
            dashboard_page.start_parking(plate, "99")
            active_row = dashboard_page.page.locator("tr").filter(has_text=plate).first
            expect(active_row).not_to_be_visible()

    def test_bug_005_missing_aria_label_password_toggle(self, login_page):
        """
        Bug: The "Show Password" toggle button is missing an aria-label.
        """
        login_page.navigate()
        expect(login_page.password_toggle).to_have_attribute("aria-label", "/.+/")

    def test_bug_006_broken_routes_raw_404(self, login_page):
        """
        Bug: Accessing protected routes directly returns raw 404 instead of redirecting.
        """
        login_page.page.goto(f"{login_page.base_url}/dashboard")
        expect(login_page.page.locator("body")).not_to_contain_text("Not Found")

    def test_bug_007_missing_favicon(self, login_page):
        """
        Bug: Application throws 404 console error for missing favicon.ico.
        """
        login_page.navigate()
        errors = login_page.check_for_console_errors()
        assert not any("favicon.ico" in e for e in errors)

    def test_bug_008_admin_self_deletion(self, login_page, users_page):
        """
        Bug: Logged in admin can delete their own account.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        users_page.navigate()
        
        admin_row = users_page.get_user_row("admin")
        delete_btn = admin_row.locator("button:has_text('מחק')")
        expect(delete_btn).to_be_disabled()

    def test_bug_009_negative_slot_accepted(self, login_page, dashboard_page):
        """
        Bug: System accepts negative slot numbers.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        
        dashboard_page.start_parking("88889999", "-5")
        active_parking = dashboard_page.get_active_row("-5")
        expect(active_parking).not_to_be_visible()

    def test_bug_010_fee_calculation_string_error(self, login_page, dashboard_page, history_page):
        """
        Bug: Fee calculation shows '(חיוב: error)' for certain sessions.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        
        plate = "99990000"
        dashboard_page.start_parking(plate, "77")
        active_row = dashboard_page.get_active_row(plate)
        active_row.locator("button").click() 
        
        history_page.navigate()
        history_row = history_page.get_row_by_plate(plate).first
        expect(history_row).not_to_contain_text("error")

    def test_bug_011_image_upload_missing_accept(self, login_page, dashboard_page):
        """
        Bug: Image upload input lacks accept="image/*" attribute.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        
        file_input = dashboard_page.page.locator("input[type='file']")
        expect(file_input).to_have_attribute("accept", "image/*")

    def test_bug_012_alphabetical_slot_accepted(self, login_page, dashboard_page):
        """
        Bug: The system accepts alphabetical (English/Hebrew) and special characters as a valid parking slot.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        
        
        for invalid_slot in ["abc", "אבג", "!@#"]:
            dashboard_page.start_parking("11223344", invalid_slot)
            active_parking = dashboard_page.page.locator("tr").filter(has_text=invalid_slot).first
            expect(active_parking).not_to_be_visible()

    def test_bug_013_timestamp_microsecond_overlap(self, login_page, dashboard_page):
        """
        Bug: ISO timestamps with microseconds overlap UI elements.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        
        dashboard_page.start_parking("12121212", "44")
        active_row = dashboard_page.get_active_row("12121212")
        time_cell = active_row.locator("td").nth(2) 
        
        expect(time_cell).not_to_contain_text(".")

    def test_bug_014_history_images_404_path_encoding(self, login_page, history_page):
        """
        Bug: History page attempts to load images from broken paths due to backslash encoding (%5C).
        RCA: Windows-style paths from the backend are not correctly converted to URL-friendly forward slashes.
        """
        login_page.navigate()
        login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
        history_page.navigate()
        
        
        errors = history_page.check_for_console_errors()
        assert not any("uploads%5C" in e for e in errors)

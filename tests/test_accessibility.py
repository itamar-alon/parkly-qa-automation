import pytest
from playwright.sync_api import expect

class TestAccessibility:
    """
    Accessibility test suite checking for basic WCAG compliance issues.
    """

    def test_login_page_accessibility(self, login_page):
        login_page.navigate()
        
        
        images = login_page.page.locator("img")
        for i in range(images.count()):
            alt = images.nth(i).get_attribute("alt")
            assert alt is not None, f"Image {i} on Login Page is missing an alt attribute"

        
        inputs = login_page.page.locator("input:not([type='hidden'])")
        for i in range(inputs.count()):
            input_id = inputs.nth(i).get_attribute("id")
            if input_id:
                label = login_page.page.locator(f"label[for='{input_id}']")
                
                aria_label = inputs.nth(i).get_attribute("aria-label")
                assert label.count() > 0 or aria_label, f"Input '{input_id}' is missing a linked label or aria-label"

    def test_dashboard_interactive_elements_a11y(self, login_page, dashboard_page):
        login_page.navigate()
        login_page.login("admin", "password")
        
        
        
        login_page.navigate() 
        expect(login_page.password_toggle).to_have_attribute("aria-label", "/.+/", timeout=1000)

    def test_dashboard_images_alt_text(self, login_page, dashboard_page):
        login_page.navigate()
        login_page.login("admin", "password")
        
        
        dashboard_page.start_parking("22334455", "101")
        
        images = dashboard_page.page.locator("img")
        for i in range(images.count()):
            alt = images.nth(i).get_attribute("alt")
            assert alt and len(alt.strip()) > 0, f"Image {i} on Dashboard is missing descriptive alt text"

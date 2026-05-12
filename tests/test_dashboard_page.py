import os
import pytest
from playwright.sync_api import expect

@pytest.fixture(autouse=True)
def setup(login_page):
    login_page.navigate()
    login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))

def test_dashboard_page_load(dashboard_page):
    dashboard_page.navigate()
    expect(dashboard_page.page.get_by_text("חניות פעילות נוכחיות")).to_be_visible()
    expect(dashboard_page.plate_input).to_be_visible()

def test_start_parking_action(dashboard_page):
    dashboard_page.navigate()
    dashboard_page.start_parking("12121212", "99")
    expect(dashboard_page.get_active_row("12121212")).to_be_visible()

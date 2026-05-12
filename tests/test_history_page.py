import os
import pytest
from playwright.sync_api import expect

@pytest.fixture(autouse=True)
def setup(login_page):
    login_page.navigate()
    login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))

def test_history_page_load(history_page):
    history_page.navigate()
    expect(history_page.page.get_by_text("Parking History")).to_be_visible()
    expect(history_page.page.locator("table")).to_be_visible()

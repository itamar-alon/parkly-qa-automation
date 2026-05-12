import os
import pytest
from playwright.sync_api import expect

@pytest.fixture(autouse=True)
def setup(login_page):
    login_page.navigate()
    login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))

def test_users_page_load(users_page):
    users_page.navigate()
    expect(users_page.page.locator(".users-header")).to_have_text("Users")
    expect(users_page.get_user_row("admin")).to_be_visible()
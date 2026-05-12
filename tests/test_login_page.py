import os
import pytest
from playwright.sync_api import expect

def test_login_page_load(login_page):
    login_page.navigate()
    expect(login_page.page).to_have_title("כניסה לחשבון שלי")
    expect(login_page.username_input).to_be_visible()
    expect(login_page.password_input).to_be_visible()

def test_login_successful(login_page):
    login_page.navigate()
    login_page.login(os.getenv("ADMIN_USER", "admin"), os.getenv("ADMIN_PASS", "password"))
    expect(login_page.page).to_have_url(f"{login_page.base_url}/")

import os
import pytest
from playwright.sync_api import APIRequestContext, expect


@pytest.fixture(scope="session")
def base_api_url() -> str:
    return "http://localhost:5000"

def test_api_health_check(playwright, base_api_url):
    """
    Verify the application server is up and responding to basic HTTP requests.
    """
    api_context = playwright.request.new_context(base_url=base_api_url)
    response = api_context.get("/")
    
    assert response.status == 200
    assert "text/html" in response.headers.get("content-type", "")

def test_api_unauthorized_access(playwright, base_api_url):
    """
    Verify that protected API routes/pages deny access to unauthenticated requests.
    Flask typically returns a 302 Redirect to the login page for unauthorized access.
    """
    api_context = playwright.request.new_context(base_url=base_api_url)
    
    response = api_context.get("/dashboard")
    
    assert response.status == 200
    assert "/login" in response.url

def test_api_authentication_success(playwright, base_api_url):
    """
    Verify backend authentication logic using form-data submission.
    This simulates the HTTP POST request sent by the browser.
    """
    api_context = playwright.request.new_context(base_url=base_api_url)
    
    username = os.getenv("ADMIN_USER", "admin")
    password = os.getenv("ADMIN_PASS", "password")
    
    login_response = api_context.post(
        "/login",
        form={
            "username": username,
            "password": password
        }
    )
    
    assert login_response.status == 200
    assert "/dashboard" in login_response.url
    
    cookies = api_context.cookies()
    session_cookie = next((cookie for cookie in cookies if cookie['name'] == 'session'), None)
    assert session_cookie is not None, "Backend did not set a session cookie upon login."

def test_api_authentication_failure(playwright, base_api_url):
    """
    Verify backend rejects invalid credentials via API.
    """
    api_context = playwright.request.new_context(base_url=base_api_url)
    
    login_response = api_context.post(
        "/login",
        form={
            "username": "invalid_user",
            "password": "wrong_password"
        }
    )
    
    assert "/login" in login_response.url
    
def test_api_robots_txt_exists(playwright, base_api_url):
    """
    Bug Discovery: Check if robots.txt exists.
    Commonly missing in this application, causing unnecessary 404s.
    """
    api_context = playwright.request.new_context(base_url=base_api_url)
    
    response = api_context.get("/robots.txt")
    
    assert response.status == 200, f"Expected robots.txt to be present (200), but got {response.status}"
    
    assert "User-agent" in response.text(), "robots.txt is missing standard User-agent header" 

def test_api_brute_force_vulnerability(playwright, base_api_url):
    """
    Bug Discovery (Security): System lacks Rate Limiting / Brute Force protection on login.
    A secure system should return HTTP 429 or block the IP after ~5-10 failed attempts.
    """
    api_context = playwright.request.new_context(base_url=base_api_url)
    
    
    for i in range(20):
        response = api_context.post(
            "/login",
            form={"username": "admin", "password": f"wrong_{i}"}
        )
        
        
        
        assert response.status != 429, f"System blocked request on attempt {i}. Vulnerability might be fixed!"
        
    
    assert True 

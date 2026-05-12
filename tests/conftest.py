import os
import sys
import pytest
import requests
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

def pytest_configure(config):
    logs_dir = os.getenv("LOG_DIR", os.path.join(PROJECT_ROOT, "logs"))
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file = os.path.join(logs_dir, "automation.log")
    
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logging.info("=== Test Session Started ===")

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://mock-n8n-webhook-url.com/webhook/qa-results")


@pytest.fixture
def login_page(page):
    from pages.login_page import LoginPage
    return LoginPage(page)

@pytest.fixture
def dashboard_page(page):
    from pages.dashboard_page import DashboardPage
    return DashboardPage(page)

@pytest.fixture
def history_page(page):
    from pages.history_page import HistoryPage
    return HistoryPage(page)

@pytest.fixture
def users_page(page):
    from pages.users_page import UsersPage
    return UsersPage(page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        status = report.outcome.upper()
        logging.info(f"Test Result: {item.name} -> {status}")
        if report.failed:
            logging.error(f"Reason of failure: {report.longreprtext}")

def pytest_runtest_setup(item):
    logging.info(f"--- Starting Test Case: {item.name} ---")

def pytest_sessionfinish(session, exitstatus):
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    
    if reporter:
        passed = len(reporter.stats.get("passed", []))
        failed = len(reporter.stats.get("failed", []))
        skipped = len(reporter.stats.get("skipped", []))
        total = passed + failed + skipped
        
        payload = {
            "timestamp": datetime.now().isoformat(),
            "project": "Parkly QA Automation",
            "environment": "Docker Local",
            "results": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "exit_status": str(exitstatus)
            },
            "status": "FAILED" if failed > 0 else "SUCCESS"
        }
        
        logging.info(f"=== Session Finished. Results: {passed}/{total} Passed ===")
        
        try:
            if "mock" not in N8N_WEBHOOK_URL.lower():
                response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
                logging.info(f"[n8n] Webhook sent. Status: {response.status_code}")
            else:
                logging.info(f"[n8n] Mock mode active. Results: {payload['status']}")
                
        except Exception as e:
            logging.warning(f"[n8n] Webhook failed: {e}")
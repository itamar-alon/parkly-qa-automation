from playwright.sync_api import Page, expect
import os
import logging

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = os.getenv("APP_URL", "http://localhost:5000")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.console_errors = []
        self.page.on("console", lambda msg: self._collect_error(msg))

    def _collect_error(self, msg):
        if msg.type == "error":
            self.console_errors.append(msg.text)
            self.logger.error(f"Console error captured: {msg.text}")

    def navigate(self, path: str = ""):
        full_url = f"{self.base_url}{path}"
        self.logger.info(f"Navigating to: {full_url}")
        self.page.goto(full_url)

    def get_toast_message(self):
        return self.page.locator(".error, .toast-error, .alert, .invalid-feedback").first

    def is_image_broken(self, locator):
        try:
            return self.page.evaluate(
                "(img) => !img.complete || img.naturalWidth === 0", 
                locator.element_handle()
            )
        except:
            return True

    def check_for_console_errors(self):
        self.logger.info(f"Collected {len(self.console_errors)} console error(s)")
        return self.console_errors
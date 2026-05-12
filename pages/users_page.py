from pages.base_page import BasePage

class UsersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_user_btn = page.get_by_role("button", name="Add User")
        self.user_rows = page.locator("tr")
        self.delete_buttons = page.get_by_role("button", name="Delete")

    def navigate(self):
        self.logger.info("Opening users page")
        super().navigate("/users")

    def get_user_row(self, username: str):
        self.logger.info(f"Getting row for user={username}")
        return self.user_rows.filter(has_text=username)

    def is_user_present(self, username: str):
        is_present = self.get_user_row(username).count() > 0
        self.logger.info(f"User present check for {username}: {is_present}")
        return is_present

    def delete_user(self, username: str):
        self.logger.info(f"Deleting user={username}")
        row = self.get_user_row(username)
        row.get_by_role("button", name="Delete").click()
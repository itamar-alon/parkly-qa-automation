from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        
        self.login_button = page.get_by_role("button", name="כניסה")
        self.forgot_password_link = page.get_by_text("אפשר לאפס כאן")
        self.logo = page.locator("h1, .logo, .brand").first
        self.password_toggle = self.password_input.locator("..").locator("button, svg").first        
    def navigate(self):
        self.logger.info("Opening login page")
        super().navigate("/login")
        
    def login(self, username, password):
        self.logger.info(f"Attempting login for user: {username}")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
"""
LoginPage — Page Object for the SauceDemo login page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    """Page object representing the SauceDemo login page."""

    # ── Locators ─────────────────────────────────────────────────

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, ".error-button")
    LOGIN_LOGO = (By.CSS_SELECTOR, ".login_logo")

    # ── Actions ──────────────────────────────────────────────────

    def open_login_page(self):
        """Navigate to the SauceDemo login page."""
        self.open(Config.BASE_URL)

    def enter_username(self, username: str):
        """Enter username."""
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        """Enter password."""
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click the Login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Perform a complete login."""
        self.open_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Get the error message text."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed."""
        return self.is_displayed(self.ERROR_MESSAGE)

    def is_login_page(self) -> bool:
        """Check if we are on the login page."""
        return self.is_displayed(self.LOGIN_LOGO)

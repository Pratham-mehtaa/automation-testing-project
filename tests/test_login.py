"""
test_login.py — Test cases for SauceDemo login functionality.
Tests all user types to uncover login-related bugs.
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.config import Config


@pytest.mark.login
class TestLogin:
    """Test suite for login functionality across all user types."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.driver = driver

    @pytest.mark.smoke
    def test_login_standard_user(self):
        """TC-LOG-001: Login with standard_user — should succeed."""
        self.login_page.login(Config.Users.STANDARD, Config.PASSWORD)
        assert self.inventory_page.is_on_inventory_page(), (
            "Standard user should be redirected to inventory page"
        )

    @pytest.mark.smoke
    def test_login_locked_out_user(self):
        """TC-LOG-002: Login with locked_out_user — should show error."""
        self.login_page.login(Config.Users.LOCKED_OUT, Config.PASSWORD)
        assert self.login_page.is_error_displayed(), (
            "Locked out user should see an error message"
        )
        error = self.login_page.get_error_message()
        assert "locked out" in error.lower(), (
            f"Error should mention 'locked out', got: {error}"
        )

    @pytest.mark.regression
    def test_login_problem_user(self):
        """TC-LOG-003: Login with problem_user — should succeed (bugs are on other pages)."""
        self.login_page.login(Config.Users.PROBLEM, Config.PASSWORD)
        assert self.inventory_page.is_on_inventory_page(), (
            "Problem user should be able to login and reach inventory page"
        )

    @pytest.mark.regression
    def test_login_performance_glitch_user(self):
        """TC-LOG-004: Login with performance_glitch_user — should succeed but may be slow."""
        self.login_page.login(Config.Users.PERFORMANCE_GLITCH, Config.PASSWORD)
        assert self.inventory_page.is_on_inventory_page(), (
            "Performance glitch user should eventually reach inventory page"
        )

    @pytest.mark.regression
    def test_login_error_user(self):
        """TC-LOG-005: Login with error_user — should succeed (errors appear later)."""
        self.login_page.login(Config.Users.ERROR, Config.PASSWORD)
        assert self.inventory_page.is_on_inventory_page(), (
            "Error user should be able to login"
        )

    @pytest.mark.regression
    def test_login_visual_user(self):
        """TC-LOG-006: Login with visual_user — should succeed."""
        self.login_page.login(Config.Users.VISUAL, Config.PASSWORD)
        assert self.inventory_page.is_on_inventory_page(), (
            "Visual user should be able to login"
        )

    @pytest.mark.smoke
    def test_login_invalid_credentials(self):
        """TC-LOG-007: Login with invalid username/password — should show error."""
        self.login_page.login("invalid_user", "invalid_password")
        assert self.login_page.is_error_displayed(), (
            "Invalid credentials should show an error"
        )
        error = self.login_page.get_error_message()
        assert "do not match" in error.lower() or "username" in error.lower(), (
            f"Error should mention credential mismatch, got: {error}"
        )

    @pytest.mark.regression
    def test_login_empty_username(self):
        """TC-LOG-008: Login with empty username — should show error."""
        self.login_page.login("", Config.PASSWORD)
        assert self.login_page.is_error_displayed(), (
            "Empty username should show an error"
        )
        error = self.login_page.get_error_message()
        assert "username" in error.lower(), (
            f"Error should mention username, got: {error}"
        )

    @pytest.mark.regression
    def test_login_empty_password(self):
        """TC-LOG-009: Login with empty password — should show error."""
        self.login_page.login(Config.Users.STANDARD, "")
        assert self.login_page.is_error_displayed(), (
            "Empty password should show an error"
        )
        error = self.login_page.get_error_message()
        assert "password" in error.lower(), (
            f"Error should mention password, got: {error}"
        )

    @pytest.mark.smoke
    def test_logout(self):
        """TC-LOG-010: Login and then logout — should return to login page."""
        self.login_page.login(Config.Users.STANDARD, Config.PASSWORD)
        assert self.inventory_page.is_on_inventory_page()

        self.inventory_page.logout()
        assert self.login_page.is_login_page(), (
            "After logout, should be back on login page"
        )

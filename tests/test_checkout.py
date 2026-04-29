"""
test_checkout.py — Test cases for SauceDemo checkout flow.
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.config import Config


@pytest.mark.checkout
class TestCheckout:
    """Test suite for the checkout process."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)
        self.driver = driver

    def _login_and_add_item(self, user: str):
        """Login and add backpack to cart."""
        self.login_page.login(user, Config.PASSWORD)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.click_cart()
        self.cart_page.click_checkout()

    @pytest.mark.smoke
    def test_checkout_complete_flow(self):
        """TC-CHK-001: Complete checkout with standard_user."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.fill_checkout_info("John", "Doe", "12345")
        assert self.checkout_page.is_on_checkout_step_two()
        self.checkout_page.click_finish()
        assert self.checkout_page.is_order_complete(), (
            "Order should be completed successfully"
        )

    @pytest.mark.regression
    def test_checkout_empty_first_name(self):
        """TC-CHK-002: Checkout with empty first name — error."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.fill_checkout_info("", "Doe", "12345")
        assert self.checkout_page.is_error_displayed()
        error = self.checkout_page.get_checkout_error()
        assert "first name" in error.lower(), f"Expected first name error, got: {error}"

    @pytest.mark.regression
    def test_checkout_empty_last_name(self):
        """TC-CHK-003: Checkout with empty last name — error."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.fill_checkout_info("John", "", "12345")
        assert self.checkout_page.is_error_displayed()
        error = self.checkout_page.get_checkout_error()
        assert "last name" in error.lower(), f"Expected last name error, got: {error}"

    @pytest.mark.regression
    def test_checkout_empty_postal_code(self):
        """TC-CHK-004: Checkout with empty postal code — error."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.fill_checkout_info("John", "Doe", "")
        assert self.checkout_page.is_error_displayed()
        error = self.checkout_page.get_checkout_error()
        assert "postal" in error.lower() or "zip" in error.lower(), (
            f"Expected postal code error, got: {error}"
        )

    @pytest.mark.regression
    def test_checkout_overview_shows_correct_items(self):
        """TC-CHK-005: Overview should show items that were in cart."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.fill_checkout_info("John", "Doe", "12345")
        items = self.checkout_page.get_overview_item_names()
        assert Config.Products.BACKPACK in items

    @pytest.mark.regression
    def test_checkout_total_calculation(self):
        """TC-CHK-006: Total = subtotal + tax."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.fill_checkout_info("John", "Doe", "12345")
        subtotal = self.checkout_page.get_subtotal_value()
        tax = self.checkout_page.get_tax_value()
        total = self.checkout_page.get_total_value()
        expected = round(subtotal + tax, 2)
        assert total == expected, (
            f"Total (${total}) should equal subtotal (${subtotal}) + tax (${tax}) = ${expected}"
        )

    @pytest.mark.regression
    def test_checkout_cancel_returns_to_cart(self):
        """TC-CHK-007: Cancel on step one returns to cart."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.click_cancel()
        assert "cart" in self.driver.current_url

    @pytest.mark.regression
    def test_checkout_back_home_after_complete(self):
        """TC-CHK-008: Back Home after order returns to inventory."""
        self._login_and_add_item(Config.Users.STANDARD)
        self.checkout_page.fill_checkout_info("John", "Doe", "12345")
        self.checkout_page.click_finish()
        assert self.checkout_page.is_order_complete()
        self.checkout_page.click_back_home()
        assert self.inventory_page.is_on_inventory_page()

    # ── Problem User Checkout ────────────────────────────────────

    @pytest.mark.regression
    def test_problem_user_checkout_info(self):
        """TC-CHK-009: problem_user — checkout form should accept input.
        BUG EXPECTED: Last name field may not work."""
        self._login_and_add_item(Config.Users.PROBLEM)
        self.checkout_page.enter_first_name("John")
        self.checkout_page.enter_last_name("Doe")
        self.checkout_page.enter_postal_code("12345")

        # Verify fields actually contain the typed values
        fn = self.checkout_page.get_attribute(
            self.checkout_page.FIRST_NAME_INPUT, "value"
        )
        ln = self.checkout_page.get_attribute(
            self.checkout_page.LAST_NAME_INPUT, "value"
        )
        pc = self.checkout_page.get_attribute(
            self.checkout_page.POSTAL_CODE_INPUT, "value"
        )
        assert fn == "John", f"BUG: First name is '{fn}' instead of 'John'"
        assert ln == "Doe", f"BUG: Last name is '{ln}' instead of 'Doe'"
        assert pc == "12345", f"BUG: Postal code is '{pc}' instead of '12345'"

    @pytest.mark.regression
    def test_problem_user_complete_checkout(self):
        """TC-CHK-010: problem_user — full checkout flow."""
        self._login_and_add_item(Config.Users.PROBLEM)
        self.checkout_page.fill_checkout_info("John", "Doe", "12345")

        # Check if we made it to step two or got an error
        if self.checkout_page.is_error_displayed():
            error = self.checkout_page.get_checkout_error()
            pytest.fail(f"BUG: problem_user checkout error: {error}")

        self.checkout_page.click_finish()
        assert self.checkout_page.is_order_complete(), (
            "BUG: problem_user checkout did not complete"
        )

    # ── Error User Checkout ──────────────────────────────────────

    @pytest.mark.regression
    def test_error_user_checkout_info(self):
        """TC-CHK-011: error_user — checkout form fields.
        BUG EXPECTED: Last name may not be editable."""
        self._login_and_add_item(Config.Users.ERROR)
        self.checkout_page.enter_first_name("John")
        self.checkout_page.enter_last_name("Doe")
        self.checkout_page.enter_postal_code("12345")

        ln = self.checkout_page.get_attribute(
            self.checkout_page.LAST_NAME_INPUT, "value"
        )
        assert ln == "Doe", f"BUG: error_user Last name is '{ln}' instead of 'Doe'"

    @pytest.mark.regression
    def test_error_user_complete_checkout(self):
        """TC-CHK-012: error_user — full checkout flow."""
        self._login_and_add_item(Config.Users.ERROR)
        self.checkout_page.fill_checkout_info("John", "Doe", "12345")

        if self.checkout_page.is_error_displayed():
            error = self.checkout_page.get_checkout_error()
            pytest.fail(f"BUG: error_user checkout error: {error}")

        self.checkout_page.click_finish()
        assert self.checkout_page.is_order_complete(), (
            "BUG: error_user checkout did not complete"
        )

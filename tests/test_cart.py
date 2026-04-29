"""
test_cart.py — Test cases for SauceDemo shopping cart.
"""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from config.config import Config


@pytest.mark.cart
class TestCart:
    """Test suite for shopping cart functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)
        self.driver = driver

    def _login_as(self, user: str):
        self.login_page.login(user, Config.PASSWORD)

    @pytest.mark.smoke
    def test_add_single_item(self):
        """TC-CRT-001: Add one item — badge shows 1."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.add_backpack_to_cart()
        assert self.inventory_page.get_cart_badge_count() == 1

    @pytest.mark.smoke
    def test_add_multiple_items(self):
        """TC-CRT-002: Add 3 items — badge shows 3."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.add_bolt_tshirt_to_cart()
        assert self.inventory_page.get_cart_badge_count() == 3

    @pytest.mark.smoke
    def test_remove_item_from_inventory(self):
        """TC-CRT-003: Remove item from inventory — badge disappears."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.remove_backpack_from_cart()
        assert not self.inventory_page.is_cart_badge_displayed()

    @pytest.mark.smoke
    def test_cart_page_shows_items(self):
        """TC-CRT-004: Cart page lists added items."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.add_bike_light_to_cart()
        self.inventory_page.click_cart()
        items = self.cart_page.get_cart_item_names()
        assert Config.Products.BACKPACK in items
        assert Config.Products.BIKE_LIGHT in items

    @pytest.mark.regression
    def test_remove_item_from_cart_page(self):
        """TC-CRT-005: Remove item from cart page."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.click_cart()
        self.cart_page.remove_item_by_name("sauce-labs-backpack")
        assert self.cart_page.is_cart_empty()

    @pytest.mark.regression
    def test_continue_shopping(self):
        """TC-CRT-006: Continue Shopping returns to inventory."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.click_cart()
        self.cart_page.click_continue_shopping()
        assert self.inventory_page.is_on_inventory_page()

    @pytest.mark.regression
    def test_cart_persists(self):
        """TC-CRT-007: Cart persists after navigation."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.click_cart()
        self.cart_page.click_continue_shopping()
        self.inventory_page.click_cart()
        items = self.cart_page.get_cart_item_names()
        assert Config.Products.BACKPACK in items

    @pytest.mark.regression
    def test_problem_user_add_to_cart(self):
        """TC-CRT-008: problem_user add to cart. BUG EXPECTED."""
        self._login_as(Config.Users.PROBLEM)
        self.inventory_page.add_backpack_to_cart()
        assert self.inventory_page.get_cart_badge_count() == 1
        self.inventory_page.click_cart()
        items = self.cart_page.get_cart_item_names()
        assert Config.Products.BACKPACK in items, (
            f"BUG: Backpack not in cart. Found: {items}"
        )

    @pytest.mark.regression
    def test_problem_user_remove(self):
        """TC-CRT-009: problem_user remove from cart. BUG EXPECTED."""
        self._login_as(Config.Users.PROBLEM)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.click_cart()
        initial = self.cart_page.get_cart_item_count()
        self.cart_page.remove_item_by_index(0)
        assert self.cart_page.get_cart_item_count() < initial, (
            "BUG: Item not removed for problem_user"
        )

    @pytest.mark.regression
    def test_error_user_add_to_cart(self):
        """TC-CRT-010: error_user add to cart. BUG EXPECTED."""
        self._login_as(Config.Users.ERROR)
        self.inventory_page.add_backpack_to_cart()
        assert self.inventory_page.get_cart_badge_count() == 1

    @pytest.mark.regression
    def test_error_user_remove(self):
        """TC-CRT-011: error_user remove from cart."""
        self._login_as(Config.Users.ERROR)
        self.inventory_page.add_backpack_to_cart()
        self.inventory_page.click_cart()
        self.cart_page.remove_item_by_index(0)
        assert self.cart_page.is_cart_empty(), "BUG: error_user cart not empty"

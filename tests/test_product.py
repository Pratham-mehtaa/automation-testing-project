"""
test_product.py — Test cases for SauceDemo product/inventory page.
Tests product display, images, sorting, and detail pages across user types.
"""
import time
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from config.config import Config


@pytest.mark.product
class TestProduct:
    """Test suite for product browsing and display."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.product_page = ProductPage(driver)
        self.driver = driver

    def _login_as(self, user: str):
        """Helper to login with a specific user type."""
        self.login_page.login(user, Config.PASSWORD)

    # ── Standard User Tests ──────────────────────────────────────

    @pytest.mark.smoke
    def test_inventory_displays_6_products(self):
        """TC-PRD-001: Inventory page should display exactly 6 products."""
        self._login_as(Config.Users.STANDARD)
        count = self.inventory_page.get_product_count()
        assert count == 6, f"Expected 6 products, got {count}"

    @pytest.mark.smoke
    def test_product_names_displayed(self):
        """TC-PRD-002: All product names should be non-empty."""
        self._login_as(Config.Users.STANDARD)
        names = self.inventory_page.get_product_names()
        assert len(names) == 6, f"Expected 6 names, got {len(names)}"
        for name in names:
            assert name.strip() != "", f"Product name should not be empty"

    @pytest.mark.smoke
    def test_product_prices_displayed(self):
        """TC-PRD-003: All product prices should contain '$' and be valid."""
        self._login_as(Config.Users.STANDARD)
        prices = self.inventory_page.get_product_prices()
        for price in prices:
            assert "$" in price, f"Price should contain '$', got: {price}"
            numeric = float(price.replace("$", ""))
            assert numeric > 0, f"Price should be positive, got: {numeric}"

    @pytest.mark.smoke
    def test_product_images_loaded(self):
        """TC-PRD-004: All product images should load correctly (standard_user)."""
        self._login_as(Config.Users.STANDARD)
        images = self.inventory_page.get_product_images_src()
        for img_src in images:
            assert img_src is not None, "Image src should not be None"
            assert "WithGarbageOnItToBreakStuff" not in img_src, (
                f"Image appears broken: {img_src}"
            )
            assert img_src.strip() != "", "Image src should not be empty"

    @pytest.mark.regression
    def test_sort_name_a_to_z(self):
        """TC-PRD-005: Sort products A-Z — names should be in alphabetical order."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.sort_name_az()
        names = self.inventory_page.get_product_names()
        assert names == sorted(names), (
            f"Products should be sorted A-Z. Got: {names}"
        )

    @pytest.mark.regression
    def test_sort_name_z_to_a(self):
        """TC-PRD-006: Sort products Z-A — names should be in reverse alphabetical order."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.sort_name_za()
        names = self.inventory_page.get_product_names()
        assert names == sorted(names, reverse=True), (
            f"Products should be sorted Z-A. Got: {names}"
        )

    @pytest.mark.regression
    def test_sort_price_low_to_high(self):
        """TC-PRD-007: Sort by price low-to-high — prices should be ascending."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.sort_price_low_to_high()
        prices = self.inventory_page.get_product_prices_float()
        assert prices == sorted(prices), (
            f"Prices should be ascending. Got: {prices}"
        )

    @pytest.mark.regression
    def test_sort_price_high_to_low(self):
        """TC-PRD-008: Sort by price high-to-low — prices should be descending."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.sort_price_high_to_low()
        prices = self.inventory_page.get_product_prices_float()
        assert prices == sorted(prices, reverse=True), (
            f"Prices should be descending. Got: {prices}"
        )

    @pytest.mark.smoke
    def test_click_product_opens_detail(self):
        """TC-PRD-009: Clicking a product should open the detail page."""
        self._login_as(Config.Users.STANDARD)
        expected_name = self.inventory_page.get_product_names()[0]
        self.inventory_page.click_product_by_index(0)
        actual_name = self.product_page.get_product_name()
        assert actual_name == expected_name, (
            f"Product detail should show '{expected_name}', got '{actual_name}'"
        )

    @pytest.mark.regression
    def test_product_detail_has_price_and_description(self):
        """TC-PRD-010: Product detail page should show price and description."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.click_product_by_index(0)
        price = self.product_page.get_product_price()
        desc = self.product_page.get_product_description()
        assert "$" in price, f"Detail page should show price, got: {price}"
        assert len(desc) > 10, f"Description should be meaningful, got: {desc}"

    @pytest.mark.regression
    def test_back_button_returns_to_inventory(self):
        """TC-PRD-011: Back button on detail page should return to inventory."""
        self._login_as(Config.Users.STANDARD)
        self.inventory_page.click_product_by_index(0)
        self.product_page.click_back()
        assert self.inventory_page.is_on_inventory_page(), (
            "Back button should return to inventory page"
        )

    # ── Problem User Tests ───────────────────────────────────────

    @pytest.mark.regression
    def test_problem_user_images_broken(self):
        """TC-PRD-012: problem_user — product images should load correctly.
        BUG EXPECTED: problem_user sees broken/wrong images."""
        self._login_as(Config.Users.PROBLEM)
        images = self.inventory_page.get_product_images_src()

        # All images should be unique (different products = different images)
        unique_images = set(images)
        assert len(unique_images) > 1, (
            f"BUG: All product images are the same! Got {len(unique_images)} "
            f"unique image(s) out of {len(images)}: {images[0] if images else 'none'}"
        )

    @pytest.mark.regression
    def test_problem_user_sort_name_az(self):
        """TC-PRD-013: problem_user — sort A-Z should work correctly.
        BUG EXPECTED: Sorting may not work for problem_user."""
        self._login_as(Config.Users.PROBLEM)
        self.inventory_page.sort_name_az()
        names = self.inventory_page.get_product_names()
        assert names == sorted(names), (
            f"BUG: Products not sorted A-Z for problem_user. Got: {names}"
        )

    @pytest.mark.regression
    def test_problem_user_sort_name_za(self):
        """TC-PRD-014: problem_user — sort Z-A should work correctly."""
        self._login_as(Config.Users.PROBLEM)
        self.inventory_page.sort_name_za()
        names = self.inventory_page.get_product_names()
        assert names == sorted(names, reverse=True), (
            f"BUG: Products not sorted Z-A for problem_user. Got: {names}"
        )

    @pytest.mark.regression
    def test_problem_user_sort_price_lohi(self):
        """TC-PRD-015: problem_user — sort price low-to-high should work."""
        self._login_as(Config.Users.PROBLEM)
        self.inventory_page.sort_price_low_to_high()
        prices = self.inventory_page.get_product_prices_float()
        assert prices == sorted(prices), (
            f"BUG: Prices not sorted low-to-high for problem_user. Got: {prices}"
        )

    @pytest.mark.regression
    def test_problem_user_sort_price_hilo(self):
        """TC-PRD-016: problem_user — sort price high-to-low should work."""
        self._login_as(Config.Users.PROBLEM)
        self.inventory_page.sort_price_high_to_low()
        prices = self.inventory_page.get_product_prices_float()
        assert prices == sorted(prices, reverse=True), (
            f"BUG: Prices not sorted high-to-low for problem_user. Got: {prices}"
        )

    @pytest.mark.regression
    def test_problem_user_product_detail_image(self):
        """TC-PRD-017: problem_user — product detail image should be correct."""
        self._login_as(Config.Users.PROBLEM)
        self.inventory_page.click_product_by_index(0)
        img_src = self.product_page.get_product_image_src()
        assert "WithGarbageOnItToBreakStuff" not in img_src, (
            f"BUG: Product detail has broken image: {img_src}"
        )

    # ── Error User Tests ─────────────────────────────────────────

    @pytest.mark.regression
    def test_error_user_products_display(self):
        """TC-PRD-018: error_user — products page should display correctly."""
        self._login_as(Config.Users.ERROR)
        count = self.inventory_page.get_product_count()
        assert count == 6, f"Error user should see 6 products, got {count}"

    @pytest.mark.regression
    def test_error_user_sort_name_za(self):
        """TC-PRD-019: error_user — sorting Z-A should work."""
        self._login_as(Config.Users.ERROR)
        self.inventory_page.sort_name_za()
        names = self.inventory_page.get_product_names()
        assert names == sorted(names, reverse=True), (
            f"BUG: Sort Z-A broken for error_user. Got: {names}"
        )

    @pytest.mark.regression
    def test_error_user_sort_price_lohi(self):
        """TC-PRD-020: error_user — sorting price low-to-high should work."""
        self._login_as(Config.Users.ERROR)
        self.inventory_page.sort_price_low_to_high()
        prices = self.inventory_page.get_product_prices_float()
        assert prices == sorted(prices), (
            f"BUG: Sort price low-high broken for error_user. Got: {prices}"
        )

    @pytest.mark.regression
    def test_error_user_sort_price_hilo(self):
        """TC-PRD-021: error_user — sorting price high-to-low should work."""
        self._login_as(Config.Users.ERROR)
        self.inventory_page.sort_price_high_to_low()
        prices = self.inventory_page.get_product_prices_float()
        assert prices == sorted(prices, reverse=True), (
            f"BUG: Sort price high-low broken for error_user. Got: {prices}"
        )

"""
ProductPage — Page Object for the SauceDemo product detail page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object representing a SauceDemo product detail page."""

    # ── Locators ─────────────────────────────────────────────────

    BACK_BUTTON = (By.ID, "back-to-products")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".inventory_details_name")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".inventory_details_desc")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_details_price")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".inventory_details_img")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")

    # Cart
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    # ── Actions ──────────────────────────────────────────────────

    def get_product_name(self) -> str:
        """Get the product name."""
        return self.get_text(self.PRODUCT_NAME)

    def get_product_description(self) -> str:
        """Get the product description."""
        return self.get_text(self.PRODUCT_DESCRIPTION)

    def get_product_price(self) -> str:
        """Get the product price."""
        return self.get_text(self.PRODUCT_PRICE)

    def get_product_image_src(self) -> str:
        """Get the product image source URL."""
        return self.get_attribute(self.PRODUCT_IMAGE, "src")

    def add_to_cart(self):
        """Click Add to Cart button."""
        self.click(self.ADD_TO_CART_BUTTON)

    def get_add_to_cart_button_text(self) -> str:
        """Get the text of the add/remove button."""
        return self.get_text(self.ADD_TO_CART_BUTTON)

    def click_back(self):
        """Click Back to products."""
        self.click(self.BACK_BUTTON)

    def click_cart(self):
        """Navigate to cart."""
        self.click(self.CART_LINK)

    def get_cart_badge_count(self) -> int:
        """Get cart badge count."""
        try:
            return int(self.get_text(self.CART_BADGE))
        except Exception:
            return 0

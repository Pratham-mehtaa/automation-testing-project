"""
CartPage — Page Object for the SauceDemo shopping cart page.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class CartPage(BasePage):
    """Page object representing the SauceDemo cart page."""

    # ── Locators ─────────────────────────────────────────────────

    CART_LIST = (By.CSS_SELECTOR, ".cart_list")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ITEM_QUANTITIES = (By.CSS_SELECTOR, ".cart_quantity")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button.cart_button")

    # Action buttons
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    # Cart badge
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    # ── Actions ──────────────────────────────────────────────────

    def open_cart(self):
        """Navigate directly to the cart page."""
        self.open_page(Config.URLs.CART)

    def get_cart_item_names(self) -> list[str]:
        """Get names of all items in the cart."""
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_cart_item_prices(self) -> list[str]:
        """Get prices of all items in the cart."""
        elements = self.find_elements(self.ITEM_PRICES)
        return [el.text for el in elements]

    def get_cart_item_count(self) -> int:
        """Get the number of items in the cart."""
        return len(self.find_elements(self.CART_ITEMS))

    def remove_item_by_index(self, index: int = 0):
        """Remove an item from cart by index."""
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        if index < len(buttons):
            buttons[index].click()

    def remove_item_by_name(self, product_name: str):
        """Remove a specific product from cart."""
        # Build the remove button ID from product name
        btn_id = "remove-" + product_name.lower().replace(" ", "-")
        locator = (By.ID, btn_id)
        self.click(locator)

    def click_checkout(self):
        """Click the Checkout button."""
        self.click(self.CHECKOUT_BUTTON)

    def click_continue_shopping(self):
        """Click Continue Shopping."""
        self.click(self.CONTINUE_SHOPPING)

    def is_cart_empty(self) -> bool:
        """Check if the cart is empty."""
        return self.get_cart_item_count() == 0

    def get_cart_badge_count(self) -> int:
        """Get cart badge count."""
        try:
            return int(self.get_text(self.CART_BADGE))
        except Exception:
            return 0

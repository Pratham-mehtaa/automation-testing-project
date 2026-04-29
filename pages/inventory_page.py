"""
InventoryPage — Page Object for the SauceDemo products/inventory page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from config.config import Config


class InventoryPage(BasePage):
    """Page object representing the SauceDemo inventory (products) page."""

    # ── Locators ─────────────────────────────────────────────────

    # Header
    APP_LOGO = (By.CSS_SELECTOR, ".app_logo")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    # Sidebar menu
    MENU_CLOSE = (By.ID, "react-burger-cross-btn")
    MENU_ALL_ITEMS = (By.ID, "inventory_sidebar_link")
    MENU_ABOUT = (By.ID, "about_sidebar_link")
    MENU_LOGOUT = (By.ID, "logout_sidebar_link")
    MENU_RESET = (By.ID, "reset_sidebar_link")

    # Product listing
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_DESCRIPTIONS = (By.CSS_SELECTOR, ".inventory_item_desc")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ITEM_IMAGES = (By.CSS_SELECTOR, ".inventory_item_img img")

    # Sort
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".product_sort_container")

    # Add/Remove buttons
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")

    # Specific product add-to-cart buttons
    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    ADD_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    REMOVE_BIKE_LIGHT = (By.ID, "remove-sauce-labs-bike-light")
    ADD_BOLT_TSHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    REMOVE_BOLT_TSHIRT = (By.ID, "remove-sauce-labs-bolt-t-shirt")
    ADD_FLEECE_JACKET = (By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    REMOVE_FLEECE_JACKET = (By.ID, "remove-sauce-labs-fleece-jacket")
    ADD_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")
    REMOVE_ONESIE = (By.ID, "remove-sauce-labs-onesie")
    ADD_RED_TSHIRT = (By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)")
    REMOVE_RED_TSHIRT = (By.ID, "remove-test.allthethings()-t-shirt-(red)")

    # ── Actions ──────────────────────────────────────────────────

    def open_inventory_page(self):
        """Navigate to the inventory page."""
        self.open_page(Config.URLs.INVENTORY)

    def is_on_inventory_page(self) -> bool:
        """Check if we are on the inventory page."""
        return Config.URLs.INVENTORY in self.get_current_url()

    def get_product_names(self) -> list[str]:
        """Get all product names displayed."""
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_product_prices(self) -> list[str]:
        """Get all product prices displayed."""
        elements = self.find_elements(self.ITEM_PRICES)
        return [el.text for el in elements]

    def get_product_prices_float(self) -> list[float]:
        """Get all product prices as floats."""
        prices = self.get_product_prices()
        return [float(p.replace("$", "")) for p in prices]

    def get_product_images_src(self) -> list[str]:
        """Get all product image src attributes."""
        elements = self.find_elements(self.ITEM_IMAGES)
        return [el.get_attribute("src") for el in elements]

    def get_product_count(self) -> int:
        """Get the number of products displayed."""
        return len(self.find_elements(self.INVENTORY_ITEMS))

    def click_product_name(self, name: str):
        """Click a product by its name to view details."""
        locator = (By.XPATH, f"//div[@class='inventory_item_name ' and text()='{name}']")
        self.click(locator)

    def click_product_by_index(self, index: int = 0):
        """Click a product name by its index."""
        names = self.find_elements(self.ITEM_NAMES)
        if index < len(names):
            names[index].click()

    # ── Cart Actions ─────────────────────────────────────────────

    def add_backpack_to_cart(self):
        """Add Sauce Labs Backpack to cart."""
        self.click(self.ADD_BACKPACK)

    def remove_backpack_from_cart(self):
        """Remove Sauce Labs Backpack from cart."""
        self.click(self.REMOVE_BACKPACK)

    def add_bike_light_to_cart(self):
        """Add Sauce Labs Bike Light to cart."""
        self.click(self.ADD_BIKE_LIGHT)

    def add_bolt_tshirt_to_cart(self):
        """Add Sauce Labs Bolt T-Shirt to cart."""
        self.click(self.ADD_BOLT_TSHIRT)

    def add_fleece_jacket_to_cart(self):
        """Add Sauce Labs Fleece Jacket to cart."""
        self.click(self.ADD_FLEECE_JACKET)

    def add_onesie_to_cart(self):
        """Add Sauce Labs Onesie to cart."""
        self.click(self.ADD_ONESIE)

    def add_product_to_cart_by_index(self, index: int = 0):
        """Click the Add to Cart button by index."""
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(buttons):
            buttons[index].click()

    def get_cart_badge_count(self) -> int:
        """Get the number shown on the cart badge."""
        try:
            text = self.get_text(self.CART_BADGE)
            return int(text)
        except Exception:
            return 0

    def click_cart(self):
        """Click the shopping cart icon."""
        self.click(self.CART_LINK)

    def is_cart_badge_displayed(self) -> bool:
        """Check if the cart badge is displayed."""
        return self.is_displayed(self.CART_BADGE)

    # ── Sort Actions ─────────────────────────────────────────────

    def sort_by(self, option: str):
        """
        Sort products by option.
        Options: 'az', 'za', 'lohi', 'hilo'
        """
        dropdown = Select(self.find_element(self.SORT_DROPDOWN))
        dropdown.select_by_value(option)

    def sort_name_az(self):
        """Sort products A to Z."""
        self.sort_by("az")

    def sort_name_za(self):
        """Sort products Z to A."""
        self.sort_by("za")

    def sort_price_low_to_high(self):
        """Sort products by price low to high."""
        self.sort_by("lohi")

    def sort_price_high_to_low(self):
        """Sort products by price high to low."""
        self.sort_by("hilo")

    def get_active_sort_option(self) -> str:
        """Get the currently active sort option."""
        dropdown = Select(self.find_element(self.SORT_DROPDOWN))
        return dropdown.first_selected_option.get_attribute("value")

    # ── Menu Actions ─────────────────────────────────────────────

    def open_menu(self):
        """Open the burger menu."""
        self.click(self.BURGER_MENU)

    def logout(self):
        """Logout via the burger menu."""
        self.open_menu()
        self.click(self.MENU_LOGOUT)

    def reset_app_state(self):
        """Reset app state via menu."""
        self.open_menu()
        self.click(self.MENU_RESET)

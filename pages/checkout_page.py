"""
CheckoutPage — Page Object for the SauceDemo checkout flow.
Covers: checkout-step-one, checkout-step-two, checkout-complete.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import Config


class CheckoutPage(BasePage):
    """Page object representing the SauceDemo checkout pages."""

    # ── Step One: Your Information ────────────────────────────────

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    # ── Step Two: Overview ───────────────────────────────────────

    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    SUBTOTAL_LABEL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    TAX_LABEL = (By.CSS_SELECTOR, ".summary_tax_label")
    TOTAL_LABEL = (By.CSS_SELECTOR, ".summary_total_label")
    PAYMENT_INFO = (By.CSS_SELECTOR, ".summary_value_label")
    FINISH_BUTTON = (By.ID, "finish")

    # ── Complete ─────────────────────────────────────────────────

    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")
    PONY_EXPRESS_IMAGE = (By.CSS_SELECTOR, ".pony_express")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    # ── Actions: Step One ────────────────────────────────────────

    def enter_first_name(self, name: str):
        """Enter first name."""
        self.type_text(self.FIRST_NAME_INPUT, name)

    def enter_last_name(self, name: str):
        """Enter last name."""
        self.type_text(self.LAST_NAME_INPUT, name)

    def enter_postal_code(self, code: str):
        """Enter postal/zip code."""
        self.type_text(self.POSTAL_CODE_INPUT, code)

    def click_continue(self):
        """Click Continue to go to step two."""
        self.click(self.CONTINUE_BUTTON)

    def click_cancel(self):
        """Click Cancel."""
        self.click(self.CANCEL_BUTTON)

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """Fill in all checkout information and continue."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        self.click_continue()

    def get_checkout_error(self) -> str:
        """Get the checkout error message."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Check if an error is displayed."""
        return self.is_displayed(self.ERROR_MESSAGE)

    # ── Actions: Step Two (Overview) ─────────────────────────────

    def get_overview_item_names(self) -> list[str]:
        """Get product names on the overview."""
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text for el in elements]

    def get_subtotal(self) -> str:
        """Get the subtotal text."""
        return self.get_text(self.SUBTOTAL_LABEL)

    def get_tax(self) -> str:
        """Get the tax text."""
        return self.get_text(self.TAX_LABEL)

    def get_total(self) -> str:
        """Get the total text."""
        return self.get_text(self.TOTAL_LABEL)

    def get_subtotal_value(self) -> float:
        """Get the subtotal as a float."""
        text = self.get_subtotal()  # e.g. "Item total: $29.99"
        return float(text.split("$")[1])

    def get_tax_value(self) -> float:
        """Get the tax as a float."""
        text = self.get_tax()  # e.g. "Tax: $2.40"
        return float(text.split("$")[1])

    def get_total_value(self) -> float:
        """Get the total as a float."""
        text = self.get_total()  # e.g. "Total: $32.39"
        return float(text.split("$")[1])

    def click_finish(self):
        """Click Finish to complete the order."""
        self.click(self.FINISH_BUTTON)

    # ── Actions: Complete ────────────────────────────────────────

    def get_complete_header(self) -> str:
        """Get the order complete header text."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """Get the order complete description text."""
        return self.get_text(self.COMPLETE_TEXT)

    def is_order_complete(self) -> bool:
        """Check if the order was completed successfully."""
        try:
            header = self.get_complete_header()
            return "thank you" in header.lower()
        except Exception:
            return False

    def click_back_home(self):
        """Click Back Home after order completion."""
        self.click(self.BACK_HOME_BUTTON)

    def is_on_checkout_step_one(self) -> bool:
        """Check if on checkout step one."""
        return "checkout-step-one" in self.get_current_url()

    def is_on_checkout_step_two(self) -> bool:
        """Check if on checkout step two."""
        return "checkout-step-two" in self.get_current_url()

    def is_on_checkout_complete(self) -> bool:
        """Check if on checkout complete page."""
        return "checkout-complete" in self.get_current_url()

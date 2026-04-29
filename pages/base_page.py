"""
BasePage — Parent class for all Page Objects.
Provides common Selenium interactions with built-in waits and error handling.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from config.config import Config


class BasePage:
    """Base class providing common web interaction methods for all page objects."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            Config.EXPLICIT_WAIT,
            ignored_exceptions=[StaleElementReferenceException],
        )

    # ── Navigation ───────────────────────────────────────────────

    def open(self, url: str):
        """Navigate to a URL."""
        self.driver.get(url)

    def open_page(self, path: str):
        """Navigate to a page relative to the base URL."""
        self.driver.get(Config.BASE_URL + path)

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    def go_back(self):
        """Navigate back in browser history."""
        self.driver.back()

    def refresh(self):
        """Refresh the current page."""
        self.driver.refresh()

    # ── Element Finding ──────────────────────────────────────────

    def find_element(self, locator: tuple) -> WebElement:
        """Find a single element with explicit wait."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: tuple) -> list[WebElement]:
        """Find multiple elements."""
        return self.driver.find_elements(*locator)

    def find_visible_element(self, locator: tuple) -> WebElement:
        """Wait for an element to be visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable_element(self, locator: tuple) -> WebElement:
        """Wait for an element to be clickable and return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    # ── Interactions ─────────────────────────────────────────────

    def click(self, locator: tuple):
        """Wait for element to be clickable, then click it."""
        self.find_clickable_element(locator).click()

    def type_text(self, locator: tuple, text: str):
        """Clear a field and type text into it."""
        element = self.find_visible_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Get the visible text of an element."""
        return self.find_visible_element(locator).text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Get an attribute value from an element."""
        return self.find_element(locator).get_attribute(attribute)

    def select_by_visible_text(self, locator: tuple, text: str):
        """Select an option from a dropdown by visible text."""
        dropdown = Select(self.find_element(locator))
        dropdown.select_by_visible_text(text)

    def select_by_value(self, locator: tuple, value: str):
        """Select an option from a dropdown by value."""
        dropdown = Select(self.find_element(locator))
        dropdown.select_by_value(value)

    def select_by_index(self, locator: tuple, index: int):
        """Select an option from a dropdown by index."""
        dropdown = Select(self.find_element(locator))
        dropdown.select_by_index(index)

    # ── State Checks ─────────────────────────────────────────────

    def is_displayed(self, locator: tuple) -> bool:
        """Check if an element is displayed on the page."""
        try:
            return self.find_element(locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_enabled(self, locator: tuple) -> bool:
        """Check if an element is enabled."""
        try:
            return self.find_element(locator).is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_selected(self, locator: tuple) -> bool:
        """Check if a checkbox/radio button is selected."""
        try:
            return self.find_element(locator).is_selected()
        except (TimeoutException, NoSuchElementException):
            return False

    # ── Waits ────────────────────────────────────────────────────

    def wait_for_url_contains(self, text: str):
        """Wait until the URL contains the specified text."""
        self.wait.until(EC.url_contains(text))

    def wait_for_title_contains(self, text: str):
        """Wait until the page title contains the specified text."""
        self.wait.until(EC.title_contains(text))

    def wait_for_element_invisible(self, locator: tuple):
        """Wait for an element to become invisible."""
        self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_alert(self):
        """Wait for a JavaScript alert and return it."""
        return self.wait.until(EC.alert_is_present())

    # ── JavaScript Helpers ───────────────────────────────────────

    def scroll_to_element(self, locator: tuple):
        """Scroll an element into view."""
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element,
        )

    def scroll_to_top(self):
        """Scroll to the top of the page."""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page."""
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def js_click(self, locator: tuple):
        """Click an element using JavaScript (for stubborn elements)."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    # ── Screenshots ──────────────────────────────────────────────

    def take_screenshot(self, filename: str):
        """Take a screenshot and save it."""
        self.driver.save_screenshot(filename)

"""
Configuration settings for the SauceDemo automation tests.
"""


class Config:
    """Central configuration for the test framework."""

    # Base URL
    BASE_URL = "https://www.saucedemo.com/"

    # Timeouts (seconds)
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    PAGE_LOAD_TIMEOUT = 30

    # Browser settings
    BROWSER = "chrome"
    HEADLESS = False  # SauceDemo works fine in headed mode

    # Test user credentials
    # SauceDemo provides multiple user types to test different behaviors
    class Users:
        STANDARD = "standard_user"
        LOCKED_OUT = "locked_out_user"
        PROBLEM = "problem_user"
        PERFORMANCE_GLITCH = "performance_glitch_user"
        ERROR = "error_user"
        VISUAL = "visual_user"

    PASSWORD = "secret_sauce"

    # Page paths (relative to BASE_URL)
    class URLs:
        LOGIN = ""
        INVENTORY = "inventory.html"
        CART = "cart.html"
        CHECKOUT_STEP_ONE = "checkout-step-one.html"
        CHECKOUT_STEP_TWO = "checkout-step-two.html"
        CHECKOUT_COMPLETE = "checkout-complete.html"

    # Known products on SauceDemo
    class Products:
        BACKPACK = "Sauce Labs Backpack"
        BIKE_LIGHT = "Sauce Labs Bike Light"
        BOLT_TSHIRT = "Sauce Labs Bolt T-Shirt"
        FLEECE_JACKET = "Sauce Labs Fleece Jacket"
        ONESIE = "Sauce Labs Onesie"
        TSHIRT_RED = "Test.allTheThings() T-Shirt (Red)"

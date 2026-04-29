"""
pytest conftest.py — Shared fixtures and hooks for the test suite.
Configured for www.saucedemo.com (no Cloudflare, standard Selenium works fine).
"""
import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config


def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--browser",
        action="store",
        default=Config.BROWSER,
        help="Browser to run tests on: chrome or firefox",
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed (visible) mode",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Set up and tear down the WebDriver instance for each test.

    Yields:
        WebDriver: A configured browser driver instance.
    """
    browser = request.config.getoption("--browser").lower()
    headed = request.config.getoption("--headed")
    headless = not headed and Config.HEADLESS

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = ChromeService(ChromeDriverManager().install())
        _driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        service = FirefoxService(GeckoDriverManager().install())
        _driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Configure timeouts
    _driver.implicitly_wait(Config.IMPLICIT_WAIT)
    _driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    _driver.maximize_window()

    yield _driver

    # Teardown
    _driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to take a screenshot on test failure.
    Screenshots are saved to reports/screenshots/.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_dir = os.path.join(
                os.path.dirname(__file__), "reports", "screenshots"
            )
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            filename = f"FAIL_{test_name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            try:
                driver.save_screenshot(filepath)
                print(f"\n📸 Screenshot saved: {filepath}")
            except Exception as e:
                print(f"\n⚠️ Failed to capture screenshot: {e}")

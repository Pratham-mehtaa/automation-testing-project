"""
Utility helpers — Random data generation, screenshot helpers, and common utilities.
"""
import os
import string
import random
from datetime import datetime
from faker import Faker

fake = Faker()


def generate_random_email() -> str:
    """Generate a unique random email address."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = "".join(random.choices(string.ascii_lowercase, k=5))
    return f"test_{random_str}_{timestamp}@testmail.com"


def generate_random_string(length: int = 8) -> str:
    """Generate a random alphanumeric string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_phone() -> str:
    """Generate a random phone number."""
    return fake.phone_number()


def generate_random_name() -> dict:
    """Generate random first and last names."""
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }


def generate_random_address() -> dict:
    """Generate a random address for checkout forms."""
    return {
        "address_1": fake.street_address(),
        "address_2": fake.secondary_address(),
        "city": fake.city(),
        "postcode": fake.postcode(),
        "country": "United States",
        "state": "California",
    }


def generate_test_user() -> dict:
    """Generate a complete test user with all registration fields."""
    name = generate_random_name()
    return {
        "first_name": name["first_name"],
        "last_name": name["last_name"],
        "email": generate_random_email(),
        "password": "Test@" + generate_random_string(6),
    }


def ensure_directory(path: str):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)


def save_screenshot(driver, name: str, directory: str = "reports/screenshots"):
    """
    Save a screenshot with a timestamp.

    Args:
        driver: WebDriver instance
        name: Descriptive name for the screenshot
        directory: Directory to save screenshots in
    """
    ensure_directory(directory)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(directory, filename)
    driver.save_screenshot(filepath)
    return filepath

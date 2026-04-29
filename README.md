# 🛒 OpenCart Demo — Selenium Automation Testing

Automated test suite for [demo.opencart.com](https://demo.opencart.com/) built with **Python + Selenium + pytest** using the **Page Object Model (POM)** design pattern.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Running Tests](#-running-tests)
- [Test Coverage](#-test-coverage)
- [Reports & Screenshots](#-reports--screenshots)
- [Configuration](#-configuration)

---

## ✨ Features

- **Page Object Model (POM)** — Clean separation of test logic from page interactions
- **21 test cases** covering 6 core e-commerce modules
- **Automatic screenshot capture** on test failure
- **HTML test reports** via `pytest-html`
- **Random test data generation** using `Faker`
- **Headless & headed modes** — run with or without a visible browser
- **Custom pytest markers** for selective test execution (`smoke`, `regression`, etc.)
- **Chrome & Firefox support** via `webdriver-manager`

---

## 📁 Project Structure

```
AT Proj/
├── conftest.py                  # pytest fixtures (driver setup/teardown)
├── pytest.ini                   # pytest configuration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── config/
│   └── config.py                # Base URL, credentials, timeouts
│
├── pages/                       # Page Object Model classes
│   ├── base_page.py             # Common methods (click, type, wait)
│   ├── home_page.py             # Homepage
│   ├── login_page.py            # Login page
│   ├── register_page.py         # Registration page
│   ├── search_results_page.py   # Search results
│   ├── product_page.py          # Product detail page
│   ├── cart_page.py             # Shopping cart
│   └── checkout_page.py         # Checkout flow
│
├── tests/                       # Test modules
│   ├── test_registration.py     # Account registration tests (4 tests)
│   ├── test_login.py            # Login/logout tests (4 tests)
│   ├── test_search.py           # Search functionality tests (4 tests)
│   ├── test_product.py          # Product browsing tests (3 tests)
│   ├── test_cart.py             # Shopping cart tests (4 tests)
│   └── test_checkout.py         # Checkout flow tests (2 tests)
│
├── utils/
│   └── helpers.py               # Random data generators, screenshots
│
└── reports/                     # Generated after running tests
    └── screenshots/             # Failure screenshots
```

---

## 🚀 Setup & Installation

### Prerequisites

- **Python 3.9+** installed
- **Google Chrome** browser (or Firefox)
- **pip** package manager

### Installation

```bash
# 1. Navigate to the project directory
cd "AT Proj"

# 2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run with HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run Specific Test Module
```bash
pytest tests/test_login.py
pytest tests/test_search.py
pytest tests/test_cart.py
```

### Run by Marker
```bash
# Smoke tests only (critical path)
pytest -m smoke

# Regression tests
pytest -m regression

# Specific module markers
pytest -m login
pytest -m cart
pytest -m checkout
```

### Run in Headed Mode (Visible Browser)
```bash
pytest --headed
```

### Run with Firefox
```bash
pytest --browser firefox
```

### Run a Single Test
```bash
pytest tests/test_search.py::TestSearch::test_search_valid_product
```

---

## 📊 Test Coverage

| Module | Tests | Markers |
|--------|-------|---------|
| **Registration** | 4 | `registration`, `smoke`, `regression` |
| **Login/Logout** | 4 | `login`, `smoke`, `regression` |
| **Search** | 4 | `search`, `smoke`, `regression` |
| **Product** | 3 | `product`, `smoke`, `regression` |
| **Cart** | 4 | `cart`, `smoke`, `regression` |
| **Checkout** | 2 | `checkout`, `regression` |
| **Total** | **21** | |

---

## 📄 Reports & Screenshots

- **HTML Report**: Generated at `reports/report.html` when using `--html` flag
- **Failure Screenshots**: Automatically captured in `reports/screenshots/` when a test fails
- **Console Output**: Verbose output with `-v` flag (enabled by default in `pytest.ini`)

---

## ⚙️ Configuration

All configuration is centralized in `config/config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `BASE_URL` | `https://demo.opencart.com/` | Target website |
| `BROWSER` | `chrome` | Browser to use |
| `HEADLESS` | `True` | Run without visible browser |
| `IMPLICIT_WAIT` | `10` | Implicit wait timeout (seconds) |
| `EXPLICIT_WAIT` | `15` | Explicit wait timeout (seconds) |
| `PAGE_LOAD_TIMEOUT` | `30` | Page load timeout (seconds) |

---

## 📝 Notes

- The demo site at `demo.opencart.com` resets its database periodically, so test data (accounts, orders) may be cleaned up.
- Registration tests create fresh accounts with random data to avoid conflicts.
- Login tests use a `registered_user` fixture that creates a fresh account before each login test.

---

## 🛠 Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.9+ | Programming language |
| Selenium | 4.20+ | Browser automation |
| pytest | 8.0+ | Test framework |
| pytest-html | 4.1+ | HTML report generation |
| webdriver-manager | 4.0+ | Automatic driver management |
| Faker | 24.0+ | Random test data generation |

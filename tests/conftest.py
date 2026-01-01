import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.order_page import OrderPage
from pages.overview_page import OverviewPage
from pages.product_page import ProductPage
from utils.generator import DataGenerator
from utils.logger import get_logger, log_test_end, log_test_start

load_dotenv()

HEADLESS_VALUE = os.getenv("HEADLESS", "headless").strip().lower()
HEADLESS = HEADLESS_VALUE != "ui"
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")


def _get_chromedriver_path() -> str:
    """Return path to ChromeDriver, downloading via webdriver-manager if needed."""
    if os.path.exists(CHROMEDRIVER_PATH):
        return CHROMEDRIVER_PATH
    return ChromeDriverManager().install()


@pytest.fixture(scope="session", autouse=True)
def preload_chromedriver():
    """Warm up ChromeDriver cache before running tests."""
    _get_chromedriver_path()


def pytest_configure(config):
    """Ensure reports directory exists before test run."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    reports_dir = os.path.join(project_root, "reports")

    # Create reports directory if it doesn't exist
    os.makedirs(reports_dir, exist_ok=True)

    # Ensure the directory is writable
    if not os.access(reports_dir, os.W_OK):
        raise PermissionError(f"Reports directory '{reports_dir}' is not writable")


@pytest.fixture(scope="function", autouse=True)
def log_test_execution(request):
    """Log test execution start and end."""
    logger = get_logger("TestRunner")
    log_test_start(logger, request.node.nodeid)

    yield

    status = "PASSED" if hasattr(request.node, "rep_call") and request.node.rep_call.passed else "COMPLETED"
    log_test_end(logger, request.node.nodeid, status)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for logging."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def driver():
    """Initialize Chrome WebDriver with disabled popups and automation detection."""
    options = Options()

    # Turn off password popups
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", prefs)

    # Chrome args to make tests stable
    base_arguments = [
        "--window-size=1920,1080",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-features=PasswordCheck,PasswordLeakDetection,SafetyTipUI,PasswordManagerOnboarding",
        "--disable-save-password-bubble",
        "--disable-notifications",
        "--disable-infobars",
        "--disable-extensions",
        "--disable-blink-features=AutomationControlled",
        "--no-first-run",
        "--disable-search-engine-choice-screen",
    ]

    # Add headless if needed
    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    for argument in base_arguments:
        options.add_argument(argument)

    # Setup ChromeDriver
    chromedriver_path = _get_chromedriver_path()
    service = ChromeService(executable_path=chromedriver_path)

    # Create driver
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def pages(driver):
    """Initialize all page objects for tests."""
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)
    overview_page = OverviewPage(driver)
    order_page = OrderPage(driver)
    return locals()


@pytest.fixture(scope="function")
def data():
    """Initialize test data generator (Faker)."""
    generator = DataGenerator()
    return locals()

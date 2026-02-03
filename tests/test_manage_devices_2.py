# config.py
BASE_URL = "https://your-app-url.com"
USERNAME = "test_user"
PASSWORD = "secure_password"

# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import config

class LoginPage:
    EMAIL = (By.XPATH, "//input[@id='login-email']")
    PASSWORD = (By.XPATH, "//input[@id='login-input-password']")
    LOGIN_BTN = (By.XPATH, "//button[text()='LOG IN']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open(self):
        self.driver.get(config.BASE_URL)

    def login(self, username, password):
        self.open()
        email_el = self.wait.until(EC.presence_of_element_located(self.EMAIL))
        email_el.clear()
        email_el.send_keys(username)
        password_el = self.wait.until(EC.presence_of_element_located(self.PASSWORD))
        password_el.clear()
        password_el.send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()

# pages/welcome_modal_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class WelcomeModalPage:
    MODAL = (By.ID, "welcome-modal")
    CLOSE_BTN = (By.XPATH, "//button[@aria-label='Close']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def accept_welcome_modal(self):
        modal = self.wait.until(EC.presence_of_element_located(self.MODAL))
        close_btn = modal.find_element(*self.CLOSE_BTN)
        close_btn.click()

# pages/manage_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ManagePage:
    MANAGE_TAB = (By.XPATH, "//a[.='Manage']")
    DEVICE_USERS_TAB = (By.XPATH, "//a[.='Device Users']")
    DEVICES_LIST = (By.CSS_SELECTOR, ".device-list .device")
    NO_DEVICES = (By.XPATH, "//div[contains(text(), 'No devices connected')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_manage(self):
        self.wait.until(EC.element_to_be_clickable(self.MANAGE_TAB)).click()

    def open_device_users(self):
        self.wait.until(EC.element_to_be_clickable(self.DEVICE_USERS_TAB)).click()

    def get_all_devices(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.DEVICES_LIST))
            devices = self.driver.find_elements(*self.DEVICES_LIST)
            return [d.text for d in devices]
        except Exception:
            # Check for no devices message
            try:
                self.driver.find_element(*self.NO_DEVICES)
                return []
            except Exception:
                raise

# conftest.py
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

# tests/test_login_and_device_management.py
import pytest
import allure
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

@allure.feature("Login and Device Management")
def test_login_and_device_management(driver):
    logging.info("Navigating to login page...")
    login_page = LoginPage(driver)
    welcome_modal = WelcomeModalPage(driver)
    manage_page = ManagePage(driver)

    # Login
    logging.info("Entering credentials and logging in...")
    login_page.login(config.USERNAME, config.PASSWORD)

    # Handle welcome modal if present
    try:
        logging.info("Checking for welcome modal...")
        welcome_modal.accept_welcome_modal()
        logging.info("Welcome modal closed.")
    except Exception:
        logging.info("Welcome modal not displayed.")

    # Navigate to Manage → Device Users
    logging.info("Navigating to Manage section...")
    manage_page.open_manage()
    logging.info("Opening Device Users tab...")
    manage_page.open_device_users()

    # Wait for devices to load
    logging.info("Waiting for devices to load...")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        logging.error(f"Page body did not load: {e}")

    # Get devices
    logging.info("Retrieving connected devices...")
    devices = manage_page.get_all_devices()

    # Print devices
    if devices:
        logging.info(f"Connected devices found: {devices}")
    else:
        logging.info("No devices connected.")

    # Assertion
    logging.info("Validating devices list type...")
    assert isinstance(devices, list), "Device list should be a list"

    # Allure step
    allure.attach(str(devices), name="Devices List", attachment_type=allure.attachment_type.TEXT)

    logging.info("[PASS] Test completed successfully.")

# requirements.txt
pytest==8.0.0
selenium==4.16.0
allure-pytest==2.13.2
webdriver-manager==4.0.1
pytest-html==4.1.1
pytest-xdist==3.5.0
requests==2.31.0
python-dotenv==1.0.1

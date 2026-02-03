import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import config

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage

class TestSuccessfulLoginAndDeviceListRetrieval(unittest.TestCase):
    """
    Test Case: TC01 - Successful Login and Device List Retrieval
    Steps:
      1. Launch app
      2. Go to login
      3. Enter valid credentials
      4. Handle modal if present
      5. Go to Manage > Device Users
      6. Wait for devices to load
      7. Verify devices displayed
    """

    def setUp(self):
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.get(config.BASE_URL)

        # Page objects
        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        self.manage_page = ManagePage(self.driver)

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

    def test_successful_login_and_device_list_retrieval(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Step 1-3: Launch app and login with valid credentials
        # (LoginPage.login() opens the app and logs in)
        self.login_page.login(config.USERNAME, config.PASSWORD)

        # Step 4: Handle welcome modal if present
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed")

        # Step 5: Navigate to Manage > Device Users
        try:
            self.manage_page.open_manage()
        except ElementClickInterceptedException as e:
            # Fallback to JS click if intercepted
            element = wait.until(EC.element_to_be_clickable(self.manage_page.MANAGE_MENU))
            driver.execute_script("arguments[0].click();", element)

        try:
            self.manage_page.open_device_users()
        except ElementClickInterceptedException as e:
            element = wait.until(EC.element_to_be_clickable(self.manage_page.DEVICE_USERS_MENU))
            driver.execute_script("arguments[0].click();", element)

        # Step 6: Wait for devices to load (or "No Device Users" message)
        # Step 7: Verify devices displayed
        devices = self.manage_page.get_all_devices()
        print("Devices found:", devices)

        # Assert that the device list is a list (could be empty if no devices)
        self.assertIsInstance(devices, list, "Device list should be a list")

        # If devices are expected, assert at least one device is present
        # (Remove/comment this assertion if empty device list is a valid case for this test)
        self.assertGreater(len(devices), 0, "At least one device should be displayed")

if __name__ == '__main__':
    unittest.main()

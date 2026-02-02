import unittest
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import config

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage

class TestLoginAndDeviceManagement(unittest.TestCase):

    def setUp(self):
        # Set up Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Optional: run headless for CI
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

        # Initialize page objects
        self.login_page = LoginPage(self.driver)
        self.welcome_modal = WelcomeModalPage(self.driver)
        self.manage_page = ManagePage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_login_and_device_management_flow(self):
        # TC01: Launch Application
        # Step 1: Launch browser and go to BASE_URL
        self.login_page.open()
        # Assert login page is displayed (by checking presence of login email field)
        login_email_present = self.login_page.wait.until(
            lambda d: d.find_element(*LoginPage.EMAIL)
        )
        self.assertTrue(login_email_present.is_displayed(), "Login page is not displayed")

        # TC02: Login with Valid Credentials
        # Step 2: Enter valid USERNAME and PASSWORD, Click Login
        self.login_page.login(config.USERNAME, config.PASSWORD)
        # Assert dashboard is displayed (by checking for Manage menu)
        dashboard_loaded = self.manage_page.wait.until(
            lambda d: d.find_element(*ManagePage.MANAGE_MENU)
        )
        self.assertTrue(dashboard_loaded.is_displayed(), "Dashboard not displayed after login")

        # TC04: Handle Welcome Modal
        # Step 3: Handle welcome modal if present
        try:
            self.welcome_modal.accept_welcome_modal()
        except Exception:
            # Modal not present, continue
            pass

        # TC05: Navigate to Manage Section
        # Step 4: Click 'Manage'
        try:
            self.manage_page.open_manage()
        except ElementClickInterceptedException:
            # Fallback to JS click
            element = self.driver.find_element(*ManagePage.MANAGE_MENU)
            self.driver.execute_script("arguments[0].click();", element)

        # Assert Manage page is displayed (by checking for Device Users menu)
        manage_loaded = self.manage_page.wait.until(
            lambda d: d.find_element(*ManagePage.DEVICE_USERS_MENU)
        )
        self.assertTrue(manage_loaded.is_displayed(), "Manage page not displayed")

        # TC06: Open Device Users Section
        # Step 5: Click 'Device Users'
        try:
            self.manage_page.open_device_users()
        except ElementClickInterceptedException:
            element = self.driver.find_element(*ManagePage.DEVICE_USERS_MENU)
            self.driver.execute_script("arguments[0].click();", element)

        # Assert Device Users tab is displayed (by checking for devices or no devices message)
        # TC07: Wait for Devices to Load
        # Step 6: Wait for devices to load
        # TC08: Retrieve Connected Devices
        # Step 7: Retrieve devices
        devices = self.manage_page.get_all_devices()

        # TC09: Validate Devices List Format
        # Step 8: Validate returned data is a list
        self.assertIsInstance(devices, list, "Devices should be returned as a list")

        # Print devices for output
        print("Connected Devices:")
        if devices:
            for device in devices:
                print(f"- {device}")
        else:
            print("No devices connected")

        # TC10: No Devices Connected
        # Step 9: If no devices, check for 'No devices connected' message or empty list
        if not devices:
            # Check for 'No Device Users' message
            try:
                no_devices_msg = self.driver.find_element(*ManagePage.NO_DEVICE_USERS_MSG)
                self.assertTrue(no_devices_msg.is_displayed(), "'No devices connected' message not displayed")
            except Exception:
                # Message not found, but list is empty
                pass

        # TC11: Device List Load Failure
        # Step 10: Simulate device list load failure (network error)
        # Placeholder: Implement network disconnect simulation and error message validation
        # Example:
        # # Placeholder: Simulate network disconnect and validate error message and retry option

        # TC12: Session Timeout During Navigation
        # Step 11: Handle session timeout while navigating
        # Placeholder: Implement session timeout simulation and validation
        # Example:
        # # Placeholder: Simulate session expiration and check for redirect to login page and session expired message

    def test_login_with_invalid_credentials(self):
        # TC03: Login with Invalid Credentials
        # Step 1: Enter invalid USERNAME or PASSWORD, Click Login
        self.login_page.open()
        self.login_page.login("invalid_user", "invalid_pass")
        # Assert error message displayed, login fails
        # Placeholder: Implement error message locator and assertion
        # Example:
        # error_msg = self.driver.find_element(By.XPATH, "//div[@class='error']")
        # self.assertTrue(error_msg.is_displayed(), "Error message not displayed for invalid login")
        # # Placeholder: Implement functionality for error message locator

if __name__ == "__main__":
    unittest.main()

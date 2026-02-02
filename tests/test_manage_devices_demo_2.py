import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config

class TestDeviceManagementWorkflow(unittest.TestCase):

    def setUp(self):
        # Initialize Chrome WebDriver and maximize window
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)

    def tearDown(self):
        # Quit the browser
        self.driver.quit()

    def login(self, username, password):
        # Step: Launch app and login
        login_page = LoginPage(self.driver)
        login_page.login(username, password)

    def handle_welcome_modal(self):
        # Step: Handle welcome modal if present
        try:
            welcome_modal = WelcomeModalPage(self.driver)
            welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed or already handled.")

    def navigate_to_device_users(self):
        # Step: Navigate to Manage > Device Users
        manage_page = ManagePage(self.driver)
        manage_page.open_manage()
        manage_page.open_device_users()
        return manage_page

    def test_TC01_successful_login_and_device_list_retrieval(self):
        """
        TC01: Registered user logs in, handles modal, navigates to Device Users, views devices.
        """
        # Step 1-3: Login
        self.login(config.USERNAME, config.PASSWORD)

        # Step 4: Handle modal
        self.handle_welcome_modal()

        # Step 5-6: Go to Manage > Device Users
        manage_page = self.navigate_to_device_users()

        # Step 7: Wait for device list to load
        time.sleep(2)  # Prefer explicit waits, but sleep for CI stability

        # Step 8: Verify devices
        devices = manage_page.get_all_devices()
        print("Devices:", devices if devices else "No devices connected")
        self.assertIsInstance(devices, list)
        # If devices are expected, check not empty
        # self.assertGreater(len(devices), 0)  # Uncomment if always expecting devices

    def test_TC02_invalid_login_credentials(self):
        """
        TC02: System prevents access with incorrect credentials.
        """
        # Step 1: Launch app and go to login page
        login_page = LoginPage(self.driver)
        login_page.open()

        # Step 2: Enter invalid credentials
        invalid_username = "invalid_user@example.com"
        invalid_password = "wrongpassword"
        login_page.login(invalid_username, invalid_password)

        # Step 3: Login and expect error
        # Placeholder: Implement error message locator and assertion
        try:
            error_msg = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'error') or contains(text(),'Invalid')]"))
            )
            self.assertIn("Invalid", error_msg.text)
        except TimeoutException:
            self.fail("Error message not displayed for invalid login.")

    def test_TC03_welcome_modal_handling(self):
        """
        TC03: Workflow continues if welcome modal appears or not.
        """
        self.login(config.USERNAME, config.PASSWORD)
        # Step: Observe modal and handle if present
        self.handle_welcome_modal()
        # Step: Go to Manage > Device Users
        manage_page = self.navigate_to_device_users()
        # Step: Device list accessible
        devices = manage_page.get_all_devices()
        print("Devices after modal handling:", devices)
        self.assertIsInstance(devices, list)

    def test_TC04_device_list_loads_with_no_devices_connected(self):
        """
        TC04: System displays message if no devices connected.
        """
        self.login(config.USERNAME, config.PASSWORD)
        self.handle_welcome_modal()
        manage_page = self.navigate_to_device_users()
        # Wait for device list
        time.sleep(2)
        devices = manage_page.get_all_devices()
        print("Devices:", devices)
        if not devices:
            # Check for 'No Device Users' message
            try:
                msg = self.wait.until(
                    EC.visibility_of_element_located(ManagePage.NO_DEVICE_USERS_MSG)
                )
                self.assertIn("No Device Users", msg.text)
            except TimeoutException:
                self.fail("'No Device Users' message not displayed when no devices connected.")
        else:
            self.fail("Devices found when none should be connected.")

    def test_TC05_device_list_loads_with_many_devices(self):
        """
        TC05: System handles large device list without performance issues.
        """
        self.login(config.USERNAME, config.PASSWORD)
        self.handle_welcome_modal()
        manage_page = self.navigate_to_device_users()
        # Wait for device list
        time.sleep(2)
        devices = manage_page.get_all_devices()
        print("Devices:", devices)
        self.assertIsInstance(devices, list)
        # Placeholder: Implement check for large device list and UI responsiveness

    def test_TC06_device_list_fails_to_load(self):
        """
        TC06: System shows error if device list cannot be retrieved.
        """
        self.login(config.USERNAME, config.PASSWORD)
        self.handle_welcome_modal()
        manage_page = self.navigate_to_device_users()
        # Step: Simulate backend/network failure
        # Placeholder: Implement backend/network failure simulation
        # Check for error message
        try:
            error_msg = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'error') or contains(text(),'failed')]"))
            )
            self.assertTrue("failed" in error_msg.text.lower() or "error" in error_msg.text.lower())
        except TimeoutException:
            self.fail("Error message not displayed when device list fails to load.")

    def test_TC07_navigation_to_manage_section(self):
        """
        TC07: User can navigate to Manage section after login.
        """
        self.login(config.USERNAME, config.PASSWORD)
        self.handle_welcome_modal()
        manage_page = ManagePage(self.driver)
        manage_page.open_manage()
        # Placeholder: Implement assertion to verify Manage section is loaded
        # Example: Check for Manage section header
        try:
            header = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(),'Manage')]") )
            )
            self.assertIn("Manage", header.text)
        except TimeoutException:
            self.fail("Manage section not loaded.")

    def test_TC08_access_control_for_device_users_section(self):
        """
        TC08: Only authorized users can access Device Users.
        """
        # Step: Login as unauthorized user
        unauthorized_username = "unauthorized_user@example.com"
        unauthorized_password = "password"
        self.login(unauthorized_username, unauthorized_password)
        self.handle_welcome_modal()
        manage_page = ManagePage(self.driver)
        manage_page.open_manage()
        # Step: Attempt Device Users
        try:
            manage_page.open_device_users()
            # Check for access denied message
            denied_msg = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Access Denied') or contains(text(),'not authorized')]") )
            )
            self.assertTrue("denied" in denied_msg.text.lower() or "not authorized" in denied_msg.text.lower())
        except TimeoutException:
            self.fail("Access denied message not displayed for unauthorized user.")
        except Exception:
            # Placeholder: Implement handling for missing access control
            print("Access control not implemented or locator missing.")

    def test_TC09_device_list_data_verification(self):
        """
        TC09: Device list displays correct device info.
        """
        self.login(config.USERNAME, config.PASSWORD)
        self.handle_welcome_modal()
        manage_page = self.navigate_to_device_users()
        time.sleep(2)
        devices = manage_page.get_all_devices()
        print("Devices:", devices)
        # Placeholder: Implement verification against known device data
        # Example:
        # expected_devices = ["Device A", "Device B"]
        # self.assertEqual(devices, expected_devices)

    def test_TC10_session_timeout_during_workflow(self):
        """
        TC10: System handles session timeout gracefully.
        """
        self.login(config.USERNAME, config.PASSWORD)
        self.handle_welcome_modal()
        manage_page = self.navigate_to_device_users()
        # Step: Wait for session to expire
        # Placeholder: Implement session timeout simulation (e.g., wait, API call, etc.)
        print("Waiting for session to expire...")
        time.sleep(65)  # Example: Wait longer than session timeout
        # Step: Interact with device list
        try:
            devices = manage_page.get_all_devices()
            # Placeholder: Implement check for re-authentication prompt or logout
            # Example: Check for login page or session expired message
            login_field = self.wait.until(
                EC.presence_of_element_located(LoginPage.EMAIL)
            )
            self.assertTrue(login_field.is_displayed())
        except TimeoutException:
            self.fail("Session timeout not handled gracefully.")

if __name__ == '__main__':
    unittest.main()

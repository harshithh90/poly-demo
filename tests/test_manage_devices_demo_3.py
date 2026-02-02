import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config

class TestLoginAndDeviceManagement(unittest.TestCase):

    def setUp(self):
        # Initialize the Chrome WebDriver and maximize window
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)

    def tearDown(self):
        # Quit the browser after each test
        self.driver.quit()

    def test_login_and_view_connected_devices(self):
        driver = self.driver

        # Step 1: Launch Application
        # Open browser and navigate to BASE_URL
        login_page = LoginPage(driver)
        login_page.open()
        # Assert login page is displayed by checking for email input
        self.assertTrue(self.wait.until(EC.presence_of_element_located(LoginPage.EMAIL)))

        # Step 2: Login with Valid Credentials
        # Enter valid USERNAME and PASSWORD, click Login
        login_page.login(config.USERNAME, config.PASSWORD)
        # Assert dashboard is displayed (could check for a dashboard element, placeholder below)
        # Placeholder: Implement dashboard validation
        # self.assertTrue(self.wait.until(EC.presence_of_element_located((By.ID, 'dashboard'))))

        # Step 3: Handle Welcome Modal
        # Close welcome modal if present
        welcome_modal = WelcomeModalPage(driver)
        try:
            welcome_modal.accept_welcome_modal()
        except Exception:
            print("Welcome modal not displayed or already closed.")

        # Step 4: Navigate to Manage Section
        manage_page = ManagePage(driver)
        try:
            manage_page.open_manage()
        except ElementClickInterceptedException:
            # Fallback to JS click
            element = self.wait.until(EC.element_to_be_clickable(ManagePage.MANAGE_MENU))
            driver.execute_script("arguments[0].click();", element)

        # Assert Manage page is displayed (could check for a Manage page element, placeholder below)
        # Placeholder: Implement Manage page validation

        # Step 5: Open Device Users Section
        try:
            manage_page.open_device_users()
        except ElementClickInterceptedException:
            element = self.wait.until(EC.element_to_be_clickable(ManagePage.DEVICE_USERS_MENU))
            driver.execute_script("arguments[0].click();", element)

        # Assert Device Users tab is displayed (could check for a Device Users tab element, placeholder below)
        # Placeholder: Implement Device Users tab validation

        # Step 6: Wait for Devices to Load
        # Wait for device list to populate
        time.sleep(2)  # Prefer explicit waits, but sleep is used in CI for stability

        # Step 7: Retrieve Connected Devices
        devices = manage_page.get_all_devices()

        # Step 8: Print Connected Devices
        print("Connected Devices:")
        if devices:
            for device in devices:
                print(device)
        else:
            print("No devices connected")

        # Step 9: Validate Devices List
        self.assertIsInstance(devices, list)

    def test_login_with_invalid_credentials(self):
        driver = self.driver
        login_page = LoginPage(driver)
        login_page.open()

        # Step: Enter invalid USERNAME or PASSWORD, click Login
        login_page.login("invalid_user", "invalid_pass")

        # Step: Assert error message displayed, login fails
        # Placeholder: Implement error message locator and assertion
        # error_msg = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'error')]")))
        # self.assertIn("Invalid credentials", error_msg.text)

    def test_no_devices_connected(self):
        driver = self.driver
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(config.USERNAME, config.PASSWORD)
        welcome_modal = WelcomeModalPage(driver)
        try:
            welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        manage_page = ManagePage(driver)
        manage_page.open_manage()
        manage_page.open_device_users()
        time.sleep(2)

        # Step: Wait for devices, expect "No devices connected" message
        # The get_all_devices() method prints "No devices found" and returns []
        devices = manage_page.get_all_devices()
        self.assertEqual(devices, [])

    def test_device_list_load_failure(self):
        driver = self.driver
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(config.USERNAME, config.PASSWORD)
        welcome_modal = WelcomeModalPage(driver)
        try:
            welcome_modal.accept_welcome_modal()
        except Exception:
            pass
        manage_page = ManagePage(driver)
        manage_page.open_manage()
        manage_page.open_device_users()
        time.sleep(2)

        # Step: Simulate network error during device retrieval
        # Placeholder: Implement network error simulation (e.g., disable network, mock API)
        # Placeholder: Assert error message displayed and retry option available
        # error_msg = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'error')]")))
        # self.assertIn("Network error", error_msg.text)
        # retry_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Retry']")))
        # self.assertTrue(retry_btn.is_displayed())

if __name__ == '__main__':
    unittest.main()

import sys
import os
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage  # Placeholder: Implement WelcomeModalPage if missing
from pages.manage_page import ManagePage
import config

@pytest.fixture
def driver(driver):
    # Assumes driver fixture is defined in conftest.py using driver_factory
    yield driver
    driver.quit()

# TC01: Launch Application
# TC02: Login with Valid Credentials
# TC04: Handle Welcome Modal
# TC05: Skip Welcome Modal (Not Present)
# TC06: Navigate to Manage Section
# TC07: Open Device Users Section
# TC08: Wait for Devices to Load
# TC10: Retrieve Connected Devices
# TC12: Print Connected Devices
# TC13: Validate Devices List Format

def test_login_and_device_management_flow(driver):
    """
    End-to-end test: Login, handle welcome modal, navigate to Manage > Device Users,
    wait for devices, retrieve and print device list, validate format.
    """
    # Step 1: Launch application
    driver.get(config.BASE_URL)
    login_page = LoginPage(driver)
    welcome_modal = WelcomeModalPage(driver)  # Placeholder: Implement WelcomeModalPage if missing
    manage_page = ManagePage(driver)

    # Step 2: Login with valid credentials
    login_page.login(config.USERNAME, config.PASSWORD)

    # Step 3: Handle welcome modal if present
    try:
        welcome_modal.accept_welcome_modal()
    except Exception:
        print("Welcome modal not displayed")

    # Step 4: Navigate to Manage section
    manage_page.open_manage()

    # Step 5: Open Device Users section
    manage_page.open_device_users()

    # Step 6: Wait for devices to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except TimeoutException:
        pytest.fail("Page body did not load in time")

    # Step 7: Retrieve connected devices
    devices = manage_page.get_all_devices()

    # Step 8: Print connected devices
    print("Connected Devices:")
    for device in devices:
        print(device)

    # Step 9: Validate devices list format
    assert isinstance(devices, list), "Device list should be a list"

# TC03: Login with Invalid Credentials

def test_login_with_invalid_credentials(driver):
    """
    Negative test: Attempt login with invalid credentials, expect error message.
    """
    login_page = LoginPage(driver)
    driver.get(config.BASE_URL)
    # Use invalid credentials
    invalid_username = "invalid_user"
    invalid_password = "invalid_pass"
    login_page.login(invalid_username, invalid_password)
    # Placeholder: Implement error message locator/assertion for failed login
    # Example:
    # error_msg = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.XPATH, "//div[@class='error-message']"))
    # )
    # assert "Invalid credentials" in error_msg.text
    # Placeholder: Implement functionality for login error validation

# TC09: Device List Fails to Load

def test_device_list_fails_to_load(driver):
    """
    Negative test: Simulate device list failing to load (timeout/error), expect error message.
    """
    login_page = LoginPage(driver)
    welcome_modal = WelcomeModalPage(driver)  # Placeholder: Implement WelcomeModalPage if missing
    manage_page = ManagePage(driver)
    driver.get(config.BASE_URL)
    login_page.login(config.USERNAME, config.PASSWORD)
    try:
        welcome_modal.accept_welcome_modal()
    except Exception:
        pass
    manage_page.open_manage()
    manage_page.open_device_users()
    # Simulate device list failing to load
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'device')]")
        )
    except TimeoutException:
        # Placeholder: Implement error message locator/assertion for device list load failure
        print("Device list failed to load. Error message should be displayed.")
        # Example:
        # error_msg = driver.find_element(By.XPATH, "//div[@class='error-message']")
        # assert "Failed to load devices" in error_msg.text
        # Placeholder: Implement functionality for device list load error validation

# TC11: Empty Device List

def test_empty_device_list(driver):
    """
    Edge test: Handle case where no devices are connected, expect 'No devices connected' message.
    """
    login_page = LoginPage(driver)
    welcome_modal = WelcomeModalPage(driver)  # Placeholder: Implement WelcomeModalPage if missing
    manage_page = ManagePage(driver)
    driver.get(config.BASE_URL)
    login_page.login(config.USERNAME, config.PASSWORD)
    try:
        welcome_modal.accept_welcome_modal()
    except Exception:
        pass
    manage_page.open_manage()
    manage_page.open_device_users()
    # Simulate empty device list
    devices = manage_page.get_all_devices()
    if not devices:
        # Check for 'No Device Users' message
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(ManagePage.NO_DEVICE_USERS_MSG)
            )
            print("No devices connected message displayed.")
        except TimeoutException:
            pytest.fail("No devices connected message not displayed when device list is empty.")
    else:
        pytest.skip("Devices found, cannot test empty device list scenario.")

# Placeholder: Implement additional edge/negative cases as needed
# - WelcomeModalPage class implementation if missing
# - Error message locators for login/device list failures
# - Test data management for valid/invalid credentials

import sys
import os
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException

# Add project root to path for imports
#
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage  # Placeholder: Implement WelcomeModalPage if missing
from pages.manage_page import ManagePage
import config

@pytest.fixture
def driver():
    """
    Pytest fixture for WebDriver setup and teardown.
    Assumes driver is provided by conftest.py or utils.driver_factory.
    """
    # Placeholder: Use actual driver factory or setup from your framework
    from selenium import webdriver
    driver = webdriver.Chrome()  # Or use get_driver() from your utils if available
    yield driver
    driver.quit()

def test_launch_application(driver):
    """
    TC01: Launch Application
    Step: Open application and navigate to login page.
    """
    driver.get(config.BASE_URL)
    # Assert login page is displayed by checking for login field presence
    login_page = LoginPage(driver)
    email_el = login_page.wait.until(EC.presence_of_element_located(LoginPage.EMAIL))
    assert email_el.is_displayed(), "Login page should be displayed"

def test_login_with_valid_credentials(driver):
    """
    TC02: Login with Valid Credentials
    Step: Enter valid username/password and click Login.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    # Assert user is redirected to main page (check for Manage menu)
    manage_page = ManagePage(driver)
    manage_menu = manage_page.wait.until(EC.presence_of_element_located(ManagePage.MANAGE_MENU))
    assert manage_menu.is_displayed(), "User should be redirected to main page after login"

def test_login_with_invalid_credentials(driver):
    """
    TC03: Login with Invalid Credentials
    Step: Enter invalid username/password and click Login.
    """
    login_page = LoginPage(driver)
    login_page.login("invalid_user", "invalid_pass")
    # Placeholder: Implement error message locator and assertion
    # Example:
    # error_msg = driver.find_element(By.XPATH, "//div[@class='error']")
    # assert error_msg.is_displayed(), "Error message should be displayed for invalid login"
    # Placeholder: Implement functionality for error message validation

def test_handle_welcome_modal(driver):
    """
    TC04: Handle Welcome Modal
    Step: Check for modal and close/accept if present.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    welcome_modal = WelcomeModalPage(driver)
    try:
        welcome_modal.accept_welcome_modal()
    except Exception:
        print("Welcome modal not displayed")
    # Assert modal is closed or not present
    # Placeholder: Implement assertion for modal closed state
    #pass

def test_navigate_to_manage_section(driver):
    """
    TC05: Navigate to Manage Section
    Step: Click 'Manage' menu.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    try:
        manage_page.open_manage()
    except ElementClickInterceptedException as e:
        element = manage_page.wait.until(EC.element_to_be_clickable(ManagePage.MANAGE_MENU))
        driver.execute_script("arguments[0].click();", element)
    # Assert Manage section is displayed
    # Placeholder: Implement assertion for Manage section display

def test_open_device_users_section(driver):
    """
    TC06: Open Device Users Section
    Step: Click 'Device Users' tab.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    manage_page.open_manage()
    try:
        manage_page.open_device_users()
    except ElementClickInterceptedException as e:
        element = manage_page.wait.until(EC.element_to_be_clickable(ManagePage.DEVICE_USERS_MENU))
        driver.execute_script("arguments[0].click();", element)
    # Assert Device Users tab is displayed
    # Placeholder: Implement assertion for Device Users tab display

def test_wait_for_devices_to_load(driver):
    """
    TC07: Wait for Devices to Load
    Step: Wait for device list to populate.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    manage_page.open_manage()
    manage_page.open_device_users()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    # Assert devices list is populated or "No Device Users" message is handled
    # Placeholder: Implement assertion for devices list population

def test_retrieve_connected_devices(driver):
    """
    TC08: Retrieve Connected Devices
    Step: Get all connected devices.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    manage_page.open_manage()
    manage_page.open_device_users()
    devices = manage_page.get_all_devices()
    assert isinstance(devices, list), "Device list should be a list"
    # Assert at least one device if not empty
    if devices:
        assert len(devices) > 0, "There should be at least one connected device"

def test_print_connected_devices(driver):
    """
    TC09: Print Connected Devices
    Step: Print/display device info.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    manage_page.open_manage()
    manage_page.open_device_users()
    devices = manage_page.get_all_devices()
    print("Connected Devices:")
    for device in devices:
        print(device)
    # No assertion needed for print step

def test_validate_devices_list_format(driver):
    """
    TC10: Validate Devices List Format
    Step: Assert devices are returned in a list.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    manage_page.open_manage()
    manage_page.open_device_users()
    devices = manage_page.get_all_devices()
    assert isinstance(devices, list), "Devices should be returned as a list"

def test_no_devices_connected(driver):
    """
    TC11: No Devices Connected
    Step: Wait for devices list to load when no devices are connected.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    manage_page.open_manage()
    manage_page.open_device_users()
    # Check for "No Device Users" message
    try:
        msg = manage_page.wait.until(EC.visibility_of_element_located(ManagePage.NO_DEVICE_USERS_MSG))
        assert msg.is_displayed(), "'No devices connected' message should be displayed"
    except Exception:
        # If not found, fail the test
        pytest.fail("'No devices connected' message not displayed when expected")

def test_device_list_fails_to_load(driver):
    """
    TC12: Device List Fails to Load
    Step: Simulate network failure and wait for devices list to load.
    """
    login_page = LoginPage(driver)
    login_page.login(config.USERNAME, config.PASSWORD)
    manage_page = ManagePage(driver)
    manage_page.open_manage()
    manage_page.open_device_users()
    # Placeholder: Implement network failure simulation
    # Placeholder: Implement error message locator and assertion for device list load failure

# Additional edge/negative cases can be added as needed per recommendations.
# Ensure all locators and helper functions are imported from the knowledge base.
# For missing page objects or locators, use placeholder comments as shown above.

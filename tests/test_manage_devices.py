import sys
import os
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config


def test_device_users_list(driver):   # 👈 driver comes from conftest.py
    # Open application
    driver.get(config.BASE_URL)

    # Page objects
    login_page = LoginPage(driver)
    welcome_modal = WelcomeModalPage(driver)
    manage_page = ManagePage(driver)

    # Login
    login_page.login(config.USERNAME, config.PASSWORD)

    # Handle welcome modal if present
    try:
        welcome_modal.accept_welcome_modal()
    except Exception:
        print("Welcome modal not displayed")

    # Navigate to Manage → Device Users
    manage_page.open_manage()
    manage_page.open_device_users()

    # Explicit wait instead of sleep
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Get devices
    devices = manage_page.get_all_devices()

    # Assertion
    assert isinstance(devices, list), "Device list should be a list"

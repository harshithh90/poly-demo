import pytest
import time

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config


def test_login_and_manage_devices(driver):

    login_page = LoginPage(driver)
    welcome_modal = WelcomeModalPage(driver)
    manage_page = ManagePage(driver)

    login_page.login(config.USERNAME, config.PASSWORD)

    try:
        welcome_modal.accept_welcome_modal()
    except Exception:
        print("Welcome modal not displayed")

    manage_page.open_manage()
    manage_page.open_device_users()

    time.sleep(5)

    devices = manage_page.get_all_devices()

    if not devices:
        print("No devices connected")
    else:
        print(f"Devices found ({len(devices)}):")
        for device in devices:
            print(device)

    assert isinstance(devices, list)

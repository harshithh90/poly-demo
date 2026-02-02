import time
import allure

from pages.login_page import LoginPage
from pages.welcome_modal_page import WelcomeModalPage
from pages.manage_page import ManagePage
import config


@allure.feature("Device Management")
@allure.story("Login and view connected devices")
def test_login_and_manage_devices(driver):

    with allure.step("Initialize pages"):
        login_page = LoginPage(driver)
        welcome_modal = WelcomeModalPage(driver)
        manage_page = ManagePage(driver)

    with allure.step("Login to application"):
        login_page.login(config.USERNAME, config.PASSWORD)

    with allure.step("Handle welcome modal if present"):
        try:
            welcome_modal.accept_welcome_modal()
        except Exception:
            allure.attach(
                "Welcome modal not displayed",
                name="Info",
                attachment_type=allure.attachment_type.TEXT
            )

    with allure.step("Navigate to Manage → Device Users"):
        manage_page.open_manage()
        manage_page.open_device_users()

    time.sleep(5)  # OK for now in CI

    with allure.step("Fetch connected devices"):
        devices = manage_page.get_all_devices()

        allure.attach(
            "\n".join(devices) if devices else "No devices connected",
            name="Devices",
            attachment_type=allure.attachment_type.TEXT
        )

    assert isinstance(devices, list)


import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import InvalidSessionIdException
import config


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver_path = ChromeDriverManager().install()

    # 🔥 CRITICAL FIX for GitHub Actions
    if "THIRD_PARTY_NOTICES" in driver_path:
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)

    # Navigate to base URL so tests start from the app home/login
    try:
        driver.get(config.BASE_URL)
    except Exception:
        # ignore navigation errors here; tests can navigate explicitly if needed
        pass

    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                png = driver.get_screenshot_as_png()
            except InvalidSessionIdException:
                # Session already closed; skip attaching screenshot
                return
            except Exception:
                return

            try:
                allure.attach(
                    png,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                # If attaching fails for any reason, don't raise further
                return

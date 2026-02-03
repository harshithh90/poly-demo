import os
import stat
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

    # ✅ Fix webdriver-manager returning THIRD_PARTY_NOTICES path
    if "THIRD_PARTY_NOTICES" in driver_path:
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver")

    # 🔥 REQUIRED for GitHub Actions (this is what you were missing)
    os.chmod(driver_path, stat.S_IRWXU)

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)

    # Optional: open base URL once
    try:
        driver.get(config.BASE_URL)
    except Exception:
        pass

    yield driver

    try:
        driver.quit()
    except Exception:
        pass


# 📸 Attach screenshot to Allure on test failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if not driver:
            return

        try:
            png = driver.get_screenshot_as_png()
            allure.attach(
                png,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except InvalidSessionIdException:
            pass
        except Exception:
            pass


# 🔐 Safety net: block webdriver.Chrome() usage anywhere else
@pytest.fixture(autouse=True)
def block_direct_chrome_usage():
    import selenium.webdriver
    original = selenium.webdriver.Chrome

    def fail(*args, **kwargs):
        raise RuntimeError(
            "❌ Do NOT instantiate webdriver.Chrome() directly. "
            "Use the pytest 'driver' fixture."
        )

    selenium.webdriver.Chrome = fail
    yield
    selenium.webdriver.Chrome = original

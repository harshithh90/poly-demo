from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


class LoginPage:
    EMAIL = (By.XPATH, "//input[@id='login-email']")
    PASSWORD = (By.XPATH, "//input[@id='login-input-password']")
    LOGIN_BTN = (By.XPATH, "//button[text()='LOG IN']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open(self):
        self.driver.get(config.BASE_URL)

    def login(self, username, password):
        self.open()  # 🔥 CRITICAL FIX

        email_el = self.wait.until(EC.presence_of_element_located(self.EMAIL))
        email_el.clear()
        email_el.send_keys(username)

        password_el = self.wait.until(EC.presence_of_element_located(self.PASSWORD))
        password_el.clear()
        password_el.send_keys(password)

        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()

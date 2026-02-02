from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):

    EMAIL = (By.XPATH, "//input[@id='login-email']")
    PASSWORD = (By.XPATH, "//input[@id='login-input-password']")
    LOGIN_BTN = (By.XPATH, "//button[text()='LOG IN']")

    def login(self, username, password):
        self.type(self.EMAIL, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

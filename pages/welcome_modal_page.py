from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WelcomeModalPage:

    CHECKBOX = (By.XPATH, "//span[@class='checkbox-custom']")
    GET_STARTED_BTN = (
        By.XPATH,
        "//button[@data-testid='welcome-modal-button' and not(@disabled)]"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def accept_welcome_modal(self):
        """
        Click checkbox and then click 'Let's Get Started'
        """
        checkbox = self.wait.until(
            EC.presence_of_element_located(self.CHECKBOX)
        )
        self.driver.execute_script("arguments[0].click();", checkbox)

        button = self.wait.until(
            EC.element_to_be_clickable(self.GET_STARTED_BTN)
        )
        button.click()

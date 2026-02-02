from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ManagePage(BasePage):

    MANAGE_MENU = (
        By.XPATH,
        "//span[@data-testid='dropdown-trigger' and normalize-space()='Manage']"
    )

    DEVICE_USERS_MENU = (
        By.XPATH,
        "//a[@data-testid='sub-menu-item' and normalize-space()='Device Users']"
    )

    NO_DEVICE_USERS_MSG = (
        By.XPATH,
        "//h4[normalize-space()='No Device Users']"
    )

    DEVICES = (
        By.XPATH,
        "//div[contains(@class,'device')]"
    )

    def open_manage(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.MANAGE_MENU)
        )
        self.driver.execute_script("arguments[0].click();", element)

    def open_device_users(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.DEVICE_USERS_MENU)
        )
        element.click()

    def get_all_devices(self):
        """
        Returns device list.
        If 'No Device Users' message appears, prints message and returns empty list.
        """
        # Check for 'No Device Users' message
        try:
            self.wait.until(EC.visibility_of_element_located(self.NO_DEVICE_USERS_MSG))
            print("No devices found")
            return []
        except:
            pass

        # Otherwise collect devices
        self.wait.until(EC.presence_of_all_elements_located(self.DEVICES))
        devices = self.driver.find_elements(*self.DEVICES)
        return [d.text.strip() for d in devices if d.text.strip()]

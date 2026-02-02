
import allure

def attach_screenshot(driver, name="Screenshot"):
    png = driver.get_screenshot_as_png()
    allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)


class AllureStep:
    def __init__(self, driver, step_name):
        self.driver = driver
        self.step_name = step_name

    def __enter__(self):
        self.step = allure.step(self.step_name)
        self.step.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        attach_screenshot(self.driver, self.step_name)
        self.step.__exit__(exc_type, exc_val, exc_tb)
        return False

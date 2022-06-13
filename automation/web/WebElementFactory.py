from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from automation.web.WaitCommands import WaitCommands


class WebElementFactory:

    def __init__(self, driver, wait: WaitCommands):
        self.driver = driver
        self.wait = wait
        print("Creating instance of WebElementFactory.")

    def create_element(self, locator: By, value: str):
        element = self.wait.wait_for_element_to_be_present(locator, value)
        return element

    def create_element(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        child_element = self.wait.wait_for_element_to_be_present(parent_locator, parent_value, child_locator, child_value)
        return child_element

    def create_element(self, parent_element: WebElement, child_locator: By, child_value: str):
        child_element = self.wait.wait_for_element_to_be_present(parent_element, child_locator, child_value)
        return child_element

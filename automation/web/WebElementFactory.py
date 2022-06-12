from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class WebElementFactory:

    global local_driver

    def __init__(self, driver: webdriver):
        self.local_driver = driver
        print("Creating instance of WebElementFactory")

    def create_element(self, locator: By, value: str):
        element = self.local_driver.find_element(locator, value)
        return element

    def create_element(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        parent_element = self.local_driver.find_element(parent_locator, parent_value)
        child_element = parent_element.find_element(child_locator, child_value)
        return child_element

    def create_element(self, parent_element: WebElement, child_locator: By, child_value: str):
        child_element = parent_element.find_element(child_locator, child_value)
        return child_element
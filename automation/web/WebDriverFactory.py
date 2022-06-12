from selenium import webdriver

from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver
import platform


class WebDriverFactory:

    def __init__(self):
        print("Creating instance of WebDriverFactory")

    @staticmethod
    def get_chrome_driver():
        print("Initializing Google Chrome Web Driver")
        chrome_driver: WebDriver = webdriver.Chrome()
        return chrome_driver

    @staticmethod
    def get_firefox_driver(self):
        print("Initializing Mozilla Firefox Web Driver")
        firefox_driver: WebDriver = webdriver.Firefox()
        return firefox_driver

    @staticmethod
    def get_safari_driver(self):
        operating_system = platform.system()
        if operating_system == 'Darwin':
            print("Initializing Safari Web Driver")
            safari_driver: WebDriver = webdriver.Safari()
        else:
            print("Unsupported Operating System to run Safari Web Driver")

        return safari_driver

    @staticmethod
    def get_edge_driver(self):
        print("Initializing Microsoft Edge Web Driver")
        edge_driver: WebDriver = webdriver.Edge()
        return edge_driver

    @staticmethod
    def get_ie_driver(self):
        operating_system = platform.system()
        if operating_system == 'Windows':
            print("Initializing Internet Explorer Web Driver")
            ie_driver: WebDriver = webdriver.Ie()
        else:
            print("Unsupported Operating System to run Internet Explorer Web Driver")

        return ie_driver

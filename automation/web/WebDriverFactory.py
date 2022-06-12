import sys

from selenium import webdriver

from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver
import platform


class WebDriverFactory:

    def __init__(self):
        print("Creating instance of WebDriverFactory")

    @staticmethod
    def __get_driver(driver_name: str):
        driver = None
        operating_system = platform.system()
        try:
            match driver_name:
                case "CHROME":
                    driver = webdriver.Chrome()
                case "FIREFOX":
                    driver = webdriver.Firefox()
                case "SAFARI":
                    if operating_system == 'Darwin':
                        driver = webdriver.Safari()
                    else:
                        print(operating_system + " is an unsupported Operating System to run Safari Web Driver")
                        exit(1)
                case "EDGE":
                    driver = webdriver.Edge()
                case "IE":
                    if operating_system == 'Windows':
                        driver = webdriver.Ie()
                    else:
                        print(operating_system + " is an unsupported Operating System to run Internet Explorer Web " +
                                                 "Driver")
                        exit(1)
                case default:
                    print("Unsupported Web Driver.")
        except Exception as error_message:
            print("Encountered Exception when trying to get " + driver_name + " Web Driver: " + str(error_message))
            exit(1)
        return driver

    @staticmethod
    def get_chrome_driver():
        print("Initializing Google Chrome Web Driver")
        chrome_driver: WebDriver = WebDriverFactory.__get_driver("CHROME")
        return chrome_driver

    @staticmethod
    def get_firefox_driver():
        print("Initializing Mozilla Firefox Web Driver")
        firefox_driver: WebDriver = WebDriverFactory.__get_driver("FIREFOX")
        return firefox_driver

    @staticmethod
    def get_safari_driver():
        print("Initializing Safari Web Driver")
        safari_driver: WebDriver = WebDriverFactory.__get_driver("SAFARI")
        return safari_driver

    @staticmethod
    def get_edge_driver():
        print("Initializing Microsoft Edge Web Driver")
        edge_driver: WebDriver = WebDriverFactory.__get_driver("EDGE")
        return edge_driver

    @staticmethod
    def get_ie_driver():
        print("Initializing Internet Explorer Web Driver")
        ie_driver: WebDriver = WebDriverFactory.__get_driver("IE")
        return ie_driver

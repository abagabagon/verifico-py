from selenium import webdriver

from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver
import platform


class WebDriverFactory:

    def __init__(self):
        print("Creating instance of WebDriverFactory")
        self.driver: WebDriver = None

    def __get_driver(self, driver_name: str):
        self.driver = None
        operating_system = platform.system()
        try:
            match driver_name:
                case "CHROME":
                    self.driver: WebDriver = webdriver.Chrome()
                case "FIREFOX":
                    self. driver: WebDriver = webdriver.Firefox()
                case "SAFARI":
                    if operating_system == 'Darwin':
                        self.driver: WebDriver = webdriver.Safari()
                    else:
                        print(operating_system + " is an unsupported Operating System to run Safari Web Driver")
                        exit(1)
                case "EDGE":
                    self.driver: WebDriver = webdriver.Edge()
                case "IE":
                    if operating_system == 'Windows':
                        self.driver: WebDriver = webdriver.Ie()
                    else:
                        print(operating_system + " is an unsupported Operating System to run Internet Explorer Web " +
                                                 "Driver")
                        exit(1)
                case default:
                    print("Unsupported Web Driver.")
        except Exception as error_message:
            print("Encountered Exception when trying to get " + driver_name + " Web Driver: " + str(error_message))
            exit(1)
        return self.driver

    def get_chrome_driver(self):
        print("Initializing Google Chrome Web Driver")
        chrome_driver: WebDriver = self.__get_driver("CHROME")
        return chrome_driver

    def get_firefox_driver(self):
        print("Initializing Mozilla Firefox Web Driver")
        firefox_driver: WebDriver = self.__get_driver("FIREFOX")
        return firefox_driver

    def get_safari_driver(self):
        print("Initializing Safari Web Driver")
        safari_driver: WebDriver = self.__get_driver("SAFARI")
        return safari_driver

    def get_edge_driver(self):
        print("Initializing Microsoft Edge Web Driver")
        edge_driver: WebDriver = self.__get_driver("EDGE")
        return edge_driver

    def get_ie_driver(self):
        print("Initializing Internet Explorer Web Driver")
        ie_driver: WebDriver = self.__get_driver("IE")
        return ie_driver

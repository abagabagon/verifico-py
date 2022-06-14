import platform
import os
import logging

from selenium.common import WebDriverException
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class WebDriverFactory:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of WebDriverFactory.")
        self.driver = None
        os.environ['GH_TOKEN'] = "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"

    def __get_driver(self, driver_name: str):
        self.log.debug("Initializing " + driver_name.replace("_", " ") + " Web Driver")
        self.driver = None
        operating_system = platform.system()
        try:
            match driver_name:
                case "GOOGLE_CHROME":
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                case "CHROMIUM":
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
                case "BRAVE":
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
                case "MOZILLA_FIREFOX":
                    self. driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
                case "SAFARI":
                    if operating_system == 'Darwin':
                        self.driver = webdriver.Safari()
                    else:
                        self.log.error(operating_system + " is an unsupported Operating System to run SAFARI Web Driver")
                        exit(1)
                case "MICROSOFT_EDGE":
                    self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
                case "INTERNET_EXPLORER":
                    if operating_system == 'Windows':
                        self.driver = webdriver.Ie(service=Service(IEDriverManager().install()))
                    else:
                        self.log.error(operating_system + " is an unsupported Operating System to run INTERNET EXPLORER Web Driver")
                        exit(1)
                case _:
                    self.log.error(driver_name.replace("_", " ") + " is an unsupported Web Driver.")
        except WebDriverException as error_message:
            self.log.error("Encountered WebDriverException when trying to get " + driver_name.replace("_", " ") + " Web Driver: " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to get " + driver_name.replace("_", " ") + " Web Driver: " + str(error_message))
            exit(1)
        return self.driver

    def get_chrome_driver(self):
        chrome_driver = self.__get_driver("CHROME")
        return chrome_driver

    def get_chromium_driver(self):
        chromium_driver = self.__get_driver("CHROMIUM")
        return chromium_driver

    def get_brave_driver(self):
        brave_driver = self.__get_driver("BRAVE")
        return brave_driver

    def get_firefox_driver(self):
        firefox_driver = self.__get_driver("FIREFOX")
        return firefox_driver

    def get_safari_driver(self):
        safari_driver = self.__get_driver("SAFARI")
        return safari_driver

    def get_edge_driver(self):
        edge_driver = self.__get_driver("EDGE")
        return edge_driver

    def get_ie_driver(self):
        ie_driver = self.__get_driver("IE")
        return ie_driver

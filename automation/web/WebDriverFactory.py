from selenium.common import WebDriverException
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from enum import Enum, auto
import platform
import os
import logging


class BrowserType(Enum):
    GOOGLE_CHROME = auto()
    CHROMIUM = auto()
    BRAVE = auto()
    MOZILLA_FIREFOX =auto()
    SAFARI = auto()
    MICROSOFT_EDGE = auto()
    INTERNET_EXPLORER = auto()


class WebDriverFactory:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of WebDriverFactory.")
        self.driver = None
        os.environ['GH_TOKEN'] = "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"

    def __get_driver(self, browser_type: BrowserType):
        local_task = str(browser_type).replace("_", " ").title()
        self.log.debug("Initializing " + local_task + " Web Driver")
        self.driver = None
        operating_system = platform.system()
        try:
            match browser_type:
                case BrowserType.GOOGLE_CHROME:
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                case BrowserType.CHROMIUM:
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
                case BrowserType.BRAVE:
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
                case BrowserType.MOZILLA_FIREFOX:
                    self. driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
                case BrowserType.SAFARI:
                    if operating_system == 'Darwin':
                        self.driver = webdriver.Safari()
                    else:
                        self.log.error(operating_system + " is an unsupported Operating System to run SAFARI Web Driver")
                        exit(1)
                case BrowserType.MICROSOFT_EDGE:
                    self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
                case BrowserType.INTERNET_EXPLORER:
                    if operating_system == 'Windows':
                        self.driver = webdriver.Ie(service=Service(IEDriverManager().install()))
                    else:
                        self.log.error(operating_system + " is an unsupported Operating System to run INTERNET EXPLORER Web Driver")
                        exit(1)
                case _:
                    self.log.error(local_task + " is an unsupported Web Driver.")
        except WebDriverException as error_message:
            self.log.error("Encountered WebDriverException when trying to get " + local_task + " Web Driver: " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to get " + local_task + " Web Driver: " + str(error_message))
            exit(1)
        return self.driver

    def get_chrome_driver(self):
        chrome_driver = self.__get_driver(BrowserType.CHROME)
        return chrome_driver

    def get_chromium_driver(self):
        chromium_driver = self.__get_driver(BrowserType.CHROMIUM)
        return chromium_driver

    def get_brave_driver(self):
        brave_driver = self.__get_driver(BrowserType.BRAVE)
        return brave_driver

    def get_firefox_driver(self):
        firefox_driver = self.__get_driver(BrowserType.FIREFOX)
        return firefox_driver

    def get_safari_driver(self):
        safari_driver = self.__get_driver(BrowserType.SAFARI)
        return safari_driver

    def get_edge_driver(self):
        edge_driver = self.__get_driver(BrowserType.EDGE)
        return edge_driver

    def get_ie_driver(self):
        ie_driver = self.__get_driver(BrowserType.IE)
        return ie_driver

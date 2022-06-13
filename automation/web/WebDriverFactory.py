from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import platform
import os


from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager


class WebDriverFactory:

    def __init__(self):
        print("Creating instance of WebDriverFactory.")
        self.driver = None
        os.environ['GH_TOKEN'] = "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"

    def __get_driver(self, driver_name: str):
        self.driver = None
        operating_system = platform.system()
        try:
            match driver_name:
                case "CHROME":
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
                case "CHROMIUM":
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
                case "BRAVE":
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
                case "FIREFOX":
                    self. driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
                case "SAFARI":
                    if operating_system == 'Darwin':
                        self.driver = webdriver.Safari()
                    else:
                        print(operating_system + " is an unsupported Operating System to run Safari Web Driver")
                        exit(1)
                case "EDGE":
                    self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
                case "IE":
                    if operating_system == 'Windows':
                        self.driver = webdriver.Ie(service=Service(IEDriverManager().install()))
                    else:
                        print(operating_system + " is an unsupported Operating System to run Internet Explorer Web Driver")
                        exit(1)
                case default:
                    print("Unsupported Web Driver.")
        except Exception as error_message:
            print("Encountered Exception when trying to get " + driver_name + " Web Driver: " + str(error_message))
            exit(1)
        return self.driver

    def get_chrome_driver(self):
        print("Initializing Google Chrome Web Driver")
        chrome_driver = self.__get_driver("CHROME")
        return chrome_driver

    def get_chromium_driver(self):
        print("Initializing Chromium Web Driver")
        chromium_driver = self.__get_driver("CHROMIUM")
        return chromium_driver

    def get_brave_driver(self):
        print("Initializing Brave Web Driver")
        brave_driver = self.__get_driver("BRAVE")
        return brave_driver

    def get_firefox_driver(self):
        print("Initializing Mozilla Firefox Web Driver")
        firefox_driver = self.__get_driver("FIREFOX")
        return firefox_driver

    def get_safari_driver(self):
        print("Initializing Safari Web Driver")
        safari_driver = self.__get_driver("SAFARI")
        return safari_driver

    def get_edge_driver(self):
        print("Initializing Microsoft Edge Web Driver")
        edge_driver = self.__get_driver("EDGE")
        return edge_driver

    def get_ie_driver(self):
        print("Initializing Internet Explorer Web Driver")
        ie_driver = self.__get_driver("IE")
        return ie_driver

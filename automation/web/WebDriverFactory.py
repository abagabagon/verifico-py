from selenium import webdriver


import platform


class WebDriverFactory:

    def __init__(self):
        print("Creating instance of WebDriverFactory")
        self.driver = None

    def __get_driver(self, driver_name: str):
        self.driver = None
        operating_system = platform.system()
        try:
            match driver_name:
                case "CHROME":
                    self.driver = webdriver.Chrome()
                case "FIREFOX":
                    self. driver = webdriver.Firefox()
                case "SAFARI":
                    if operating_system == 'Darwin':
                        self.driver = webdriver.Safari()
                    else:
                        print(operating_system + " is an unsupported Operating System to run Safari Web Driver")
                        exit(1)
                case "EDGE":
                    self.driver = webdriver.Edge()
                case "IE":
                    if operating_system == 'Windows':
                        self.driver = webdriver.Ie()
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
        chrome_driver = self.__get_driver("CHROME")
        return chrome_driver

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

from selenium import webdriver
from selenium.common import NoSuchWindowException
from selenium.webdriver.common.by import By
import logging


class BrowserCommands:

    def __init__(self, driver: webdriver):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of BrowserCommands.")
        self.driver = driver

    def __execute_browser_action(self, task: str, input_value: str):
        self.log.debug("Performing " + task.replace("_", " ") + " Browser Action.")
        try:
            match task:
                case "OPEN_TAB":
                    self.driver.execute_script("window.open('" + input_value + "', '_blank');")
                case "MAXIMIZE":
                    self.driver.maximize_window()
                case "DELETE_ALL_COOKIES":
                    self.driver.delete_all_cookies()
                case "GO_TO":
                    self.driver.get(input_value)
                case "BACK":
                    self.driver.back()
                case "FORWARD":
                    self.driver.forward()
                case "REFRESH":
                    self.driver.refresh()
                case "CLOSE_TAB":
                    self.driver.close()
                case "CLOSE_BROWSER":
                    self.driver.quit()
                case _:
                    self.log.error(task.replace("_", " ") + " is an unsupported Browser Action.")
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + task.replace("_", " ") + " Web Driver: " + str(error_message))

    def open_tab(self, url: str):
        self.__execute_browser_action("OPEN_TAB", url)

    def maximize(self):
        self.__execute_browser_action("MAXIMIZE", None)

    def delete_all_cookies(self):
        self.__execute_browser_action("DELETE_ALL_COOKIES", None)

    def go_to(self, url: str):
        self.__execute_browser_action("GO_TO", url)

    def back(self):
        self.__execute_browser_action("BACK", None)

    def forward(self):
        self.__execute_browser_action("FORWARD", None)

    def refresh(self):
        self.__execute_browser_action("REFRESH", None)

    def close_tab(self):
        self.__execute_browser_action("CLOSE_TAB", None)

    def close_browser(self):
        self.__execute_browser_action("CLOSE_BROWSER", None)

    def __execute_switch_action(self, task: str, input_value: str):

        for handle in self.driver.window_handles:
            try:
                self.driver.switch_to_window(handle)
                if task.__eq__("TO_DEFAULT"):
                    self.log.debug("Switching tab " + task.replace("_", " "))
                    break
                else:
                    self.log.debug("Switching tab " + task.replace("_", " ") + ": " + input_value)
                match task:
                    case "BY_TITLE":
                        page_title: str = self.driver.title
                        if page_title.__eq__(input_value):
                            self.log.debug("Successfully switched to Window with Title: " + input_value)
                            break
                    case "BY_URL":
                        page_url: str = self.driver.current_url
                        if page_url.__eq__(input_value):
                            self.log.debug("Successfully switched to Window with URL: " + input_value)
                            break
                    case _:
                        self.log.error(task.replace("_", " ") + " is an unsupported Switch Action.")
            except NoSuchWindowException as error_message:
                self.log.warning("Encountered NoSuchWindowException when trying to perform Switch " + task.replace("_", " ") + " Action: " + str(error_message))
            except Exception as error_message:
                self.log.warning("Encountered Exception when trying to perform Switch " + task.replace("_", " ") + " Action: " + str(error_message))

    def switch_tab_by_title(self, title: str):
        self.__execute_switch_action("BY_TITLE", title)

    def switch_tab_by_url(self, url: str):
        self.__execute_switch_action("BY_TITLE", url)

    def switch_tab_to_original(self):
        self.__execute_switch_action("TO_DEFAULT", None)

    def scroll(self, pixel_horizontal: int, pixel_vertical: int):
        self.log.debug("Performing SCROLL Browser Action to coordinates " + pixel_horizontal + ", " + pixel_vertical)
        try:
            self.driver.execute_script("window.scrollBy(" + pixel_horizontal + ", " + pixel_vertical + ")")
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform SCROLL Browser Action: " + str(error_message))

    def count(self, locator: By, value: str):
        self.log.debug("Performing Element Count.")
        elements = self.driver.find_elements(locator, value);
        count = len(elements)
        return count

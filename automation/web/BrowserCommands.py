from selenium import webdriver
from selenium.common import NoSuchWindowException
from selenium.webdriver.common.by import By
import logging
from enum import Enum, auto


class BrowserAction(Enum):
    OPEN_TAB = auto()
    MAXIMIZE = auto()
    DELETE_ALL_COOKIES = auto()
    GO_TO = auto()
    BACK = auto()
    FORWARD = auto()
    REFRESH = auto()
    CLOSE_TAB = auto()
    CLOSE_BROWSER = auto()


class SwitchAction(Enum):
    TO_DEFAULT = auto()
    BY_TITLE = auto()
    BY_URL = auto()


class BrowserCommands:

    def __init__(self, driver: webdriver):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of BrowserCommands.")
        self.driver = driver

    def __execute_browser_action(self, action: BrowserAction, input_value: str):
        local_task = str(action).replace("_", " ")
        self.log.debug("Performing " + local_task + " Browser Action.")
        try:
            match action:
                case BrowserAction.OPEN_TAB:
                    self.driver.execute_script("window.open('" + input_value + "', '_blank');")
                case BrowserAction.MAXIMIZE:
                    self.driver.maximize_window()
                case BrowserAction.DELETE_ALL_COOKIES:
                    self.driver.delete_all_cookies()
                case BrowserAction.GO_TO:
                    self.driver.get(input_value)
                case BrowserAction.BACK:
                    self.driver.back()
                case BrowserAction.FORWARD:
                    self.driver.forward()
                case BrowserAction.REFRESH:
                    self.driver.refresh()
                case BrowserAction.CLOSE_TAB:
                    self.driver.close()
                case BrowserAction.CLOSE_BROWSER:
                    self.driver.quit()
                case _:
                    self.log.error(local_task + " is an unsupported Browser Action.")
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + local_task + " Web Driver: " + str(error_message))

    def open_tab(self, url: str):
        self.__execute_browser_action(BrowserAction.OPEN_TAB, url)

    def maximize(self):
        self.__execute_browser_action(BrowserAction.MAXIMIZE, None)

    def delete_all_cookies(self):
        self.__execute_browser_action(BrowserAction.DELETE_ALL_COOKIES, None)

    def go_to(self, url: str):
        self.__execute_browser_action(BrowserAction.GO_TO, url)

    def back(self):
        self.__execute_browser_action(BrowserAction.BACK, None)

    def forward(self):
        self.__execute_browser_action(BrowserAction.FORWARD, None)

    def refresh(self):
        self.__execute_browser_action(BrowserAction.REFRESH, None)

    def close_tab(self):
        self.__execute_browser_action(BrowserAction.CLOSE_TAB, None)

    def close_browser(self):
        self.__execute_browser_action(BrowserAction.CLOSE_BROWSER, None)

    def __execute_switch_action(self, action: SwitchAction, input_value: str):
        local_task = str(action).replace("_", " ")
        for handle in self.driver.window_handles:
            try:
                self.driver.switch_to_window(handle)
                if action == SwitchAction.TO_DEFAULT:
                    self.log.debug("Switching tab " + local_task)
                    break
                else:
                    self.log.debug("Switching tab " + local_task + ": " + input_value)
                match action:
                    case SwitchAction.BY_TITLE:
                        page_title: str = self.driver.title
                        if page_title.__eq__(input_value):
                            self.log.debug("Successfully switched to Window with Title: " + input_value)
                            break
                    case SwitchAction.BY_URL:
                        page_url: str = self.driver.current_url
                        if page_url.__eq__(input_value):
                            self.log.debug("Successfully switched to Window with URL: " + input_value)
                            break
                    case _:
                        self.log.error(local_task + " is an unsupported Switch Action.")
            except NoSuchWindowException as error_message:
                self.log.warning("Encountered NoSuchWindowException when trying to perform Switch " + local_task + " Action: " + str(error_message))
            except Exception as error_message:
                self.log.warning("Encountered Exception when trying to perform Switch " + local_task + " Action: " + str(error_message))

    def switch_tab_by_title(self, title: str):
        self.__execute_switch_action(SwitchAction.BY_TITLE, title)

    def switch_tab_by_url(self, url: str):
        self.__execute_switch_action(SwitchAction.BY_URL, url)

    def switch_tab_to_original(self):
        self.__execute_switch_action(SwitchAction.TO_DEFAULT, None)

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

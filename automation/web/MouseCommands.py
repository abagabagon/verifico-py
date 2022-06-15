from selenium.common import StaleElementReferenceException, ElementClickInterceptedException, MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from automation.web.WaitCommands import WaitCommands
from automation.web.WebElementFactory import WebElementFactory
from time import sleep
from enum import Enum, auto
import logging


class MouseAction(Enum):
    CLICK = auto()
    CLICK_JS = auto()
    CLICK_AND_HOLD = auto()
    DOUBLE_CLICK = auto()
    POINT = auto()


class MouseCommands:

    def __init__(self, driver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of MouseCommands.")
        self.driver = driver
        self.wait = wait
        self.action_chains = ActionChains(self.driver)
        self.element_factory = WebElementFactory(self.driver, self.wait)

    def __execute(self, action: MouseAction, element: WebElement):
        local_task = str(action).replace("_", " ").title()
        action_performed = False
        try:
            match action:
                case MouseAction.CLICK:
                    element.click()
                case MouseAction.CLICK_JS:
                    self.driver.execute_script("arguments[0].click();", element)
                case MouseAction.CLICK_AND_HOLD:
                    self.action_chains.click_and_hold(element)
                case MouseAction.DOUBLE_CLICK:
                    self.action_chains.double_click(element)
                case MouseAction.POINT:
                    self.action_chains.move_to_element(element)
                case _:
                    self.log.error(local_task + " is an unsupported Mouse Action.")
            action_performed = True
        except StaleElementReferenceException as error_message:
            self.log.warning("Encountered StaleElementReferenceException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        except ElementClickInterceptedException as error_message:
            self.log.warning("Encountered ElementClickInterceptedException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
            self.action_chains.move_to_element(element)
        except MoveTargetOutOfBoundsException as error_message:
            self.log.warning("Encountered MoveTargetOutOfBoundsException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
            self.action_chains.move_to_element(element)
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        return action_performed

    def __do_command(self, action: MouseAction, locator: By, value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Web Element " + value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Mouse Action " + local_task + " to Web Element " + value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Mouse Action " + local_task + " to Web Element " + value + ".")
            else:
                break

    def click(self, locator: By, value: str):
        self.__do_command(MouseAction.CLICK, locator, value)

    def click_js(self, locator: By, value: str):
        self.__do_command(MouseAction.CLICK_JS, locator, value)

    def click_and_hold(self, locator: By, value: str):
        self.__do_command(MouseAction.CLICK_AND_HOLD, locator, value)

    def double_click(self, locator: By, value: str):
        self.__do_command(MouseAction.DOUBLE_CLICK, locator, value)

    def point(self, locator: By, value: str):
        self.__do_command(MouseAction.POINT, locator, value)

    def __do_command(self, action: MouseAction, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_value, child_locator, child_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Mouse Action " + local_task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Mouse Action " + local_task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
            else:
                break

    def click(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command(MouseAction.CLICK, parent_locator, parent_value, child_locator, child_value)

    def click_js(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command(MouseAction.CLICK_JS, parent_locator, parent_value, child_locator, child_value)

    def click_and_hold(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command(MouseAction.CLICK_AND_HOLD, parent_locator, parent_value, child_locator, child_value)

    def double_click(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command(MouseAction.DOUBLE_CLICK, parent_locator, parent_value, child_locator, child_value)

    def point(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command(MouseAction.POINT, parent_locator, parent_value, child_locator, child_value)

    def __do_command(self, action: MouseAction, parent_element: WebElement, child_locator: By, child_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Mouse Action " + local_task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Mouse Action " + local_task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break

    def click(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command(MouseAction.CLICK, parent_element, child_locator, child_value)

    def click_js(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command(MouseAction.CLICK_JS, parent_element, child_locator, child_value)

    def click_and_hold(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command(MouseAction.CLICK_AND_HOLD, parent_element, child_locator, child_value)

    def double_click(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command(MouseAction.DOUBLE_CLICK, parent_element, child_locator, child_value)

    def point(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command(MouseAction.POINT, parent_element, child_locator, child_value)

from selenium.common import StaleElementReferenceException, UnexpectedTagNameException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from automation.web.WaitCommands import WaitCommands
from automation.web.WebElementFactory import WebElementFactory
from enum import Enum, auto
from time import sleep
import logging


class SelectAction(Enum):
    SELECT = auto()
    DESELECT = auto()


class SelectCommands:

    def __init__(self, driver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of SelectCommands.")
        self.driver = driver
        self.wait = wait
        self.element_factory = WebElementFactory(self.driver, self.wait)

    def __execute(self, action: SelectAction, element: WebElement, input_option: str):
        action_performed = False
        log_task = str(action).replace("_", " ").title()
        try:
            select = Select(element)
            option_ticked = False
            for option in select.options:
                if input_option.__eq__(option):
                    match action:
                        case SelectAction.SELECT:
                            select.select_by_visible_text(input_option)
                        case SelectAction.DESELECT:
                            select.deselect_by_visible_text(input_option)
                        case _:
                            self.log.error(log_task + " is an unsupported Select Action.")
                    break
            if option_ticked:
                self.log.error("Failed to select an option. Option " + option + " is invalid!")
            action_performed = True
        except StaleElementReferenceException as error_message:
            self.log.warning("Encountered StaleElementReferenceException when trying to perform task " + log_task + " Web Driver: " + str(error_message))
        except UnexpectedTagNameException as error_message:
            self.log.warning("Encountered UnexpectedTagNameException when trying to perform task " + log_task + " Web Driver: " + str(error_message))
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + log_task + " Web Driver: " + str(error_message))
        return action_performed

    def __do_command(self, action: SelectAction, locator: By, value: str, input_option: str):
        log_task = str(action).replace("_", " ").title()
        self.log.debug(log_task + "ing the option: " + input_option + " from the Web Element " + value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Select Action " + log_task + " to Web Element " + value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Select Action " + log_task + " to Web Element " + value + ".")
            else:
                break

    def select(self, locator: By, value: str, input_option: str):
        self.__do_command(SelectAction.SELECT, locator, value, input_option)

    def deselect(self, locator: By, value: str, input_option: str):
        self.__do_command(SelectAction.DESELECT, locator, value, input_option)

    def __do_command(self, action: SelectAction, parent_locator: By, parent_value: str, child_locator: By, child_value: str, input_option: str):
        log_task = str(action).replace("_", " ").title()
        self.log.debug(log_task + "ing the option: " + input_option + " from the Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_value, child_locator, child_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Select Action " + log_task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Select Action " + log_task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
            else:
                break

    def select(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str, input_option: str):
        self.__do_command(SelectAction.SELECT, parent_locator, parent_value, child_locator, child_value, input_option)

    def deselect(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str, input_option: str):
        self.__do_command(SelectAction.DESELECT, parent_locator, parent_value, child_locator, child_value, input_option)

    def __do_command(self, action: SelectAction, parent_element: WebElement, child_locator: By, child_value: str, input_option: str):
        log_task = str(action).replace("_", " ").title()
        self.log.debug(log_task + "ing the option: " + input_option + " from the Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Select Action " + log_task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Select Action " + log_task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break

    def select(self, parent_element: WebElement, child_locator: By, child_value: str, input_option: str):
        self.__do_command(SelectAction.SELECT, parent_element, child_locator, child_value, input_option)

    def deselect(self, parent_element: WebElement, child_locator: By, child_value: str, input_option: str):
        self.__do_command(SelectAction.DESELECT, parent_element, child_locator, child_value, input_option)

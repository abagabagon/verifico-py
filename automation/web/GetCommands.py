from selenium.common import StaleElementReferenceException, UnexpectedTagNameException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from automation.web.WaitCommands import WaitCommands
from automation.web.WebElementFactory import WebElementFactory
from time import sleep
import logging


class GetCommands:

    def __init__(self, driver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of GetCommands.")
        self.driver = driver
        self.wait = wait
        self.action_chains = ActionChains(self.driver)
        self.element_factory = WebElementFactory(self.driver, self.wait)
        self.retrieved_value = None

    def __execute(self, task: str, element: WebElement, attribute: str):
        action_performed = False
        self.retrieved_value = None
        try:
            match task:
                case "GET_ATTRIBUTE":
                    self.retrieved_value = element.get_attribute(attribute)
                case "GET_DROPDOWN":
                    select = Select(element)
                    self.retrieved_value = select.first_selected_option
                case "GET_TEXT":
                    self.retrieved_value = element.text
                case _:
                    self.log.error(task.replace("_", " ") + " is an unsupported Get Action.")
            action_performed = True
        except StaleElementReferenceException as error_message:
            self.log.warning("Encountered StaleElementReferenceException when trying to perform task " + task.replace("_", " ") + " Web Driver: " + str(error_message))
        except UnexpectedTagNameException as error_message:
            self.log.warning("Encountered UnexpectedTagNameException when trying to perform task " + task.replace("_", " ") + " Web Driver: " + str(error_message))
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + task.replace("_", " ") + " Web Driver: " + str(error_message))
        return action_performed

    def __do_command(self, task: str, locator: By, value: str, attribute: str):
        self.log.debug("Performing " + task.replace("_", " ") + " to the Web Element " + value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, value)
            action_performed = self.__execute(task, element, attribute)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Get Action " + task.replace("_", " ") + " for Web Element " + value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Get Action " + task.replace("_", " ") + " for Web Element " + value + ".")
            else:
                break
        return self.retrieved_value

    def get_text(self, locator: By, value: str):
        text = self.__do_command(locator, value, None)
        return text

    def get_attribute(self, locator: By, value: str, attribute: str):
        attribute_value = self.__do_command(locator, value, attribute)
        return attribute_value

    def get_dropdown_value(self, locator: By, value: str):
        dropdown_value = self.__do_command(locator, value, None)
        return dropdown_value

    def __do_command(self, task: str, parent_locator: By, parent_value: str, child_locator: By, child_value: str, attribute: str):
        self.log.debug("Performing " + task.replace("_", " ") + " to the Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_value, child_locator, child_value)
            action_performed = self.__execute(task, element, attribute)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Get Action " + task.replace("_", " ") + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Get Action " + task.replace("_", " ") + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
            else:
                break
        return self.retrieved_value

    def get_text(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        text = self.__do_command(parent_locator, parent_value, child_locator, child_value, None)
        return text

    def get_attribute(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str, attribute: str):
        attribute_value = self.__do_command(parent_locator, parent_value, child_locator, child_value, attribute)
        return attribute_value

    def get_dropdown_value(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        dropdown_value = self.__do_command(parent_locator, parent_value, child_locator, child_value, None)
        return dropdown_value

    def __do_command(self, task: str, parent_element, child_locator: By, child_value: str, attribute: str):
        self.log.debug("Performing " + task.replace("_", " ") + " to the Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_value)
            action_performed = self.__execute(task, element, attribute)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Get Action " + task.replace("_", " ") + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Get Action " + task.replace("_", " ") + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break
        return self.retrieved_value

    def get_text(self, parent_element: WebElement, child_locator: By, child_value: str):
        text = self.__do_command(parent_element, child_locator, child_value, None)
        return text

    def get_attribute(self, parent_element: WebElement, child_locator: By, child_value: str, attribute: str):
        attribute_value = self.__do_command(parent_element, child_locator, child_value, attribute)
        return attribute_value

    def get_dropdown_value(self, parent_element: WebElement, child_locator: By, child_value: str):
        dropdown_value = self.__do_command(parent_element, child_locator, child_value, None)
        return dropdown_value

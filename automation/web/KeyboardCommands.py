import logging

from selenium.common import StaleElementReferenceException, ElementNotInteractableException, InvalidElementStateException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from automation.web.WaitCommands import WaitCommands
from automation.web.WebElementFactory import WebElementFactory
from time import sleep
import platform
import logging


class KeyboardCommands:

    def __init__(self, driver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of KeyboardCommands.")
        self.driver = driver
        self.wait = wait
        self.action_chains = ActionChains(self.driver)
        self.element_factory = WebElementFactory(self.driver, self.wait)

    def __execute(self, task: str, element: WebElement, input_text: str, key_button: Keys):
        action_performed = False
        operating_system = platform.system()
        try:
            match task:
                case "CLEAR":
                    if operating_system.__eq__("Darwin"):
                        self.action_chains.click(element)\
                            .pause(200).keyDown(Keys.COMMAND).sendKeys("a").keyUp(Keys.COMMAND)\
                            .pause(200).sendKeys(Keys.DELETE).perform()
                    else:
                        self.action_chains.click(element)\
                            .pause(200).keyDown(Keys.CONTROL).sendKeys("a").keyUp(Keys.CONTROL)\
                            .pause(200).sendKeys(Keys.DELETE).perform()
                case "PRESS":
                    element.send_keys(key_button)
                case "TYPE":
                    element.send_keys(input_text)
                case _:
                    self.log.error(task + " is an unsupported Keyboard Action.")
            action_performed = True
        except StaleElementReferenceException as error_message:
            self.log.warning("Encountered StaleElementReferenceException when trying to perform task " + task + " Web Driver: " + str(error_message))
        except ElementNotInteractableException as error_message:
            self.log.warning("Encountered ElementNotInteractableException when trying to perform task " + task + " Web Driver: " + str(error_message))
            element.click()
        except InvalidElementStateException as error_message:
            self.log.warning("Encountered InvalidElementStateException when trying to perform task " + task + " Web Driver: " + str(error_message))
            element.click()
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + task + " Web Driver: " + str(error_message))
        return action_performed

    def __do_command(self, task: str, locator: By, value: str, input_text: str, key_button: Keys):
        self.log.debug("Performing " + task + " to the Web Element " + value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, value)
            action_performed = self.__execute(task, element, input_text, key_button)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Keyboard Action " + task + " for Web Element " + value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Keyboard Action " + task + " for Web Element " + value + ".")
            else:
                break

    def clear(self, locator: By, value: str):
        self.__do_command("CLEAR", locator, value, None, None)

    def type(self, locator: By, value: str, input_text: str):
        self.__do_command("TYPE", locator, value, input_text, None)

    def press(self, locator: By, value: str, key_button: Keys):
        self.__do_command("PRESS", locator, value, None, key_button)

    def __do_command(self, task: str, parent_locator: By, parent_value: str, child_locator: By, child_value: str, input_text: str, key_button: Keys):
        self.log.debug("Performing " + task + " to the Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_value, child_locator, child_value)
            action_performed = self.__execute(task, element, input_text, key_button)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Keyboard Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Keyboard Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
            else:
                break

    def clear(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command("CLEAR", parent_locator, parent_value, child_locator, child_value, None, None)

    def type(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str, input_text: str):
        self.__do_command("TYPE", parent_locator, parent_value, child_locator, child_value, input_text, None)

    def press(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str, key_button: Keys):
        self.__do_command("PRESS", parent_locator, parent_value, child_locator, child_value, None, key_button)

    def __do_command(self, task: str, parent_element: WebElement, child_locator: By, child_value: str, input_text: str, key_button: Keys):
        self.log.debug("Performing " + task + " to the Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_value)
            action_performed = self.__execute(task, element, input_text, key_button)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Keyboard Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Keyboard Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break

    def clear(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command("CLEAR", parent_element, child_locator, child_value, None, None)

    def type(self, parent_element: WebElement, child_locator: By, child_value: str, input_text: str):
        self.__do_command("TYPE", parent_element, child_locator, child_value, input_text, None)

    def press(self, parent_element: WebElement, child_locator: By, child_value: str, key_button: Keys):
        self.__do_command("PRESS", parent_element, child_locator, child_value, None, key_button)

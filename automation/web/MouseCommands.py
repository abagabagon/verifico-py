from selenium.common import StaleElementReferenceException, ElementClickInterceptedException, MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from automation.web.WaitCommands import WaitCommands
from automation.web.WebElementFactory import WebElementFactory
from time import sleep


class MouseCommands:

    def __init__(self, driver, wait: WaitCommands):
        print("Creating instance of MouseCommands.")
        self.driver = driver
        self.wait = wait
        self.action_chains = ActionChains(self.driver)
        self.element_factory = WebElementFactory(self.driver, self.wait)

    def __execute(self, task: str, element: WebElement):
        action_performed = False
        try:
            match task:
                case "CLICK":
                    element.click()
                case "CLICK_JS":
                    self.driver.execute_script("arguments[0].click();", element)
                case "CLICK_AND_HOLD":
                    self.action_chains.click_and_hold(element)
                case "DOUBLE_CLICK":
                    self.action_chains.double_click(element)
                case "POINT":
                    self.action_chains.move_to_element(element)
                case _:
                    print(task + " is an unsupported Mouse Action.")
            action_performed = True
        except StaleElementReferenceException as error_message:
            print("Encountered StaleElementReferenceException when trying to perform task " + task + " Web Driver: " + str(error_message))
        except ElementClickInterceptedException as error_message:
            print("Encountered ElementClickInterceptedException when trying to perform task " + task + " Web Driver: " + str(error_message))
            self.action_chains.move_to_element(element)
        except MoveTargetOutOfBoundsException as error_message:
            print("Encountered MoveTargetOutOfBoundsException when trying to perform task " + task + " Web Driver: " + str(error_message))
            self.action_chains.move_to_element(element)
        except Exception as error_message:
            print("Encountered Exception when trying to perform task " + task + " Web Driver: " + str(error_message))
        return action_performed

    def __do_command(self, task: str, locator: By, value: str):
        print("Performing " + task + " to the Web Element " + value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, value)
            action_performed = self.__execute(task, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    print("Retrying Mouse Action " + task + " to Web Element " + value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    print("Failed to perform Mouse Action " + task + " to Web Element " + value + ".")
            else:
                break

    def click(self, locator: By, value: str):
        self.__do_command("CLICK", locator, value)

    def click_js(self, locator: By, value: str):
        self.__do_command("CLICK_JS", locator, value)

    def click_and_hold(self, locator: By, value: str):
        self.__do_command("CLICK_AND_HOLD", locator, value)

    def double_click(self, locator: By, value: str):
        self.__do_command("DOUBLE_CLICK", locator, value)

    def point(self, locator: By, value: str):
        self.__do_command("POINT", locator, value)

    def __do_command(self, task: str, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        print("Performing " + task + " to the Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_value, child_locator, child_value)
            action_performed = self.__execute(task, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    print("Retrying Mouse Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    print("Failed to perform Mouse Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + parent_value + ".")
            else:
                break

    def click(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command("CLICK", parent_locator, parent_value, child_locator, child_value)

    def click_js(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command("CLICK_JS", parent_locator, parent_value, child_locator, child_value)

    def click_and_hold(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command("CLICK_AND_HOLD", parent_locator, parent_value, child_locator, child_value)

    def double_click(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command("DOUBLE_CLICK", parent_locator, parent_value, child_locator, child_value)

    def point(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__do_command("POINT", parent_locator, parent_value, child_locator, child_value)

    def __do_command(self, task: str, parent_element: WebElement, child_locator: By, child_value: str):
        print("Performing " + task + " to the Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_value)
            action_performed = self.__execute(task, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    print("Retrying Mouse Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    print("Failed to perform Mouse Action " + task + " to Child Web Element " + child_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break

    def click(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command("CLICK", parent_element, child_locator, child_value)

    def click_js(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command("CLICK_JS", parent_element, child_locator, child_value)

    def click_and_hold(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command("CLICK_AND_HOLD", parent_element, child_locator, child_value)

    def double_click(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command("DOUBLE_CLICK", parent_element, child_locator, child_value)

    def point(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__do_command("POINT", parent_element, child_locator, child_value)

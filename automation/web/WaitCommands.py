from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from enum import Enum, auto
import logging


class WaitAction(Enum):
    URL_TO_MATCH = auto()
    URL_TO_CONTAIN = auto()
    TITLE_TO_MATCH = auto()
    TITLE_TO_CONTAIN = auto()
    ELEMENT_TO_BE_PRESENT = auto()
    ELEMENT_TO_BE_VISIBLE = auto()
    ELEMENT_TO_BE_INVISIBLE = auto()
    ELEMENT_TO_BE_CLICKABLE = auto()
    ELEMENTS_TO_BE_PRESENT = auto()
    ELEMENTS_TO_BE_VISIBLE = auto()
    TEXT_TO_MATCH = auto()
    ALERT_TO_BE_PRESENT = auto()
    ATTRIBUTE_TO_MATCH = auto()


class WaitCommands:

    def __init__(self, driver, implicit_wait_duration, explicit_wait_duration: int):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of WaitCommands.")
        self.element = None
        self.driver = driver
        self.implicit_wait_duration = implicit_wait_duration
        self.explicit_wait_duration = explicit_wait_duration
        self.driver.implicitly_wait(self.implicit_wait_duration)
        self.wait = WebDriverWait(self.driver, explicit_wait_duration)

    def set_implicit_wait(self, implicit_wait_duration: int):
        self.log.debug("Setting Implicit Wait to " + implicit_wait_duration)
        self.driver.implicitly_wait(implicit_wait_duration)

    def set_explicit_wait(self, explicit_wait_duration: int):
        self.log.debug("Setting Explicit Wait to " + explicit_wait_duration)
        self.wait = WebDriverWait(self.driver, explicit_wait_duration)

    def __execute(self, action: WaitAction, check_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + local_task + " specified value: " + check_value)
        status = False
        try:
            match action:
                case WaitAction.URL_TO_MATCH:
                    status = self.wait.until(expected_conditions.url_to_be(check_value))
                case WaitAction.URL_TO_CONTAIN:
                    status = self.wait.until(expected_conditions.url_contains(check_value))
                case WaitAction.TITLE_TO_MATCH:
                    status = self.wait.until(expected_conditions.title_is(check_value))
                case WaitAction.TITLE_TO_CONTAIN:
                    status = self.wait.until(expected_conditions.title_contains(check_value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + local_task + " specified value: " + check_value + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + local_task + " specified value: " + check_value + ": " + str(error_message))
        return status

    def wait_for_to_be(self, url: str):
        status = self.__execute(WaitAction.URL_TO_MATCH, url)
        return status

    def wait_for_url_to_contain(self, url: str):
        status = self.__execute(WaitAction.URL_TO_CONTAIN, url)
        return status

    def wait_for_title_to_be(self, title: str):
        status = self.__execute(WaitAction.TITLE_TO_MATCH, title)
        return status

    def wait_for_title_to_contain(self, title: str):
        status: bool = self.__execute(WaitAction.TITLE_TO_CONTAIN, title)
        return status

    def __execute(self, action: WaitAction, locator: By, value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + value + " " + local_task + ".")
        element = None
        try:
            match str:
                case WaitAction.ELEMENT_TO_BE_PRESENT:
                    element = self.wait.until(expected_conditions.presence_of_element_located(locator, value))
                case WaitAction.ELEMENT_TO_BE_VISIBLE:
                    element = self.wait.until(expected_conditions.visibility_of_element_located(locator, value))
                case WaitAction.ELEMENT_TO_BE_INVISIBLE:
                    self.wait.until(expected_conditions.invisibility_of_element_located(locator, value))
                case WaitAction.ELEMENT_TO_BE_CLICKABLE:
                    element = self.wait.until(expected_conditions.element_to_be_clickable(locator, value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + local_task + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + local_task + ": " + str(error_message))
        return element

    def wait_for_element_to_be_present(self, locator: By, value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_PRESENT, locator, value)
        return element

    def wait_for_element_to_be_visible(self, locator: By, value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_VISIBLE, locator, value)
        return element

    def wait_for_element_to_be_invisible(self, locator: By, value: str):
        self.__execute(WaitAction.ELEMENT_TO_BE_INVISIBLE, locator, value)

    def wait_for_element_to_be_clickable(self, locator: By, value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_CLICKABLE, locator, value)
        return element

    def __execute(self, action: WaitAction, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + parent_value + ".")
        child_element = None
        try:
            parent_element = self.wait.until(expected_conditions.presence_of_element_located(parent_locator, parent_value))
            local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
            match str:
                case WaitAction.ELEMENT_TO_BE_PRESENT:
                    child_element = local_wait.until(expected_conditions.presence_of_element_located(child_locator, child_value))
                case WaitAction.ELEMENT_TO_BE_VISIBLE:
                    child_element = local_wait.until(expected_conditions.visibility_of_element_located(child_locator, child_value))
                case WaitAction.ELEMENT_TO_BE_INVISIBLE:
                    local_wait.until(expected_conditions.invisibility_of_element_located(child_locator, child_value))
                case WaitAction.ELEMENT_TO_BE_CLICKABLE:
                    child_element = local_wait.until(expected_conditions.element_to_be_clickable(child_locator, child_value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + parent_value + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + parent_value + ": " + str(error_message))
        return child_element

    def wait_for_element_to_be_present(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_PRESENT, parent_locator, parent_value, child_locator, child_value)
        return element

    def wait_for_element_to_be_visible(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_VISIBLE, parent_locator, parent_value, child_locator, child_value)
        return element

    def wait_for_element_to_be_invisible(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        self.__execute(WaitAction.ELEMENT_TO_BE_INVISIBLE, parent_locator, parent_value, child_locator, child_value)

    def wait_for_element_to_be_clickable(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_CLICKABLE, parent_locator, parent_value, child_locator, child_value)
        return element

    def __execute(self, action: WaitAction, parent_element: WebElement, child_locator: By, child_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + str(parent_element) + ".")
        child_element = None
        try:
            local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
            match str:
                case WaitAction.ELEMENT_TO_BE_PRESENT:
                    child_element = local_wait.until(expected_conditions.presence_of_element_located(child_locator, child_value))
                case WaitAction.ELEMENT_TO_BE_VISIBLE:
                    child_element = local_wait.until(expected_conditions.visibility_of_element_located(child_locator, child_value))
                case WaitAction.ELEMENT_TO_BE_INVISIBLE:
                    local_wait.until(expected_conditions.invisibility_of_element_located(child_locator, child_value))
                case WaitAction.ELEMENT_TO_BE_CLICKABLE:
                    child_element = local_wait.until(expected_conditions.element_to_be_clickable(child_locator, child_value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + str(parent_element) + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + str(parent_element) + ": " + str(error_message))
        return child_element

    def wait_for_element_to_be_present(self, parent_element: WebElement, child_locator: By, child_value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_PRESENT, parent_element, child_locator, child_value)
        return element

    def wait_for_element_to_be_visible(self, parent_element: WebElement, child_locator: By, child_value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_VISIBLE, parent_element, child_locator, child_value)
        return element

    def wait_for_element_to_be_invisible(self, parent_element: WebElement, child_locator: By, child_value: str):
        self.__execute(WaitAction.ELEMENT_TO_BE_INVISIBLE, parent_element, child_locator, child_value)

    def wait_for_element_to_be_clickable(self, parent_element: WebElement, child_locator: By, child_value: str):
        element = self.__execute(WaitAction.ELEMENT_TO_BE_CLICKABLE, parent_element, child_locator, child_value)
        return element

    def __execute(self, action: WaitAction, locator: By, value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + value + " " + local_task + ".")
        try:
            match str:
                case WaitAction.ELEMENTS_TO_BE_PRESENT:
                    elements = self.wait.until(expected_conditions.presence_of_all_elements_located(locator, value))
                case WaitAction.ELEMENTS_TO_BE_VISIBLE:
                    elements = self.wait.until(expected_conditions.visibility_of_all_elements_located(locator, value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + local_task + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + local_task + ": " + str(error_message))
        return elements

    def wait_for_elements_to_be_present(self, locator: By, value: str):
        elements = self.__execute(WaitAction.ELEMENTS_TO_BE_PRESENT, locator, value)
        return elements

    def wait_for_elements_to_be_visible(self, locator: By, value: str):
        elements = self.__execute(WaitAction.ELEMENTS_TO_BE_VISIBLE, locator, value)
        return elements

    def __execute(self, action: WaitAction, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + parent_value + ".")
        try:
            parent_element = self.wait.until(expected_conditions.presence_of_element_located(parent_locator, parent_value))
            local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
            match str:
                case WaitAction.ELEMENTS_TO_BE_PRESENT:
                    child_elements = local_wait.until(expected_conditions.presence_of_all_elements_located(child_locator, child_value))
                case WaitAction.ELEMENTS_TO_BE_VISIBLE:
                    child_elements = local_wait.until(expected_conditions.visibility_of_all_elements_located(child_locator, child_value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + parent_value + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + parent_value + ": " + str(error_message))
        return child_elements

    def wait_for_elements_to_be_present(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        elements = self.__execute(WaitAction.ELEMENTS_TO_BE_PRESENT, parent_locator, parent_value, child_locator, child_value)
        return elements

    def wait_for_elements_to_be_visible(self, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        elements = self.__execute(WaitAction.ELEMENTS_TO_BE_VISIBLE, parent_locator, parent_value, child_locator, child_value)
        return elements

    def __execute(self, action: WaitAction, parent_element: WebElement, child_locator: By, child_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + str(parent_element) + ".")
        try:
            local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
            match str:
                case WaitAction.ELEMENTS_TO_BE_PRESENT:
                    child_elements = local_wait.until(expected_conditions.presence_of_element_located(child_locator, child_value))
                case WaitAction.ELEMENTS_TO_BE_VISIBLE:
                    child_elements = local_wait.until(expected_conditions.visibility_of_element_located(child_locator, child_value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + str(parent_element) + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + child_value + " CHILD " + local_task + " under PARENT ELEMENT " + str(parent_element) + ": " + str(error_message))
        return child_elements

    def wait_for_elements_to_be_present(self, parent_element: WebElement, child_locator: By, child_value: str):
        elements = self.__execute(WaitAction.ELEMENT_TO_BE_PRESENT, parent_element, child_locator, child_value)
        return elements

    def wait_for_elements_to_be_visible(self, parent_element: WebElement, child_locator: By, child_value: str):
        elements = self.__execute(WaitAction.ELEMENT_TO_BE_VISIBLE, parent_element, child_locator, child_value)
        return elements

    def __execute(self, action: WaitAction, locator: By, value: str, attribute: str, check_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Waiting for " + value + " " + local_task + ".")
        element = None
        try:
            match str:
                case WaitAction.ATTRIBUTE_TO_MATCH:
                    element = self.wait.until(expected_conditions.text_to_be_present_in_element_attribute((locator, value), attribute, check_value))
                case WaitAction.TEXT_TO_MATCH:
                    self.wait.until(expected_conditions.text_to_be_present_in_element((locator, value), check_value))
                case _:
                    self.log.error(local_task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for " + local_task + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for " + local_task + ": " + str(error_message))
        return element

    def wait_for_attribute_to_be(self, locator: By, value: str, attribute: str, check_value: str):
        self.__execute(WaitAction.ATTRIBUTE_TO_MATCH, locator, value, attribute, check_value)

    def wait_for_text_to_be(self, locator: By, value: str, check_value: str):
        self.__execute(WaitAction.TEXT_TO_MATCH, locator, value, None, check_value)

    def wait_for_alert_to_be_present(self):
        self.log.debug("Waiting for Javascript " + str(WaitAction.ALERT_TO_BE_PRESENT).replace("_", " ").title() + ".")
        try:
            alert = self.wait.until(expected_conditions.alert_is_present())
        except TimeoutException as error_message:
            self.log.error("Encountered TimeoutException when trying to wait for Javascript " + str(WaitAction.ALERT_TO_BE_PRESENT).replace("_", " ").title() + ": " + str(error_message))
        except Exception as error_message:
            self.log.error("Encountered Exception when trying to wait for Javascript " + str(WaitAction.ALERT_TO_BE_PRESENT).replace("_", " ").title() + ": " + str(error_message))
        return alert

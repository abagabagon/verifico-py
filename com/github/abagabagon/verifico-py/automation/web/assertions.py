import logging
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from selenium_utils import WaitCommands, WebElementFactory
from enum import Enum, auto


class ValueAssertion(Enum):
    URL = auto()
    PARTIAL_URL = auto()
    TITLE = auto()
    PARTIAL_TITLE = auto()
    ATTRIBUTE = auto()
    PARTIAL_ATTRIBUTE = auto()
    DROPDOWN = auto()
    PARTIAL_DROPDOWN = auto()
    TEXT = auto()
    PARTIAL_TEXT = auto()
    ALERT_MESSAGE = auto()


class ValueAssertions:

    actual_value: str

    def __init__(self, driver: webdriver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.driver = driver
        self.wait = wait
        self.element_factory = WebElementFactory(self.driver, self.wait)

    def __execute(self, assertion: ValueAssertion, element: WebElement, attribute: str, input_value: str):
        local_task = str(assertion).replace("_", " ").title()
        select: Select
        status: bool = False
        try:
            match assertion:
                case ValueAssertion.URL:
                    self.actual_value = self.driver.current_url.strip()
                    status = self.actual_value.__eq__(input_value)
                case ValueAssertion.PARTIAL_URL:
                    self.actual_value = self.driver.current_url.strip()
                    status = input_value in self.actual_value
                case ValueAssertion.TITLE:
                    self.actual_value = self.driver.title.strip()
                    status = self.actual_value.__eq__(input_value)
                case ValueAssertion.PARTIAL_TITLE:
                    self.actual_value = self.driver.title.strip()
                    status = input_value in self.actual_value
                case ValueAssertion.ATTRIBUTE:
                    self.actual_value = element.get_attribute(attribute)
                    if self.actual_value is None:
                        status = self.actual_value.__eq__(input_value)
                    else:
                        status = False
                case ValueAssertion.PARTIAL_ATTRIBUTE:
                    self.actual_value = element.get_attribute(attribute)
                    if self.actual_value is None:
                        status = input_value in self.actual_value
                    else:
                        status = False
                case ValueAssertion.DROPDOWN:
                    select = Select(element)
                    self.actual_value = select.first_selected_option.strip()
                    status = self.actual_value.__eq__(input_value)
                case ValueAssertion.PARTIAL_DROPDOWN:
                    select = Select(element)
                    self.actual_value = select.first_selected_option.strip()
                    status = input_value in self.actual_value
                case ValueAssertion.TEXT:
                    self.actual_value = element.text
                    status = self.actual_value.__eq__(input_value)
                case ValueAssertion.PARTIAL_TEXT:
                    self.actual_value = element.text
                    status = input_value in self.actual_value
                case ValueAssertion.ALERT_MESSAGE:
                    alert: Alert = self.wait.wait_for_alert_to_be_present()
                    self.actual_value = alert.text
                    status = self.actual_value.__eq__(input_value)
                case _:
                    self.log.error(local_task + " is an unsupported Value Assertion.")
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        return status

    def __is_equal(self, assertion: ValueAssertion, element: WebElement, attribute: str, input_value: str):
        status: bool = self.__execute(assertion, element, attribute, input_value)
        local_task = str(assertion).replace("_", " ").title()
        if status:
            self.log.debug(local_task + " Value is \"" + input_value + "\".")
        else:
            self.log.error(local_task + " Value is not \"" + input_value + "\". Actual locator_value is \"" + self.actual_value + "\".")
        return status

    def __is_not_equal(self, assertion: ValueAssertion, element: WebElement, attribute: str, input_value: str):
        status: bool = self.__execute(assertion, element, attribute, input_value)
        local_task = str(assertion).replace("_", " ").title()
        if status:
            self.log.error(local_task + " Value is \"" + input_value + "\".")
        else:
            self.log.debug(local_task + " Value is not \"" + input_value + "\". Actual locator_value is \"" + self.actual_value + "\".")
        return status

    def see_url(self, url: str):
        status: bool = self.__is_equal(ValueAssertion.URL, None, None, url)
        return status

    def see_partial_url(self, url: str):
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_URL, None, None, url)
        return status

    def dont_see_url(self, url: str):
        status: bool = self.__is_not_equal(ValueAssertion.URL, None, None, url)
        return status

    def dont_see_partial_url(self, url: str):
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_URL, None, None, url)
        return status

    def see_title(self, title: str):
        status: bool = self.__is_equal(ValueAssertion.TITLE, None, None, title)
        return status

    def see_partial_title(self, title: str):
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_TITLE, None, None, title)
        return status

    def dont_see_title(self, title: str):
        status: bool = self.__is_not_equal(ValueAssertion.TITLE, None, None, title)
        return status

    def dont_see_partial_title(self, title: str):
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_TITLE, None, None, title)
        return status

    def see_attribute_value(self, locator: By, locator_value: str, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_equal(ValueAssertion.ATTRIBUTE, element, attribute, attribute_value)
        return status

    def see_partial_attribute_value(self, locator: By, locator_value: str, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_ATTRIBUTE, element, attribute, attribute_value)
        return status

    def dont_see_attribute_value(self, locator: By, locator_value: str, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.ATTRIBUTE, element, attribute, attribute_value)
        return status

    def dont_see_partial_attribute_value(self, locator: By, locator_value: str, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_ATTRIBUTE, element, attribute, attribute_value)
        return status

    def see_attribute_value(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.ATTRIBUTE, element, attribute, attribute_value)
        return status

    def see_partial_attribute_value(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_ATTRIBUTE, element, attribute, attribute_value)
        return status

    def dont_see_attribute_value(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.ATTRIBUTE, element, attribute, attribute_value)
        return status

    def dont_see_partial_attribute_value(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_ATTRIBUTE, element, attribute, attribute_value)
        return status

    def see_attribute_value(self, parent_locator: WebElement, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.ATTRIBUTE, element, attribute, attribute_value)
        return status

    def see_partial_attribute_value(self, parent_locator: WebElement, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_ATTRIBUTE, element, attribute, attribute_value)
        return status

    def dont_see_attribute_value(self, parent_locator: WebElement, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.ATTRIBUTE, element, attribute, attribute_value)
        return status

    def dont_see_partial_attribute_value(self, parent_locator: WebElement, child_locator: By, child_locator_value, attribute: str, attribute_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_ATTRIBUTE, element, attribute, attribute_value)
        return status

    def see_text(self, locator: By, locator_value: str, text_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_equal(ValueAssertion.TEXT, element, None, text_value)
        return status

    def see_partial_text(self, locator: By, locator_value: str, text_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_TEXT, element, None, text_value)
        return status

    def dont_see_text(self, locator: By, locator_value: str, text_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.TEXT, element, None, text_value)
        return status

    def dont_see_partial_text(self, locator: By, locator_value: str, text_value: str):
        element = self.element_factory.create_element(locator, locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_TEXT, element, None, text_value)
        return status

    def see_text(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.TEXT, element, None, text_value)
        return status

    def see_partial_text(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_TEXT, element, None, text_value)
        return status

    def dont_see_text(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.TEXT, element, None, text_value)
        return status

    def dont_see_partial_text(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_TEXT, element, None, text_value)
        return status

    def see_text(self, parent_locator: WebElement, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.TEXT, element, None, text_value)
        return status

    def see_partial_text(self, parent_locator: WebElement, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_equal(ValueAssertion.PARTIAL_TEXT, element, None, text_value)
        return status

    def dont_see_text(self, parent_locator: WebElement, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.TEXT, element, None, text_value)
        return status

    def dont_see_partial_text(self, parent_locator: WebElement, child_locator: By, child_locator_value, text_value: str):
        element = self.element_factory.create_element(parent_locator, child_locator, child_locator_value)
        status: bool = self.__is_not_equal(ValueAssertion.PARTIAL_TEXT, element, None, text_value)
        return status

    def see_alert_message(self, message: str):
        status: bool = self.__is_equal(ValueAssertion.ALERT_MESSAGE, None, None, message)
        return status


class StateAssertion(Enum):
    DISPLAYED = auto()
    NOT_DISPLAYED = auto()
    ENABLED = auto()
    DISABLED = auto()
    SELECTED = auto()
    DESELECTED = auto()


class StateAssertions:

    def __init__(self, driver: webdriver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.driver = driver
        self.wait = wait


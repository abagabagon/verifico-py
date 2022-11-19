import logging

from redo import retriable
from selenium import webdriver
from selenium.common import (
    NoAlertPresentException,
    StaleElementReferenceException,
    UnexpectedTagNameException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from ledger_test_utils.web.selenium_utils import WaitCommands, WebElementFactory


class ValueAssertions:
    """Value Assertions contains functions pertaining to checking of values done by a user in a Web Page."""

    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of ValueAssertions.")
        try:
            self.driver = driver
            self.wait = wait
            self.element_factory = WebElementFactory(self.driver, self.wait)
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    def __is_equal(self, expected_value: str, actual_value):
        status = expected_value == actual_value
        if status:
            self.log.debug(f'Actual Value is equal to "{expected_value}".')
        else:
            self.log.debug(f'Actual Value "{actual_value}" is not equal to "{expected_value}"..')
        return status

    def __is_partially_equal(self, expected_value: str, actual_value):
        status = expected_value in actual_value
        if status:
            self.log.debug(
                f'Expected Value: {expected_value} is partially equal to Actual Value: "{actual_value}".'
            )
        else:
            self.log.debug(
                f'Expected Value: {expected_value} is not partially equal to Actual Value: "{actual_value}".'
            )
        return status

    def __does_text_exist(self, elements, text_value):
        status = False
        for element in elements:
            actual_text_value = element.text
            status = text_value == actual_text_value
            if status:
                self.log.debug(f"Found text value: {text_value} from element list.")
                break
        return status

    def __does_partial_text_exist(self, elements, text_value):
        status = False
        for element in elements:
            actual_text_value = element.text
            status = text_value in actual_text_value
            if status:
                self.log.debug(
                    f"Found text value: {text_value} as part of {actual_text_value} from element list."
                )
                break
        return status

    @retriable(
        attempts=3, sleeptime=1, max_sleeptime=10, sleepscale=1.5, retry_exceptions=(Exception,)
    )
    def __see_url(self, url: str, check_value):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {url}"
        )
        actual_url = self.driver.current_url.strip()
        status = check_value(url, actual_url)
        return status

    def see_url(self, url: str):
        """
        Verifies Page URL of Web Page if equal to the expected URL.

        Parameters:
            url (str): expected URL value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_url(url, self.__is_equal)
        return status

    def see_partial_url(self, url: str):
        """
        Verifies Page URL of Web Page if partially equal to the expected URL.

        Parameters:
            url (str): expected partial URL value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_url(url, self.__is_partially_equal)
        return status

    def dont_see_url(self, url: str):
        """
        Verifies Page URL of Web Page if not equal to the specified URL.

        Parameters:
            url (str): expected URL value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_url(url, self.__is_equal)
        return status

    def dont_see_partial_url(self, url: str):
        """
        Verifies Page URL of Web Page if not partially equal to the specified URL.

        Parameters:
            url (str): expected partial URL value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_url(url, self.__is_partially_equal)
        return status

    @retriable(attempts=3, sleeptime=1, sleepscale=1.5, retry_exceptions=(Exception,))
    def __see_title(self, title: str, check_value):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {title}"
        )
        actual_title = self.driver.title.strip()
        status = check_value(title, actual_title)
        return status

    def see_title(self, title: str):
        """
        Verifies Page Title of Web Page if equal to the expected Title.

        Parameters:
            title (str): expected Page Title value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_title(title, self.__is_equal)
        return status

    def see_partial_title(self, title: str):
        """
        Verifies Page Title of Web Page if partially equal to the expected Title.

        Parameters:
            title (str): expected Page Title value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_title(title, self.__is_partially_equal)
        return status

    def dont_see_title(self, title: str):
        """
        Verifies Page Title of Web Page if not equal to the specified Title.

        Parameters:
            title (str): expected Page Title value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_title(title, self.__is_equal)
        return status

    def dont_see_partial_title(self, title: str):
        """
        Verifies Page Title of Web Page if not partially equal to the specified Title.

        Parameters:
            title (str): expected Page Title value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_title(title, self.__is_partially_equal)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __see_attribute_value(self, locator: By, attribute: str, attribute_value: str, check_value):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {attribute_value} for attribute: {attribute} of locator: {str(locator)}."
        )
        element = self.element_factory.create_element(locator)
        actual_attribute_value = element.get_attribute(attribute)
        if actual_attribute_value is None:
            self.log.error(
                f"Please check if the attribute: {attribute} exists for locator: {str(locator)}."
            )
            status = False
        else:
            status = check_value(attribute_value, actual_attribute_value)
        return status

    def see_attribute_value(self, locator: By, attribute: str, attribute_value: str):
        """
        Verifies the attribute value of the Web Element of the specified Locator if equal to the expected value.

        Parameters:
            locator (By): locator of Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_attribute_value(locator, attribute, attribute_value, self.__is_equal)
        return status

    def see_partial_attribute_value(self, locator: By, attribute: str, attribute_value: str):
        """
        Verifies the attribute value of the Web Element of the specified Locator if partially equal to the expected
        value.

        Parameters:
            locator (By): locator of Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_attribute_value(
            locator, attribute, attribute_value, self.__is_partially_equal
        )
        return status

    def dont_see_attribute_value(self, locator: By, attribute: str, attribute_value: str):
        """
        Verifies the attribute value of the Web Element of the specified Locator if not equal to the specified value.

        Parameters:
            locator (By): locator of Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_attribute_value(
            locator, attribute, attribute_value, self.__is_equal
        )
        return status

    def dont_see_partial_attribute_value(self, locator: By, attribute: str, attribute_value: str):
        """
        Verifies the attribute value of the Web Element of the specified Locator if not partially equal to the
        specified value.

        Parameters:
            locator (By): locator of Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_attribute_value(
            locator, attribute, attribute_value, self.__is_partially_equal
        )
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __see_attribute_value_nested(
        self,
        parent_element: WebElement,
        child_locator: By,
        attribute: str,
        attribute_value: str,
        check_value,
    ):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {attribute_value} for attribute: {attribute} of locator: {str(child_locator)} under parent element: {str(parent_element)}."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        actual_attribute_value = element.get_attribute(attribute)
        if actual_attribute_value is None:
            self.log.error(
                f"Please check if the attribute: {attribute} exists for locator: {str(child_locator)}. under parent element: {str(parent_element)}"
            )
            status = False
        else:
            status = check_value(attribute_value, actual_attribute_value)
        return status

    def see_attribute_value_nested(
        self, parent_element: WebElement, child_locator: By, attribute: str, attribute_value: str
    ):
        """
        Verifies the attribute value of the nested Web Element of the specified Locator under a Parent Web Element if
        equal to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_attribute_value_nested(
            parent_element, child_locator, attribute, attribute_value, self.__is_equal
        )
        return status

    def see_partial_attribute_value_nested(
        self, parent_element: WebElement, child_locator: By, attribute: str, attribute_value: str
    ):
        """
        Verifies the attribute value of the nested Web Element of the specified Locator under a Parent Web Element if
        partially equal to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_attribute_value_nested(
            parent_element, child_locator, attribute, attribute_value, self.__is_partially_equal
        )
        return status

    def dont_see_attribute_value_nested(
        self, parent_element: WebElement, child_locator: By, attribute: str, attribute_value: str
    ):
        """
        Verifies the attribute value of the nested Web Element of the specified Locator under a Parent Web Element if
        not equal to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_attribute_value_nested(
            parent_element, child_locator, attribute, attribute_value, self.__is_equal
        )
        return status

    def dont_see_partial_attribute_value_nested(
        self, parent_element: WebElement, child_locator: By, attribute: str, attribute_value: str
    ):
        """
        Verifies the attribute value of the nested Web Element of the specified Locator under a Parent Web Element if
        not partially equal to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check attribute value of
            attribute (str): attribute of the locator to check value of
            attribute_value (str): expected attribute value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_attribute_value_nested(
            parent_element, child_locator, attribute, attribute_value, self.__is_partially_equal
        )
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __see_text(self, locator: By, text_value: str, check_value):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {text_value} of locator: {str(locator)}."
        )
        element = self.element_factory.create_element(locator)
        actual_text_value = element.text
        status = check_value(text_value, actual_text_value)
        return status

    def see_text(self, locator: By, text_value: str):
        """
        Verifies the text value of the Web Element of the specified Locator if equal to the expected value.

        Parameters:
            locator (By): locator of Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_text(locator, text_value, self.__is_equal)
        return status

    def see_partial_text(self, locator: By, text_value: str):
        """
        Verifies the text value of the Web Element of the specified Locator if partially equal to the expected value.

        Parameters:
            locator (By): locator of Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_text(locator, text_value, self.__is_partially_equal)
        return status

    def dont_see_text(self, locator: By, text_value: str):
        """
        Verifies the text value of the Web Element of the specified Locator if not equal to the expected value.

        Parameters:
            locator (By): locator of Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_text(locator, text_value, self.__is_equal)
        return status

    def dont_see_partial_text(self, locator: By, text_value: str):
        """
        Verifies the text value of the Web Element of the specified Locator if not partially equal to the expected value.

        Parameters:
            locator (By): locator of Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_text(locator, text_value, self.__is_partially_equal)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __see_text_nested(
        self, parent_element: WebElement, child_locator: By, text_value: str, check_value
    ):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {text_value} of locator: {str(child_locator)} under parent element: {str(parent_element)}."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        actual_text_value = element.text
        status = check_value(text_value, actual_text_value)
        return status

    def see_text_nested(self, parent_element: WebElement, child_locator: By, text_value: str):
        """
        Verifies the text value of the nested Web Element of the specified Locator under a Parent Web Element if equal
        to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_text_nested(parent_element, child_locator, text_value, self.__is_equal)
        return status

    def see_partial_text_nested(
        self, parent_element: WebElement, child_locator: By, text_value: str
    ):
        """
        Verifies the text value of the nested Web Element of the specified Locator under a Parent Web Element if
        partially equal to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_text_nested(
            parent_element, child_locator, text_value, self.__is_partially_equal
        )
        return status

    def dont_see_text_nested(self, parent_element: WebElement, child_locator: By, text_value: str):
        """
        Verifies the text value of the nested Web Element of the specified Locator under a Parent Web Element if not
        equal to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_text_nested(
            parent_element, child_locator, text_value, self.__is_equal
        )
        return status

    def dont_see_partial_text_nested(
        self, parent_element: WebElement, child_locator: By, text_value: str
    ):
        """
        Verifies the text value of the nested Web Element of the specified Locator under a Parent Web Element if not
        partially equal to the expected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check text value of
            text_value (str): expected text value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_text_nested(
            parent_element, child_locator, text_value, self.__is_partially_equal
        )
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(NoAlertPresentException,),
    )
    def __see_alert_message(self, message: str, check_value):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {message}."
        )
        alert = self.wait.wait_for_alert_to_be_present()
        actual_message = alert.text
        status = check_value(message, actual_message)
        return status

    def see_alert_message(self, message: str):
        """
        Verifies Javascript Alert Message displayed if equal to expected message

        Parameters:
            message (str): expected message at Javascript Alert
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_alert_message(message, self.__is_equal)
        return status

    def dont_see_alert_message(self, message: str):
        """
        Verifies Javascript Alert Message displayed if not equal to expected message

        Parameters:
            message (str): expected message at Javascript Alert
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_alert_message(message, self.__is_equal)
        return status

    def see_partial_alert_message(self, message: str):
        """
        Verifies Javascript Alert Message displayed if partially equal to expected message

        Parameters:
            message (str): expected message at Javascript Alert
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_alert_message(message, self.__is_partially_equal)
        return status

    def dont_see_partial_alert_message(self, message: str):
        """
        Verifies Javascript Alert Message displayed if not partially equal to expected message

        Parameters:
            message (str): expected message at Javascript Alert
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_alert_message(message, self.__is_partially_equal)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def __see_dropdown_value(self, locator: By, dropdown_value: str, check_value):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {dropdown_value} of locator: {str(locator)}."
        )
        element = self.element_factory.create_element(locator)
        select = Select(element)
        actual_dropdown_value = select.first_selected_option.text
        status = check_value(dropdown_value, actual_dropdown_value)
        return status

    def see_dropdown_value(self, locator: By, dropdown_value: str):
        """
        Verifies the Drop-down List value of the Web Element of the specified Locator if equal to the selected value.

        Parameters:
            locator (By): locator of Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_dropdown_value(locator, dropdown_value, self.__is_equal)
        return status

    def see_partial_dropdown_value(self, locator: By, dropdown_value: str):
        """
        Verifies the Drop-down List value of the Web Element of the specified Locator if partially equal to the
        selected value.

        Parameters:
            locator (By): locator of Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_dropdown_value(locator, dropdown_value, self.__is_partially_equal)
        return status

    def dont_see_dropdown_value(self, locator: By, dropdown_value: str):
        """
        Verifies the Drop-down List value of the Web Element of the specified Locator if not equal to the selected
        value.

        Parameters:
            locator (By): locator of Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_dropdown_value(locator, dropdown_value, self.__is_equal)
        return status

    def dont_see_partial_dropdown_value(self, locator: By, dropdown_value: str):
        """
        Verifies the Drop-down List value of the Web Element of the specified Locator if not partially equal to the
        selected value.

        Parameters:
            locator (By): locator of Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_dropdown_value(locator, dropdown_value, self.__is_partially_equal)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def __see_dropdown_value_nested(
        self, parent_element: WebElement, child_locator: By, dropdown_value: str, check_value
    ):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {dropdown_value} of locator: {str(child_locator)} under parent element: {str(parent_element)}."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        select = Select(element)
        actual_dropdown_value = select.first_selected_option.text
        status = check_value(dropdown_value, actual_dropdown_value)
        return status

    def see_dropdown_value_nested(
        self, parent_element: WebElement, child_locator: By, dropdown_value: str
    ):
        """
        Verifies the Drop-down List value of the nested Web Element of the specified Locator under a Parent Web Element
        if equal to the selected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if equal. Otherwise, False.
        """
        status = self.__see_dropdown_value_nested(
            parent_element, child_locator, dropdown_value, self.__is_equal
        )
        return status

    def see_partial_dropdown_value_nested(
        self, parent_element: WebElement, child_locator: By, dropdown_value: str
    ):
        """
        Verifies the Drop-down List value of the nested Web Element of the specified Locator under a Parent Web Element
        if partially equal to the selected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if partially equal. Otherwise, False.
        """
        status = self.__see_dropdown_value_nested(
            parent_element, child_locator, dropdown_value, self.__is_partially_equal
        )
        return status

    def dont_see_dropdown_value_nested(
        self, parent_element: WebElement, child_locator: By, dropdown_value: str
    ):
        """
        Verifies the Drop-down List value of the nested Web Element of the specified Locator under a Parent Web Element
        if not equal to the selected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if not equal. Otherwise, False.
        """
        status = not self.__see_dropdown_value_nested(
            parent_element, child_locator, dropdown_value, self.__is_equal
        )
        return status

    def dont_see_partial_dropdown_value_nested(
        self, parent_element: WebElement, child_locator: By, dropdown_value: str
    ):
        """
        Verifies the Drop-down List value of the nested Web Element of the specified Locator under a Parent Web Element
        if not partially equal to the selected value.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Drop-down List value of
            dropdown_value (str): expected drop-down option value
        Returns:
            status (bool): True if not partially equal. Otherwise, False.
        """
        status = not self.__see_dropdown_value_nested(
            parent_element, child_locator, dropdown_value, self.__is_partially_equal
        )
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def __see_multiselect_value(self, locator: By, multiselect_value: str, check_value):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {multiselect_value} of locator: {str(locator)}."
        )
        element = self.element_factory.create_element(locator)
        select = Select(element)
        selected_options = select.all_selected_options
        status = check_value(selected_options, multiselect_value)
        return status

    def see_multiselect_value(self, locator: By, multiselect_value: str):
        """
        Verifies the Multi-select value of the Web Element of the specified Locator if it is one of the selected values.

        Parameters:
            locator (By): locator of Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if selected. Otherwise, False.
        """
        status = self.__see_multiselect_value(locator, multiselect_value, self.__does_text_exist)
        return status

    def see_partial_multiselect_value(self, locator: By, multiselect_value: str):
        """
        Verifies the Multi-select value of the Web Element of the specified Locator if it is one of the selected values.

        Parameters:
            locator (By): locator of Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if selected. Otherwise, False.
        """
        status = self.__see_multiselect_value(
            locator, multiselect_value, self.__does_partial_text_exist
        )
        return status

    def dont_see_multiselect_value(self, locator: By, multiselect_value: str):
        """
        Verifies the Multi-select value of the Web Element of the specified Locator if it is not one of the selected
        values.

        Parameters:
            locator (By): locator of Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if deselected. Otherwise, False.
        """
        status = self.__see_multiselect_value(locator, multiselect_value, self.__does_text_exist)
        return not status

    def dont_see_partial_multiselect_value(self, locator: By, multiselect_value: str):
        """
        Verifies the Multi-select value of the Web Element of the specified Locator if it is not one of the selected
        values.

        Parameters:
            locator (By): locator of Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if deselected. Otherwise, False.
        """
        status = self.__see_multiselect_value(
            locator, multiselect_value, self.__does_partial_text_exist
        )
        return not status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def __see_multiselect_value_nested(
        self, parent_element: WebElement, child_locator: By, multiselect_value: str, check_value
    ):
        self.log.debug(
            f"Checking to {str(check_value.__name__).replace('_', ' ').replace('dont', 'not')}: {multiselect_value} of locator: {str(child_locator)} under parent element: {str(parent_element)}."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        select = Select(element)
        selected_options = select.all_selected_options
        status = check_value(selected_options, multiselect_value)
        return status

    def see_multiselect_value_nested(
        self, parent_element: WebElement, child_locator: By, multiselect_value: str
    ):
        """
        Verifies the Multi-select value of the nested Web Element of the specified Locator under Parent Web Element if
        it is one of the selected values.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if selected. Otherwise, False.
        """
        status = self.__see_multiselect_value_nested(
            parent_element, child_locator, multiselect_value, self.__does_text_exist
        )
        return status

    def see_partial_multiselect_value_nested(
        self, parent_element: WebElement, child_locator: By, multiselect_value: str
    ):
        """
        Verifies the Multi-select value of the nested Web Element of the specified Locator under Parent Web Element if
        it is one of the selected values.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if selected. Otherwise, False.
        """
        status = self.__see_multiselect_value_nested(
            parent_element, child_locator, multiselect_value, self.__does_partial_text_exist
        )
        return status

    def dont_see_multiselect_value_nested(
        self, parent_element: WebElement, child_locator: By, multiselect_value: str
    ):
        """
        Verifies the Multi-select value of the nested Web Element of the specified Locator under Parent Web Element if
        it is not one of the selected values.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if deselected. Otherwise, False.
        """
        status = self.__see_multiselect_value_nested(
            parent_element, child_locator, multiselect_value, self.__does_text_exist
        )
        return not status

    def dont_see_partial_multiselect_value_nested(
        self, parent_element: WebElement, child_locator: By, multiselect_value: str
    ):
        """
        Verifies the Multi-select value of the nested Web Element of the specified Locator under Parent Web Element if
        it is not one of the selected values.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check Multi-select value of
            multiselect_value (str): expected Multi-select option value
        Returns:
            status (bool): True if deselected. Otherwise, False.
        """
        status = self.__see_multiselect_value_nested(
            parent_element, child_locator, multiselect_value, self.__does_partial_text_exist
        )
        return not status


class StateAssertions:
    """State Assertions contains functions pertaining to checking the state of Web Elements done by a user in a Web Page."""

    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of StateAssertions.")
        try:
            self.driver = driver
            self.wait = wait
            self.element_factory = WebElementFactory(self.driver, self.wait)
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __see(self, locator: By):
        self.log.debug(
            f"Checking to see if element with locator: {str(locator)} is displayed or not."
        )
        element = self.element_factory.create_element(locator)
        status = element.is_displayed()
        return status

    def see(self, locator: By):
        """
        Verifies if Web Element of specified Locator is displayed on Web Page.

        Parameters:
            locator (By): locator of Web Element to check if displayed on Web Page
        Returns:
            status (bool): True if displayed. Otherwise, False.
        """
        status = self.__see(locator)
        return status

    def dont_see(self, locator: By):
        """
        Verifies if Web Element of specified Locator is not displayed on Web Page.

        Parameters:
            locator (By): locator of Web Element to check if not displayed on Web Page
        Returns:
            status (bool): True if not displayed. Otherwise, False.
        """
        status = not self.__see(locator)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __enabled(self, locator: By):
        self.log.debug(
            f"Checking to see if element with locator: {str(locator)} is enabled or not."
        )
        element = self.element_factory.create_element(locator)
        status = element.is_enabled()
        return status

    def enabled(self, locator: By):
        """
        Verifies if Web Element of specified Locator is enabled on Web Page.

        Parameters:
            locator (By): locator of Web Element to check if enabled on Web Page
        Returns:
            status (bool): True if enabled. Otherwise, False.
        """
        status = self.__enabled(locator)
        return status

    def disabled(self, locator: By):
        """
        Verifies if Web Element of specified Locator is disabled on Web Page.

        Parameters:
            locator (By): locator of Web Element to check if disabled on Web Page
        Returns:
            status (bool): True if disabled. Otherwise, False.
        """
        status = not self.__enabled(locator)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __selected(self, locator: By):
        self.log.debug(
            f"Checking to see if element with locator: {str(locator)} is selected or not."
        )
        element = self.element_factory.create_element(locator)
        status = element.is_selected()
        return status

    def selected(self, locator: By):
        """
        Verifies if Web Element of specified Locator is selected on Web Page.

        Parameters:
            locator (By): locator of Web Element to check if selected on Web Page
        Returns:
            status (bool): True if selected. Otherwise, False.
        """
        status = self.__selected(locator)
        return status

    def deselected(self, locator: By):
        """
        Verifies if Web Element of specified Locator is deselected on Web Page.

        Parameters:
            locator (By): locator of Web Element to check if deselected on Web Page
        Returns:
            status (bool): True if deselected. Otherwise, False.
        """
        status = not self.__selected(locator)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __see_nested(self, parent_element: WebElement, child_locator: By):
        self.log.debug(
            f"Checking to see if element with locator: {str(child_locator)} under parent element: {str(parent_element)} is displayed or not."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        status = element.is_displayed()
        return status

    def see_nested(self, parent_element: WebElement, child_locator: By):
        """
        Verifies if nested Web Element of specified Locator under a Parent Web Element is displayed on Web Page.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check if displayed on Web Page
        Returns:
            status (bool): True if displayed. Otherwise, False.
        """
        status = self.__see_nested(parent_element, child_locator)
        return status

    def dont_see_nested(self, parent_element: WebElement, child_locator: By):
        """
        Verifies if nested Web Element of specified Locator under a Parent Web Element is not displayed on Web Page.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check if displayed on Web Page
        Returns:
            status (bool): True if not displayed. Otherwise, False.
        """
        status = not self.__see_nested(parent_element, child_locator)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __enabled_nested(self, parent_element: WebElement, child_locator: By):
        self.log.debug(
            f"Checking to see if element with locator: {str(child_locator)} under parent element: {str(parent_element)} is enabled or not."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        status = element.is_enabled()
        return status

    def enabled_nested(self, parent_element: WebElement, child_locator: By):
        """
        Verifies if nested Web Element of specified Locator under a Parent Web Element is enabled on Web Page.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check if displayed on Web Page
        Returns:
            status (bool): True if enabled. Otherwise, False.
        """
        status = self.__enabled_nested(parent_element, child_locator)
        return status

    def disabled_nested(self, parent_element: WebElement, child_locator: By):
        """
        Verifies if nested Web Element of specified Locator under a Parent Web Element is disabled on Web Page.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check if displayed on Web Page
        Returns:
            status (bool): True if disabled. Otherwise, False.
        """
        status = not self.__enabled_nested(parent_element, child_locator)
        return status

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def __selected_nested(self, parent_element: WebElement, child_locator: By):
        self.log.debug(
            f"Checking to see if element with locator: {str(child_locator)} under parent element: {str(parent_element)} is selected or not."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        status = element.is_selected()
        return status

    def selected_nested(self, parent_element: WebElement, child_locator: By):
        """
        Verifies if nested Web Element of specified Locator under a Parent Web Element is selected on Web Page.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check if displayed on Web Page
        Returns:
            status (bool): True if selected. Otherwise, False.
        """
        status = self.__selected_nested(parent_element, child_locator)
        return status

    def deselected_nested(self, parent_element: WebElement, child_locator: By):
        """
        Verifies if nested Web Element of specified Locator under a Parent Web Element is deselected on Web Page.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to check if displayed on Web Page
        Returns:
            status (bool): True if deselected. Otherwise, False.
        """
        status = not self.__selected_nested(parent_element, child_locator)
        return status

    def see_alert_is_present(self):
        """
        Verifies that a Javascript Alert is present on the Web Page
        Returns:
            status (bool): True if present. Otherwise, False.
        """
        self.log.debug(f"Checking to see if alert is present.")
        status = self.wait.wait_for_alert_to_be_present()
        return status

    def dont_see_alert_is_present(self):
        """
        Verifies that a Javascript Alert is not present on the Web Page
        Returns:
            status (bool): True if not present. Otherwise, False.
        """
        self.log.debug(f"Checking to see if alert is not present.")
        try:
            _ = self.driver.switch_to.alert
            status = False
        except NoAlertPresentException:
            status = True
        return status

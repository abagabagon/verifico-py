import logging

from redo import retriable
from selenium import webdriver
from selenium.common import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidElementStateException,
    MoveTargetOutOfBoundsException,
    NoSuchWindowException,
    StaleElementReferenceException,
    UnexpectedTagNameException,
)
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from ledger_test_utils.web.selenium_utils import WaitCommands, WebElementFactory


class AlertCommands:
    """
    Alert Commands contains functions pertaining to Javascript Alerts in a Web Page.
    """

    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of AlertCommands.")
        try:
            self.driver = driver
            self.wait = wait
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    def accept_alert(self):
        """
        Accepts Javascript Alert
        """
        self.log.debug(f"Accepting Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.accept()

    def cancel_alert(self):
        """
        Cancels Javascript Alert
        """
        self.log.debug(f"Canceling Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.dismiss()

    def type_alert(self, input_text: str):
        """
        Simulates typing at Javascript Alert Text Box

        Parameters:
            input_text (str): input text value to type to the alert text box
        """
        self.log.debug(f"Typing {input_text} into Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.send_keys(input_text)


class BrowserCommands:
    """Browser Commands contains functions relating to actions being done by the user at the Web Browser."""

    def __init__(self, driver: webdriver, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of BrowserCommands.")
        try:
            self.driver = driver
        except AttributeError:
            self.log.fatal("WebDriver is not initialized!")
            raise

    def open_tab(self):
        """
        Opens Tab
        """
        self.log.debug("Opening new tab.")
        self.driver.execute_script("window.open('{input_value}', '_blank');")

    def maximize(self):
        """Maximizes Browser Window"""
        self.log.debug("Maximizing Window.")
        self.driver.maximize_window()

    def delete_all_cookies(self):
        """Deletes all cookies"""
        self.log.debug("Deleting all cookies.")
        self.driver.delete_all_cookies()

    def go_to(self, url: str):
        """
        Navigates to the Url specified

        Parameters:
            url (str): Url to navigate to
        """
        self.log.debug(f"Going to URL: {url}.")
        self.driver.get(url)

    def back(self):
        """Navigates one item back from the browser's history"""
        self.log.debug("Navigating back.")
        self.driver.back()

    def forward(self):
        """Navigates one item forward from the browser's history"""
        self.log.debug("Navigating forward.")
        self.driver.forward()

    def refresh(self):
        """Refreshes current page"""
        self.log.debug("Refreshing page.")
        self.driver.refresh()

    def close_tab(self):
        """Closes Tab of a Web Browser"""
        self.log.debug("Closing tab.")
        self.driver.close()

    def close_browser(self):
        """Closes Web Browser"""
        self.log.debug("Closing browser.")
        self.driver.quit()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            ValueError,
            NoSuchWindowException,
        ),
    )
    def switch_tab_by_title(self, title: str):
        """
        Switches to a Tab based on Page Title

        Parameters:
            title (str): Title of Page to Switch into
        """
        self.log.debug(f"Switching to Tab/Window with Title: {title}.")
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            current_title = self.driver.title
            if current_title == title:
                self.log.debug(f'Found Page with Title: "{title}".')
                break
        else:
            raise ValueError(f'Page with Title: "{title}" does not exist.')

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            ValueError,
            NoSuchWindowException,
        ),
    )
    def switch_tab_by_url(self, url: str):
        """
        Switches to a Tab based on Page Url

        Parameters:
            url (str): URL of Page to Switch into
        """
        self.log.debug(f"Switching to Tab/Window with Title: {url}.")
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            current_url = self.driver.current_url
            if current_url == url:
                self.log.debug(f'Found Page with URL: "{url}".')
                break
        else:
            raise ValueError(f'Page with URL: "{url}" does not exist.')

    def switch_tab_to_original(self):
        """Switches back to Original Tab"""
        self.log.debug("Switching to Original or default Tab/Window.")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])

    def scroll(self, pixel_horizontal: int, pixel_vertical: int):
        """
        Scrolls Page

        Parameters:
            pixel_horizontal (int): horizontal pixel setting
            pixel_vertical (int): vertical pixel setting
        """
        self.log.debug(f"Scrolling to coordinates {str(pixel_horizontal)}, {str(pixel_vertical)}")
        self.driver.execute_script(
            f"window.scrollBy({str(pixel_horizontal)}, {str(pixel_vertical)})"
        )

    def count(self, locator: By):
        """
        Counts instance of the Web Element of the specified Locator

        Parameters:
            locator (By): locator of Web Element to count.
        """
        self.log.debug(f"Checking Element Count of locator: {str(locator)}.")
        elements = self.driver.find_elements(locator)
        count = len(elements)
        return count


class GetCommands:
    """Get Commands contains functions pertaining to get value actions done by a user in a Web Page."""

    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of GetCommands.")
        try:
            self.driver = driver
            self.wait = wait
            self.action_chains = ActionChains(self.driver)
            self.element_factory = WebElementFactory(self.driver, self.wait)
            self.retrieved_value = None
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    @retriable(
        attempts=3, sleeptime=1, sleepscale=1.5, retry_exceptions=(StaleElementReferenceException,)
    )
    def get_text(self, locator: By):
        """
        Gets the text of the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to get text from
        Returns:
            text (str): Retrieved text value
        """
        self.log.debug(f"Retrieving text value from locator: {str(locator)}.")
        element = self.element_factory.create_element(locator)
        text = element.text
        return text

    @retriable(
        attempts=3, sleeptime=1, sleepscale=1.5, retry_exceptions=(StaleElementReferenceException,)
    )
    def get_attribute(self, locator: By, attribute: str):
        """
        Gets the attribute value of the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to get attribute value from
            attribute (str): attribute of the locator to get value from
        Returns:
            attribute_value (str): Retrieved attribute value
        """
        self.log.debug(f"Retrieving attribute value of {attribute} from locator: {str(locator)}.")
        element = self.element_factory.create_element(locator)
        attribute_value = element.get_attribute(attribute)
        return attribute_value

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def get_dropdown_value(self, locator: By):
        """
        Gets the drop-down list value of the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to get Dropdown Value from.
        Returns:
            dropdown_value (str): Retrieved Drop-down List Value
        """
        self.log.debug(f"Retrieving dropdown value from locator: {str(locator)}.")
        element = self.element_factory.create_element(locator)
        select = Select(element)
        dropdown_value = select.first_selected_option
        return dropdown_value

    @retriable(
        attempts=3, sleeptime=1, sleepscale=1.5, retry_exceptions=(StaleElementReferenceException,)
    )
    def get_text_nested(self, parent_element: WebElement, child_locator: By):
        """
        Gets the text of the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to get text from
        Returns:
            text (str): Retrieved text value
        """
        self.log.debug(
            f"Retrieving text value from locator: {str(child_locator)} under parent element: {str(parent_element)}."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        text = element.text
        return text

    @retriable(
        attempts=3, sleeptime=1, sleepscale=1.5, retry_exceptions=(StaleElementReferenceException,)
    )
    def get_attribute_nested(self, parent_element: WebElement, child_locator: By, attribute: str):
        """
        Gets the attribute value of the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement) Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to get attribute value from
            attribute (str): attribute of the locator to get value from
        Returns:
            attribute_value (str): Retrieved attribute value
        """
        self.log.debug(
            f"Retrieving attribute value of {attribute} from locator: {str(child_locator)} under parent element: {str(parent_element)}."
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        attribute_value = element.get_attribute(attribute)
        return attribute_value

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def get_dropdown_value_nested(self, parent_element: WebElement, child_locator: By):
        """
        Gets the drop-down list value of the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to get Dropdown Value from
        Returns:
            dropdown_value (str): Retrieved Drop-down List Value
        """
        self.log.debug(
            f"Retrieving dropdown value from locator: {str(child_locator)} under parent element: {str(parent_element)}"
        )
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        select = Select(element)
        dropdown_value = select.first_selected_option
        return dropdown_value


class KeyboardCommands:
    """Keyboard Commands contains functions pertaining to keyboard actions done by a user in a Web Page."""

    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of KeyboardCommands.")
        try:
            self.driver = driver
            self.wait = wait
            self.action_chains = ActionChains(self.driver)
            self.element_factory = WebElementFactory(self.driver, self.wait)
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementNotInteractableException,
            InvalidElementStateException,
        ),
    )
    def clear(self, locator: By):
        """
        Clears value of the Web Element of the specified Locator. Applicable for INPUT and TEXTAREA Web Elements.

        Parameters:
            locator (By): locator of Web Element to clear value of
        """
        element = self.element_factory.create_element(locator)
        element.clear()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementNotInteractableException,
            InvalidElementStateException,
        ),
    )
    def type(self, locator: By, input_text: str):
        """
        Types the specified input text to the Web Element of the specified Locator. Applicable for INPUT and TEXTAREA
        Web Elements.

        Parameters:
            locator (By): locator of Web Element to type value to
            input_text (str): input text value to type into the Web Element
        """
        element = self.element_factory.create_element(locator)
        element.send_keys(input_text)

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementNotInteractableException,
            InvalidElementStateException,
        ),
    )
    def press(self, locator: By, key_button: Keys):
        """
        Simulates pressing of characters into the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to press character keys to
            key_button (Keys): character keys to press into the Web Element
        """
        element = self.element_factory.create_element(locator)
        element.send_keys(key_button)

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementNotInteractableException,
            InvalidElementStateException,
        ),
    )
    def clear_nested(self, parent_element: WebElement, child_locator: By):
        """
        Clears value of the nested Web Element of the specified Locator under a Parent Web Element. Applicable for
        INPUT and TEXTAREA Web Elements.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to clear value of
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        element.clear()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementNotInteractableException,
            InvalidElementStateException,
        ),
    )
    def type_nested(self, parent_element: WebElement, child_locator: By, input_text: str):
        """
        Types the specified input text to the nested Web Element of the specified Locator under a Parent Web Element.
        Applicable for INPUT and TEXTAREA Web Elements.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to clear value of
            input_text (str): input text value to type into the nested Web Element
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        element.send_keys(input_text)

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementNotInteractableException,
            InvalidElementStateException,
        ),
    )
    def press_nested(self, parent_element: WebElement, child_locator: By, key_button: Keys):
        """
        Simulates pressing of characters into the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to press key characters to
            key_button (Keys): character keys to press into the nested Web Element
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        element.send_keys(key_button)


class MouseCommands:
    """Mouse Commands contains functions pertaining to mouse actions done by a user at a Web Page."""

    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of MouseCommands.")
        try:
            self.driver = driver
            self.wait = wait
            self.action_chains = ActionChains(self.driver)
            self.element_factory = WebElementFactory(self.driver, self.wait)
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def click(self, locator: By):
        """
        Clicks the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to click
        """
        element = self.element_factory.create_element(locator)
        element.click()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def click_js(self, locator: By):
        """
        Clicks the Web Element of the specified Locator using Javascript.

        Parameters:
            locator (By): locator of Web Element to click
        """
        element = self.element_factory.create_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def click_and_hold(self, locator: By):
        """
        Clicks and holds the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to click and hold
        """
        element = self.element_factory.create_element(locator)
        self.action_chains.click_and_hold(element).perform()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def double_click(self, locator: By):
        """
        Double-clicks the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to double-click
        """
        element = self.element_factory.create_element(locator)
        self.action_chains.double_click(element).perform()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def point(self, locator: By):
        """
        Points mouse to the Web Element of the specified Locator.

        Parameters:
            locator (By): locator of Web Element to point mouse on
        """
        element = self.element_factory.create_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.action_chains.move_to_element(element).perform()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def click_nested(self, parent_element: WebElement, child_locator: By):
        """
        Clicks the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to click
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        element.click()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(StaleElementReferenceException,),
    )
    def click_js_nested(self, parent_element: WebElement, child_locator: By):
        """
        Clicks the nested Web Element of the specified Locator using Javascript under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to click
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        self.driver.execute_script("arguments[0].click();", element)

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def click_and_hold_nested(self, parent_element: WebElement, child_locator: By):
        """
        Clicks and holds the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to click and hold
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        self.action_chains.click_and_hold(element).perform()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            ElementClickInterceptedException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def double_click_nested(self, parent_element: WebElement, child_locator: By):
        """
        Double-clicks the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to double-click
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        self.action_chains.double_click(element).perform()

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            MoveTargetOutOfBoundsException,
        ),
    )
    def point_nested(self, parent_element: WebElement, child_locator: By):
        """
        Points mouse to the nested Web Element of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of nested Web Element to point mouse on
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.action_chains.move_to_element(element).perform()


class SelectCommands:
    """Select Commands contains functions pertaining to actions done by a user on drop-down elements in a Web Page."""

    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of SelectCommands.")
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
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def select(self, locator: By, input_option: str):
        """
        Selects a Drop-down List / Multi-select Web Element Option of the specified Locator.

        Parameters:
            locator (By):locator of the Drop-down List / Multi-select Web Element
            input_option (str): input option to select at the Drop-down List Web Element
        """
        element = self.element_factory.create_element(locator)
        select = Select(element)
        for option in select.options:
            if input_option == option.text:
                select.select_by_visible_text(input_option)
                break
        else:
            raise ValueError(f'Failed to select an option. Option "{input_option}" is invalid!')

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def deselect(self, locator: By, input_option: str):
        """
        Deselects a Multi-select Web Element Option of the specified Locator.

        Parameters:
            locator (By):locator of the Multi-select Web Element
            input_option (str): input option to select at the Multi-select Web Element
        """
        element = self.element_factory.create_element(locator)
        select = Select(element)
        for option in select.options:
            if input_option == option.text:
                select.deselect_by_visible_text(input_option)
                break
        else:
            raise ValueError(f'Failed to deselect an option. Option "{input_option}" is invalid!')

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def select_nested(self, parent_element: WebElement, child_locator: By, input_option: str):
        """
        Selects a Drop-down List / Multi-select nested Web Element Option of the specified Locator under a Parent Web Element.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of the Drop-down List / Multi-select nested Web Element
            input_option (str): input option to select at the Drop-down List Web Element
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        select = Select(element)
        for option in select.options:
            if input_option == option.text:
                select.select_by_visible_text(input_option)
                break
        else:
            raise ValueError(f'Failed to select an option. Option "{input_option}" is invalid!')

    @retriable(
        attempts=3,
        sleeptime=1,
        sleepscale=1.5,
        retry_exceptions=(
            StaleElementReferenceException,
            UnexpectedTagNameException,
        ),
    )
    def deselect_nested(self, parent_element: WebElement, child_locator: By, input_option: str):
        """
        Deselects a Multi-select Web Element Option of the specified Locator.

        Parameters:
            parent_element (WebElement): Parent Web Element where the Child Locator will be located from
            child_locator (By): locator of the Multi-select Web Element
            input_option (str): input option to select at the Multi-select Web Element
        """
        element = self.element_factory.create_nested_element(parent_element, child_locator)
        select = Select(element)
        for option in select.options:
            if input_option == option.text:
                select.deselect_by_visible_text(input_option)
                break
        else:
            raise ValueError(f'Failed to deselect an option. Option "{input_option}" is invalid!')

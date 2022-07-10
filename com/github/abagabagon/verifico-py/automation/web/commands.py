from enum import Enum, auto
from selenium import webdriver
from selenium.common import NoSuchWindowException, StaleElementReferenceException, UnexpectedTagNameException, \
    ElementNotInteractableException, InvalidElementStateException, ElementClickInterceptedException, \
    MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium_utils import WaitCommands
from selenium_utils import WebElementFactory
from time import sleep
import logging
import platform


class AlertAction(Enum):
    ACCEPT = auto()
    CANCEL = auto()
    TYPE_INTO = auto()


class AlertCommands:

    def __init__(self, driver: webdriver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.driver = driver
        self.wait = wait

    def accept_alert(self):
        self.log.debug("Performing " + str(AlertAction.ACCEPT).title() + " Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.accept()

    def cancel_alert(self):
        self.log.debug("Performing " + str(AlertAction.CANCEL).title() + " Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.dismiss()

    def type_alert(self, input_text: str):
        self.log.debug("Performing " + str(AlertAction.TYPE_INTO).replace("_", " ").title() + " Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.send_keys(input_text)


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
        local_task = str(action).replace("_", " ").title()
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
        local_task = str(action).replace("_", " ").title()
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
        self.log.debug("Performing SCROLL Browser Action to coordinates " + str(pixel_horizontal) + ", " + str(pixel_vertical))
        try:
            self.driver.execute_script("window.scrollBy(" + str(pixel_horizontal) + ", " + str(pixel_vertical) + ")")
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform SCROLL Browser Action: " + str(error_message))

    def count(self, locator: By, locator_value: str):
        self.log.debug("Performing Element Count.")
        elements = self.driver.find_elements(locator, locator_value);
        count = len(elements)
        return count


class GetAction(Enum):
    GET_ATTRIBUTE = auto()
    GET_TEXT = auto()
    GET_DROPDOWN = auto()


class GetCommands:

    def __init__(self, driver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of GetCommands.")
        self.driver = driver
        self.wait = wait
        self.action_chains = ActionChains(self.driver)
        self.element_factory = WebElementFactory(self.driver, self.wait)
        self.retrieved_value = None

    def __execute(self, action: GetAction, element: WebElement, attribute: str):
        local_task = str(action).replace("_", " ").title()
        action_performed = False
        self.retrieved_value = None
        try:
            match action:
                case GetAction.GET_ATTRIBUTE:
                    self.retrieved_value = element.get_attribute(attribute)
                case GetAction.GET_DROPDOWN:
                    select = Select(element)
                    self.retrieved_value = select.first_selected_option
                case GetAction.GET_TEXT:
                    self.retrieved_value = element.text
                case _:
                    self.log.error(local_task + " is an unsupported Get Action.")
            action_performed = True
        except StaleElementReferenceException as error_message:
            self.log.warning("Encountered StaleElementReferenceException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        except UnexpectedTagNameException as error_message:
            self.log.warning("Encountered UnexpectedTagNameException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        return action_performed

    def __do_command(self, action: GetAction, locator: By, locator_value: str, attribute: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Web Element " + locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, locator_value)
            action_performed = self.__execute(action, element, attribute)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Get Action " + local_task + " for Web Element " + locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Get Action " + local_task + " for Web Element " + locator_value + ".")
            else:
                break
        return self.retrieved_value

    def get_text(self, locator: By, locator_value: str):
        text = self.__do_command(GetAction.GET_TEXT, locator, locator_value, None)
        return text

    def get_attribute(self, locator: By, locator_value: str, attribute: str):
        attribute_value = self.__do_command(GetAction.GET_ATTRIBUTE, locator, locator_value, attribute)
        return attribute_value

    def get_dropdown_value(self, locator: By, locator_value: str):
        dropdown_value = self.__do_command(GetAction.GET_DROPDOWN, locator, locator_value, None)
        return dropdown_value

    def __do_command(self, action: GetAction, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, attribute: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
            action_performed = self.__execute(action, element, attribute)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Get Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Get Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
            else:
                break
        return self.retrieved_value

    def get_text(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        text = self.__do_command(GetAction.GET_TEXT, parent_locator, parent_locator_value, child_locator, child_locator_value, None)
        return text

    def get_attribute(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, attribute: str):
        attribute_value = self.__do_command(GetAction.GET_ATTRIBUTE, parent_locator, parent_locator_value, child_locator, child_locator_value, attribute)
        return attribute_value

    def get_dropdown_value(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        dropdown_value = self.__do_command(GetAction.GET_DROPDOWN, parent_locator, parent_locator_value, child_locator, child_locator_value, None)
        return dropdown_value

    def __do_command(self, action: GetAction, parent_element, child_locator: By, child_locator_value: str, attribute: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_locator_value)
            action_performed = self.__execute(action, element, attribute)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Get Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Get Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break
        return self.retrieved_value

    def get_text(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        text = self.__do_command(GetAction.GET_TEXT, parent_element, child_locator, child_locator_value, None)
        return text

    def get_attribute(self, parent_element: WebElement, child_locator: By, child_locator_value: str, attribute: str):
        attribute_value = self.__do_command(GetAction.GET_ATTRIBUTE, parent_element, child_locator, child_locator_value, attribute)
        return attribute_value

    def get_dropdown_value(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        dropdown_value = self.__do_command(GetAction.GET_DROPDOWN, parent_element, child_locator, child_locator_value, None)
        return dropdown_value


class KeyboardAction(Enum):
    CLEAR = auto()
    PRESS = auto()
    TYPE = auto()


class KeyboardCommands:

    def __init__(self, driver, wait: WaitCommands):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating instance of KeyboardCommands.")
        self.driver = driver
        self.wait = wait
        self.action_chains = ActionChains(self.driver)
        self.element_factory = WebElementFactory(self.driver, self.wait)

    def __execute(self, action: KeyboardAction, element: WebElement, input_text: str, key_button: Keys):
        local_task = str(action).replace("_", " ").title()
        action_performed = False
        operating_system = platform.system()
        try:
            match action:
                case KeyboardAction.CLEAR:
                    if operating_system.__eq__("Darwin"):
                        self.action_chains.click(element)\
                            .pause(200).keyDown(Keys.COMMAND).sendKeys("a").keyUp(Keys.COMMAND)\
                            .pause(200).sendKeys(Keys.DELETE).perform()
                    else:
                        self.action_chains.click(element)\
                            .pause(200).keyDown(Keys.CONTROL).sendKeys("a").keyUp(Keys.CONTROL)\
                            .pause(200).sendKeys(Keys.DELETE).perform()
                case KeyboardAction.PRESS:
                    element.send_keys(key_button)
                case KeyboardAction.TYPE:
                    element.send_keys(input_text)
                case _:
                    self.log.error(local_task + " is an unsupported Keyboard Action.")
            action_performed = True
        except StaleElementReferenceException as error_message:
            self.log.warning("Encountered StaleElementReferenceException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        except ElementNotInteractableException as error_message:
            self.log.warning("Encountered ElementNotInteractableException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
            element.click()
        except InvalidElementStateException as error_message:
            self.log.warning("Encountered InvalidElementStateException when trying to perform task " + local_task + " Web Driver: " + str(error_message))
            element.click()
        except Exception as error_message:
            self.log.warning("Encountered Exception when trying to perform task " + local_task + " Web Driver: " + str(error_message))
        return action_performed

    def __do_command(self, action: KeyboardAction, locator: By, locator_value: str, input_text: str, key_button: Keys):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Web Element " + locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, locator_value)
            action_performed = self.__execute(action, element, input_text, key_button)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Keyboard Action " + local_task + " for Web Element " + locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Keyboard Action " + local_task + " for Web Element " + locator_value + ".")
            else:
                break

    def clear(self, locator: By, locator_value: str):
        self.__do_command(KeyboardAction.CLEAR, locator, locator_value, None, None)

    def type(self, locator: By, locator_value: str, input_text: str):
        self.__do_command(KeyboardAction.TYPE, locator, locator_value, input_text, None)

    def press(self, locator: By, locator_value: str, key_button: Keys):
        self.__do_command(KeyboardAction.PRESS, locator, locator_value, None, key_button)

    def __do_command(self, action: KeyboardAction, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, input_text: str, key_button: Keys):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
            action_performed = self.__execute(action, element, input_text, key_button)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Keyboard Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Keyboard Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
            else:
                break

    def clear(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        self.__do_command(KeyboardAction.CLEAR, parent_locator, parent_locator_value, child_locator, child_locator_value, None, None)

    def type(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, input_text: str):
        self.__do_command(KeyboardAction.TYPE, parent_locator, parent_locator_value, child_locator, child_locator_value, input_text, None)

    def press(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, key_button: Keys):
        self.__do_command(KeyboardAction.PRESS, parent_locator, parent_locator_value, child_locator, child_locator_value, None, key_button)

    def __do_command(self, action: KeyboardAction, parent_element: WebElement, child_locator: By, child_locator_value: str, input_text: str, key_button: Keys):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_locator_value)
            action_performed = self.__execute(action, element, input_text, key_button)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Keyboard Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Keyboard Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break

    def clear(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        self.__do_command(KeyboardAction.CLEAR, parent_element, child_locator, child_locator_value, None, None)

    def type(self, parent_element: WebElement, child_locator: By, child_locator_value: str, input_text: str):
        self.__do_command(KeyboardAction.TYPE, parent_element, child_locator, child_locator_value, input_text, None)

    def press(self, parent_element: WebElement, child_locator: By, child_locator_value: str, key_button: Keys):
        self.__do_command(KeyboardAction.PRESS, parent_element, child_locator, child_locator_value, None, key_button)


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

    def __do_command(self, action: MouseAction, locator: By, locator_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Web Element " + locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, locator_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Mouse Action " + local_task + " to Web Element " + locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Mouse Action " + local_task + " to Web Element " + locator_value + ".")
            else:
                break

    def click(self, locator: By, locator_value: str):
        self.__do_command(MouseAction.CLICK, locator, locator_value)

    def click_js(self, locator: By, locator_value: str):
        self.__do_command(MouseAction.CLICK_JS, locator, locator_value)

    def click_and_hold(self, locator: By, locator_value: str):
        self.__do_command(MouseAction.CLICK_AND_HOLD, locator, locator_value)

    def double_click(self, locator: By, locator_value: str):
        self.__do_command(MouseAction.DOUBLE_CLICK, locator, locator_value)

    def point(self, locator: By, locator_value: str):
        self.__do_command(MouseAction.POINT, locator, locator_value)

    def __do_command(self, action: MouseAction, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Mouse Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Mouse Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
            else:
                break

    def click(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.CLICK, parent_locator, parent_locator_value, child_locator, child_locator_value)

    def click_js(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.CLICK_JS, parent_locator, parent_locator_value, child_locator, child_locator_value)

    def click_and_hold(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.CLICK_AND_HOLD, parent_locator, parent_locator_value, child_locator, child_locator_value)

    def double_click(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.DOUBLE_CLICK, parent_locator, parent_locator_value, child_locator, child_locator_value)

    def point(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.POINT, parent_locator, parent_locator_value, child_locator, child_locator_value)

    def __do_command(self, action: MouseAction, parent_element: WebElement, child_locator: By, child_locator_value: str):
        local_task = str(action).replace("_", " ").title()
        self.log.debug("Performing " + local_task + " to the Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_locator_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Mouse Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Mouse Action " + local_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break

    def click(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.CLICK, parent_element, child_locator, child_locator_value)

    def click_js(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.CLICK_JS, parent_element, child_locator, child_locator_value)

    def click_and_hold(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.CLICK_AND_HOLD, parent_element, child_locator, child_locator_value)

    def double_click(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.DOUBLE_CLICK, parent_element, child_locator, child_locator_value)

    def point(self, parent_element: WebElement, child_locator: By, child_locator_value: str):
        self.__do_command(MouseAction.POINT, parent_element, child_locator, child_locator_value)


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

    def __do_command(self, action: SelectAction, locator: By, locator_value: str, input_option: str):
        log_task = str(action).replace("_", " ").title()
        self.log.debug(log_task + "ing the option: " + input_option + " from the Web Element " + locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(locator, locator_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Select Action " + log_task + " to Web Element " + locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Select Action " + log_task + " to Web Element " + locator_value + ".")
            else:
                break

    def select(self, locator: By, locator_value: str, input_option: str):
        self.__do_command(SelectAction.SELECT, locator, locator_value, input_option)

    def deselect(self, locator: By, locator_value: str, input_option: str):
        self.__do_command(SelectAction.DESELECT, locator, locator_value, input_option)

    def __do_command(self, action: SelectAction, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, input_option: str):
        log_task = str(action).replace("_", " ").title()
        self.log.debug(log_task + "ing the option: " + input_option + " from the Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_locator, parent_locator_value, child_locator, child_locator_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Select Action " + log_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Select Action " + log_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + parent_locator_value + ".")
            else:
                break

    def select(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, input_option: str):
        self.__do_command(SelectAction.SELECT, parent_locator, parent_locator_value, child_locator, child_locator_value, input_option)

    def deselect(self, parent_locator: By, parent_locator_value: str, child_locator: By, child_locator_value: str, input_option: str):
        self.__do_command(SelectAction.DESELECT, parent_locator, parent_locator_value, child_locator, child_locator_value, input_option)

    def __do_command(self, action: SelectAction, parent_element: WebElement, child_locator: By, child_locator_value: str, input_option: str):
        log_task = str(action).replace("_", " ").title()
        self.log.debug(log_task + "ing the option: " + input_option + " from the Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
        for x in range(3):
            element = self.element_factory.create_element(parent_element, child_locator, child_locator_value)
            action_performed = self.__execute(action, element)
            retry_count = x + 1
            if not action_performed:
                if x < 3:
                    self.log.warning("Retrying Select Action " + log_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + " " + retry_count + "/3.")
                    sleep(1)
                else:
                    self.log.error("Failed to perform Select Action " + log_task + " to Child Web Element " + child_locator_value + " under the Parent Web Element " + str(parent_element) + ".")
            else:
                break

    def select(self, parent_element: WebElement, child_locator: By, child_locator_value: str, input_option: str):
        self.__do_command(SelectAction.SELECT, parent_element, child_locator, child_locator_value, input_option)

    def deselect(self, parent_element: WebElement, child_locator: By, child_locator_value: str, input_option: str):
        self.__do_command(SelectAction.DESELECT, parent_element, child_locator, child_locator_value, input_option)

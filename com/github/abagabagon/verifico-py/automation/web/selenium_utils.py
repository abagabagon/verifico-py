import logging
import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager


class WebDriverFactory:
    def __init__(self, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of WebDriverFactory.")
        self.operating_system = None
        os.environ["GH_TOKEN"] = "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"

    def get_driver(self, browser_type: str, is_headless=False):
        """
        Get WebDriver instance.
        * browser_type - type of browser from which to run tests. Supported browsers are "GOOGLE_CHROME", "CHROMIUM",
        "BRAVE", "MOZILLA_FIREFOX", "SAFARI", "MICROSOFT_EDGE" and "INTERNET_EXPLORER"
        * is_headless - set headless mode. Note that "SAFARI" and "INTERNET_EXPLORER" headless modes are not supported.
        """
        self.operating_system = platform.system()
        if browser_type in ("GOOGLE_CHROME", "CHROMIUM", "BRAVE"):
            driver = self.__get_chrome_driver(browser_type, is_headless)
        elif browser_type == "MOZILLA_FIREFOX":
            driver = self.__get_mozilla_firefox_driver(is_headless)
        elif browser_type == "SAFARI":
            driver = self.__get_safari_driver(is_headless)
        elif browser_type == "MICROSOFT_EDGE":
            driver = self.__get_microsoft_edge_driver(is_headless)
        elif browser_type == "INTERNET_EXPLORER":
            driver = self.__get_internet_explorer_driver(is_headless)
        else:
            raise ValueError(f"{browser_type} is an unsupported Web Driver.")
        driver.maximize_window()
        return driver

    def __get_chrome_driver(self, browser_type: str, is_headless=False):
        self.log.info(f"Initializing {browser_type.replace('_', ' ').title()} Web Driver")
        if browser_type == "GOOGLE_CHROME":
            chrome_type = ChromeType.GOOGLE
        elif browser_type == "CHROMIUM":
            chrome_type = ChromeType.CHROMIUM
        elif browser_type == "BRAVE":
            chrome_type = ChromeType.BRAVE
        else:
            raise ValueError(f"Unsupported Chrome Browser: {browser_type}")

        if is_headless:
            options = ChromeOptions()
            options.headless = True
        else:
            options = None

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(chrome_type=chrome_type).install()), options=options
        )
        return driver

    def __get_mozilla_firefox_driver(self, is_headless=False):
        self.log.info(f"Initializing Mozilla Firefox Web Driver")
        if is_headless:
            options = FirefoxOptions()
            options.headless = True
        else:
            options = None

        profile = webdriver.FirefoxProfile()
        profile.set_preference("security.insecure_field_warning.contextual.enabled", False)

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
            firefox_profile=profile,
        )
        return driver

    def __get_safari_driver(self, is_headless=False):
        self.log.info(f"Initializing Safari Web Driver")
        if self.operating_system == "Darwin":
            if is_headless:
                raise ValueError("Headless is not supported for Safari Web Driver.")
            else:
                driver = webdriver.Safari()
        else:
            raise OSError(
                f"{self.operating_system} is an unsupported Operating System to run Safari Web Driver."
            )
        return driver

    def __get_microsoft_edge_driver(self, is_headless=False):
        self.log.info(f"Initializing Microsoft Edge Web Driver")
        options = EdgeOptions()
        if is_headless:
            options.headless = True

        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options,
        )
        return driver

    def __get_internet_explorer_driver(self, is_headless=False):
        self.log.info(f"Initializing Internet Explorer Web Driver")
        if self.operating_system == "Windows":
            if is_headless:
                raise ValueError("Headless is not supported for Internet Explorer Web Driver.")
            else:
                driver = webdriver.Ie(service=IEService(IEDriverManager().install()))
        else:
            raise OSError(
                f"{self.operating_system} is an unsupported Operating System to run Internet Explorer Web Driver"
            )
        return driver


class WaitCommands:
    def __init__(
        self, driver: webdriver, implicit_wait_duration: int, explicit_wait_duration: int, log=None
    ):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of WaitCommands.")
        try:
            self.driver = driver
            self.driver.implicitly_wait(implicit_wait_duration)
            self.explicit_wait_duration = explicit_wait_duration
            self.wait = WebDriverWait(self.driver, explicit_wait_duration)
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    def wait_for_url_to_be(self, url: str):
        self.log.debug(f"Waiting for URL to be: {url}")
        status = self.wait.until(expected_conditions.url_to_be(url))
        return status

    def wait_for_url_to_contain(self, value: str):
        self.log.debug(f"Waiting for URL to contain: {value}")
        status = self.wait.until(expected_conditions.url_contains(value))
        return status

    def wait_for_title_to_be(self, title: str):
        self.log.debug(f"Waiting for Title to be: {title}")
        status = self.wait.until(expected_conditions.title_is(title))
        return status

    def wait_for_title_to_contain(self, title: str):
        self.log.debug(f"Waiting for Title to contain: {title}")
        status = self.wait.until(expected_conditions.title_contains(title))
        return status

    def wait_for_element_to_be_present(self, locator: By):
        self.log.debug(f"Waiting for element: {str(locator)} to be present.")
        element = self.wait.until(expected_conditions.presence_of_element_located(locator))
        return element

    def wait_for_element_to_be_visible(self, locator: By):
        self.log.debug(f"Waiting for element: {str(locator)} to be visible.")
        element = self.wait.until(expected_conditions.visibility_of_element_located(locator))
        return element

    def wait_for_element_to_be_invisible(self, locator: By):
        self.log.debug(f"Waiting for element: {str(locator)} to be invisible.")
        status = self.wait.until(expected_conditions.invisibility_of_element_located(locator))
        return status

    def wait_for_element_to_be_clickable(self, locator: By):
        self.log.debug(f"Waiting for element:{str(locator)} to be clickable.")
        element = self.wait.until(expected_conditions.element_to_be_clickable(locator))
        return element

    def wait_for_nested_element_to_be_present(self, parent_element: WebElement, child_locator: By):
        self.log.debug(
            f"Waiting for nested element: {str(child_locator)} under parent element: {str(parent_element)} to be present."
        )
        local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
        element = local_wait.until(expected_conditions.presence_of_element_located(child_locator))
        return element

    def wait_for_nested_element_to_be_visible(self, parent_element: WebElement, child_locator: By):
        self.log.debug(
            f"Waiting for nested element: {str(child_locator)} under parent element: {str(parent_element)} to be visible."
        )
        local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
        element = local_wait.until(expected_conditions.visibility_of_element_located(child_locator))
        return element

    def wait_for_nested_element_to_be_invisible(
        self, parent_element: WebElement, child_locator: By
    ):
        self.log.debug(
            f"Waiting for nested element: {str(child_locator)} under parent element: {str(parent_element)} to be invisible."
        )
        local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
        status = local_wait.until(
            expected_conditions.invisibility_of_element_located(child_locator)
        )
        return status

    def wait_for_nested_element_to_be_clickable(
        self, parent_element: WebElement, child_locator: By
    ):
        self.log.debug(
            f"Waiting for nested element: {str(child_locator)} under parent element: {str(parent_element)} to be clickable."
        )
        local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
        element = local_wait.until(expected_conditions.element_to_be_clickable(child_locator))
        return element

    def wait_for_elements_to_be_present(self, locator: By):
        self.log.debug(f"Waiting for elements: {str(locator)} to be present.")
        elements = self.wait.until(expected_conditions.presence_of_all_elements_located(locator))
        return elements

    def wait_for_elements_to_be_visible(self, locator: By):
        self.log.debug(f"Waiting for elements: {str(locator)} to be visible.")
        elements = self.wait.until(expected_conditions.visibility_of_all_elements_located(locator))
        return elements

    def wait_for_nested_elements_to_be_present(self, parent_element: WebElement, child_locator: By):
        self.log.debug(
            f"Waiting for nested elements: {str(child_locator)} under parent element: {str(parent_element)} to be present."
        )
        local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
        elements = local_wait.until(expected_conditions.presence_of_element_located(child_locator))
        return elements

    def wait_for_nested_elements_to_be_visible(self, parent_element: WebElement, child_locator: By):
        self.log.debug(
            f"Waiting for nested elements: {str(child_locator)} under parent element: {str(parent_element)} to be visible."
        )
        local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
        elements = local_wait.until(
            expected_conditions.visibility_of_element_located(child_locator)
        )
        return elements

    def wait_for_attribute_to_be(self, locator: By, attribute: str, check_value: str):
        self.log.debug(
            f"Waiting for value of attribute: {attribute} for element: {str(locator)} to be {str(check_value)}."
        )
        status = self.wait.until(
            expected_conditions.text_to_be_present_in_element_attribute(
                locator, attribute, check_value
            )
        )
        return status

    def wait_for_text_to_be(self, locator: By, check_value: str):
        self.log.debug(
            f"Waiting for value of text for element: {str(locator)} to be {str(check_value)}."
        )
        status = self.wait.until(
            expected_conditions.text_to_be_present_in_element(locator, check_value)
        )
        return status

    def wait_for_selection_state_to_be(self, element: WebElement, expected_selected_state: bool):
        self.log.debug(f"Waiting for Selection State to be: {expected_selected_state}")
        status = self.wait.until(
            expected_conditions.element_selection_state_to_be(element, expected_selected_state)
        )
        return status

    def wait_for_alert_to_be_present(self):
        self.log.debug(f"Waiting for Javascript Alert To Be Present.")
        status = self.wait.until(expected_conditions.alert_is_present())
        return status


class WebElementFactory:
    def __init__(self, driver: webdriver, wait: WaitCommands, log=None):
        if log is None:
            self.log = logging.getLogger(__name__)
        else:
            self.log = log
        self.log.debug(f"Creating instance of WebElementFactory.")
        try:
            self.driver = driver
            self.wait = wait
        except AttributeError:
            self.log.fatal("WebDriver or Wait is not initialized!")
            raise

    def create_element(self, locator: By):
        """
        Creates and returns a Web Element.
        """
        element = self.wait.wait_for_element_to_be_present(locator)
        return element

    def create_nested_element(self, parent_element: WebElement, child_locator: By):
        """
        Creates and returns a nested Web Element.
        """
        child_element = self.wait.wait_for_nested_element_to_be_present(
            parent_element, child_locator
        )
        return child_element

    def create_elements(self, locator: By):
        """
        Creates and returns a List of Web Elements.
        """
        elements = self.wait.wait_for_elements_to_be_present(locator)
        return elements

    def create_nested_elements(self, parent_element: WebElement, child_locator: By):
        """
        Creates and returns a nested List of Web Elements.
        """
        child_elements = self.wait.wait_for_nested_elements_to_be_present(
            parent_element, child_locator
        )
        return child_elements

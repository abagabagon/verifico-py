from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class WaitCommands:

    def __init__(self, driver, implicit_wait_duration, explicit_wait_duration: int):
        print("Creating instance of WaitCommands.")
        self.element = None
        self.driver = driver
        self.implicit_wait_duration = implicit_wait_duration
        self.explicit_wait_duration = explicit_wait_duration
        self.driver.implicitly_wait(self.implicit_wait_duration)
        self.wait = WebDriverWait(self.driver, explicit_wait_duration)

    def set_implicit_wait(self, implicit_wait_duration: int):
        print("Setting Implicit Wait to " + implicit_wait_duration)
        self.driver.implicitly_wait(implicit_wait_duration)

    def set_explicit_wait(self, explicit_wait_duration: int):
        print("Setting Explicit Wait to " + explicit_wait_duration)
        self.wait = WebDriverWait(self.driver, explicit_wait_duration)

    def __execute(self, task: str, check_value: str):
        print("Waiting for " + task + ".")
        status = False
        try:
            match str:
                case "URL_TO_BE":
                    status = self.wait.until(expected_conditions.url_to_be(check_value))
                case "URL_TO_CONTAIN":
                    status = self.wait.until(expected_conditions.url_contains(check_value))
                case "TITLE_TO_BE":
                    status = self.wait.until(expected_conditions.title_is(check_value))
                case "TITLE_TO_CONTAIN":
                    status = self.wait.until(expected_conditions.title_contains(check_value))
                case default:
                    print(task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            print("Encountered TimeoutException when trying to wait for " + task + ": " + str(error_message))
        except Exception as error_message:
            print("Encountered Exception when trying to wait for " + task + ": " + str(error_message))
        return status

    def wait_for_url_to_be(self, url: str):
        print("Waiting for Page URL to match expected value.")
        status = self.__execute("URL_TO_BE", url)
        return status

    def wait_for_url_to_contain(self, url: str):
        print("Waiting for Page URL to contain expected value.")
        status = self.__execute("URL_TO_CONTAIN", url)
        return status

    def wait_for_title_to_be(self, title: str):
        print("Waiting for Page Title to match expected value.")
        status = self.__execute("TITLE_TO_BE", title)
        return status

    def wait_for_title_to_contain(self, title: str):
        print("Waiting for Page Title to contain expected value.")
        status: bool = self.__execute("TITLE_TO_CONTAIN", title)
        return status

    def __execute(self, task: str, locator: By, value: str):
        print("Waiting for " + task + ".")
        try:
            match str:
                case "ELEMENT_TO_BE_PRESENT":
                    element = self.wait.until(expected_conditions.presence_of_element_located(locator, value))
                case "ELEMENT_TO_BE_VISIBLE":
                    element = self.wait.until(expected_conditions.visibility_of_element_located(locator, value))
                case "ELEMENT_TO_BE_CLICKABLE":
                    element = self.wait.until(expected_conditions.element_to_be_clickable(locator, value))
                case default:
                    print(task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            print("Encountered TimeoutException when trying to wait for " + task + ": " + str(error_message))
        except Exception as error_message:
            print("Encountered Exception when trying to wait for " + task + ": " + str(error_message))
        return element

    def wait_for_element_to_be_present(self, locator: By, value: str):
        element = self.__execute("ELEMENT_TO_BE_PRESENT", locator, value)
        return element

    def wait_for_element_to_be_visible(self, locator: By, value: str):
        element = self.__execute("ELEMENT_TO_BE_VISIBLE", locator, value)
        return element

    def wait_for_element_to_be_clickable(self, locator: By, value: str):
        element = self.__execute("ELEMENT_TO_BE_CLICKABLE", locator, value)
        return element

    def __execute(self, task: str, parent_locator: By, parent_value: str, child_locator: By, child_value: str):
        print("Waiting for " + task + ".")
        try:
            parent_element = self.wait.until(expected_conditions.presence_of_element_located(parent_locator,
                                                                                             parent_value))
            local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
            match str:
                case "ELEMENT_TO_BE_PRESENT":
                    child_element = local_wait.until(expected_conditions.presence_of_element_located(child_locator,
                                                                                                     child_value))
                case "ELEMENT_TO_BE_VISIBLE":
                    child_element = local_wait.until(expected_conditions.visibility_of_element_located(child_locator,
                                                                                                       child_value))
                case "ELEMENT_TO_BE_CLICKABLE":
                    child_element = local_wait.until(expected_conditions.element_to_be_clickable(child_locator,
                                                                                                 child_value))
                case default:
                    print(task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            print("Encountered TimeoutException when trying to wait for " + task + ": " + str(error_message))
        except Exception as error_message:
            print("Encountered Exception when trying to wait for " + task + ": " + str(error_message))
        return child_element

    def wait_for_element_to_be_present(self, parent_locator: By, parent_value: str, child_locator: By,
                                       child_value: str):
        element = self.__execute("ELEMENT_TO_BE_PRESENT", parent_locator, parent_value, child_locator, child_value)
        return element

    def wait_for_element_to_be_visible(self, parent_locator: By, parent_value: str, child_locator: By,
                                       child_value: str):
        element = self.__execute("ELEMENT_TO_BE_VISIBLE", parent_locator, parent_value, child_locator, child_value)
        return element

    def wait_for_element_to_be_clickable(self, parent_locator: By, parent_value: str, child_locator: By,
                                         child_value: str):
        element = self.__execute("ELEMENT_TO_BE_CLICKABLE", parent_locator, parent_value, child_locator, child_value)
        return element

    def __execute(self, task: str, parent_element: WebElement, child_locator: By):
        print("Waiting for " + task + ".")
        try:
            local_wait = WebDriverWait(parent_element, self.explicit_wait_duration)
            match str:
                case "ELEMENT_TO_BE_PRESENT":
                    child_element = local_wait.until(expected_conditions.presence_of_element_located(child_locator))
                case "ELEMENT_TO_BE_VISIBLE":
                    child_element = local_wait.until(expected_conditions.visibility_of_element_located(child_locator))
                case "ELEMENT_TO_BE_CLICKABLE":
                    child_element = local_wait.until(expected_conditions.element_to_be_clickable(child_locator))
                case default:
                    print(task + " is an unsupported Wait Command.")
        except TimeoutException as error_message:
            print("Encountered TimeoutException when trying to wait for " + task + ": " + str(error_message))
        except Exception as error_message:
            print("Encountered Exception when trying to wait for " + task + ": " + str(error_message))
        return child_element

    def wait_for_element_to_be_present(self, parent_element: WebElement, child_locator: By):
        element = self.__execute("ELEMENT_TO_BE_PRESENT", parent_element, child_locator)
        return element

    def wait_for_element_to_be_visible(self, parent_element: WebElement, child_locator: By):
        element = self.__execute("ELEMENT_TO_BE_VISIBLE", parent_element, child_locator)
        return element

    def wait_for_element_to_be_clickable(self, parent_element: WebElement, child_locator: By):
        element = self.__execute("ELEMENT_TO_BE_CLICKABLE", parent_element, child_locator)
        return element

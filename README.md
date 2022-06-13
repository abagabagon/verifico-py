[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# **Background**
One of the disadvantages of Selenium and Appium is the steep learning curve required for users to be able to implement it. One also have to go over issues such as automation test flakiness, unhandled exceptions, etc. so they could learn how to properly implement commands of Selenium and Appium. The project is built in order to eliminate this issue.

# **Components**

| Component      | Python API                                       |
|----------------|--------------------------------------------------|
| Web Automation | [Selenium](https://www.seleniumhq.org/download/) |

# **Web Automation**

For Web Application Automation, create an instance of the `WebDriverFactory` Class to initialize and get WebDrivers:

```python
self.driver_factory = WebDriverFactory()
self.driver = self.driver_factory.get_chrome_driver()
```

Supported WebDrivers are as follows
* Google Chrome
* Chromium
* Brave
* Mozilla Firefox
* Safari
* Microsoft Edge
* Internet Explorer

Wait Commands are also available at the `WaitCommands` Class by which functions are utilized by other Automation Command Classes. User will only need to initialize Implicit and Explicit Waits. The instance of the `WaitCommands` Class will be utilized by Automation Command Classes which are discussed on below other sections.

```python
self.implicit_wait_duration = 10
self.explicit_wait_duration = 5
self.wait = WaitCommands(self.driver, self.implicit_wait_duration, self.explicit_wait_duration)
```

Web Application Automation Commands are accessible into classes from which related commands are grouped. Note that for commands that manipulates Web Elements, variations of the commands are created to accommodate actions for target Web Elements that are nested (e. g. tables, lists, etc.). Available Command Classes are shown below:

## **Browser Commands**

Browser Commands contains functions relating to actions being done by the user at the Web Browser. Class name for this is `BrowserCommands`.

`BrowserCommands` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands`:

```python
self.browser = BrowserCommands(self.driver, self.wait)
self.browser.go_to("https://www.google.com/")
self.browser.maximize()
self.browser.refresh()
```

| Command                   | Description                                                 |
|---------------------------|-------------------------------------------------------------|
| `open_tab`                | Opens Tab                                                   |
| `go_to`                   | Navigates to the Url specified                              |
| `switch_tab_by_title`     | Switches to a Tab based on Page Title                       |
| `switch_tab_by_url`       | Switches to a Tab based on Page URL                         |
| `switch_tab_to_original`  | Switches back to Original Tab                               |
| `back`                    | Navigates one item back from the browser's history          |
| `forward`                 | Navigates one item forward from the browser's history       |
| `refresh`                 | Refreshes current page                                      |
| `maximize`                | Maximizes Browser Window                                    |
| `delete_all_cookies`      | Deletes all cookies                                         |
| `scroll`                  | Scrolls Page                                                |
| `close_tab`               | Closes Tab of a Web Browser                                 |
| `close_browser`           | Closes Web Browser                                          |
| `count`                   | Counts instance of the Web Element of the specified Locator |

## **Mouse Commands**

Mouse Commands contains functions pertaining to mouse actions done by a user at a Web Page. Class for this is `MouseCommands`.

`MouseCommands` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands` Classes:

```python
self.mouse = MouseCommands(self.driver, self.wait)
self.browser.go_to("https://www.google.com/")
self.mouse.click(by=By.XPATH, "//button[@name='Search']")
```

| Command          | Description                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `point`          | Points mouse to the Web Element of the specified Locator.                                      |
| `click`          | Clicks the Web Element of the specified Locator.                                               |
| `click_js`       | Clicks the Web Element of the specified Locator using Javascript.                              |
| `click_and_hold` | Clicks and holds the Web Element of the specified Locator.                                     |
| `double_click`   | Double-clicks the Web Element of the specified Locator.                                        |
| `drag_and_drop`  | Drags a Web Element and drops it at target Web Element. Used for Elements that can be dragged. |

## **Keyboard Commands**

Keyboard Commands contains functions pertaining to keyboard actions done by a user in a Web Page. Class for this is `KeyboardCommands`.

`KeyboardCommands` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands` Classes:

```python
self.keyboard = KeyboardCommands(self.driver, self.wait)
self.browser.go_to("https://www.google.com/")
self.keyboard.type(by=By.XPATH, "//input[@name='username']", "user@sample.com")
self.keyboard.type(by=By.XPATH, "//input[@name='password']", "password123")
```

| Command  | Description                                                                                                                 |
|----------|-----------------------------------------------------------------------------------------------------------------------------|
| `type`   | Types the specified input text to the Web Element of the specified Locator. Applicable for INPUT and TEXTAREA Web Elements. |
| `press`  | Simulates pressing of characters into the Web Element of the specified Locator.                                             |
| `clear`  | Clears value of the Web Element of the specified Locator. Applicable for INPUT and TEXTAREA Web Elements.                   |

## **Select Commands**

Select Commands contains functions pertaining to actions done by a user on drop-down elements in a Web Page. Class for this is `SelectCommands`.

`SelectCommands` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands` Classes:

```python
self.select = SelectCommands(self.driver, self.wait)
self.browser.go_to("https://www.google.com/");
self.select.select(by=By.XPATH, "//select[@type='member-type']", "Guest")
```

| Command    | Description                                                              |
|------------|--------------------------------------------------------------------------|
| `select`   | Selects a Drop-down List Web Element Option of the specified Locator.    |
| `deselect` | De-selects a Drop-down List Web Element Option of the specified Locator. |

## **Get Commands**

Get Commands contains functions pertaining to get value actions done by a user in a Web Page. Class for this is `GetCommands`.

`GetCommands` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands` Classes:

```python
self.get = GetCommands(self.driver, self.wait)
self.browser.go_to("https://www.google.com/");
self.header = self.get.getText(by=By.XPATH, "//h1[@name='Login Header']");
```

| Command                   | Description                                                                |
|---------------------------|----------------------------------------------------------------------------|
| `get_text`                | Gets the text of the Web Element of the specified Locator.                 |
| `get_attribute_value`     | Gets the attribute value of the Web Element of the specified Locator.      |
| `get_dropdown_list_value` | Gets the drop-down list value of the Web Element of the specified Locator. |

## **Alert Commands**

Alert Commands contains functions pertaining to get value actions done by a user in a Web Page. Class for this is `AlertCommands`.

`AlertCommands` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands` Classes:

```python
self.alert = AlertCommands(self.driver, self.wait)
self.mouse.click(by=By.XPATH, "//input[@id='alertbtn']")
self.alert.type_alert("John")
self.alert.accept_alert()
```

| Command        | Description                                    |
|----------------|------------------------------------------------|
| `accept_alert` | Accepts Javascript Alert                       |
| `cancel_alert` | Cancels Javascript Alert                       |
| `type_alert`   | Simulates typing at Javascript Alert Text Box  |

## **Value Assertions**

Value Assertions contains functions pertaining to checking of values done by a user in a Web Page. Class for this is `ValueAssertions`.

`ValueAssertions` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands` Classes:

```python
self.value = ValueAssertions(self.driver, self.wait)
self.browser.go_to("https://www.google.com/")
self.value.see_url("https://www.google.com/")
self.keyboard.type(by=By.XPATH, "//input[@id='search-box']", "verifico")
self.value.see_attribute_value(by=By.XPATH, "//input[@id='search-box']", "value", "verifico")
```

| Command                            | Description                                                                                                            |
|------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| `see_url`                          | Verifies Page URL of Web Page if equal to the expected URL.                                                            |
| `dont_see_url`                     | Verifies Page URL of Web Page if not equal to the specified URL.                                                       |
| `see_partial_url`                  | Verifies Page URL of Web Page if partially equal to the expected URL.                                                  |
| `dont_see_partial_url`             | Verifies Page URL of Web Page if not partially equal to the expected URL.                                              |
| `see_title`                        | Verifies Page Title of Web Page if equal to the expected Title.                                                        |
| `dont_see_title`                   | Verifies Page Title of Web Page if not equal to the specified Title.                                                   |
| `see_partial_title`                | Verifies Page Title of Web Page if partially equal to the expected Title.                                              |
| `dont_see_partial_title`           | Verifies Page Title of Web Page if not partially equal to the specified Title.                                         |
| `see_attribute_value`              | Verifies the attribute value of the Web Element of the specified Locator if equal to the expected value.               |
| `dont_see_attribute_value`         | Verifies the attribute value of the Web Element of the specified Locator if not equal to the expected value.           |
| `see_partial_attribute_value`      | Verifies the attribute value of the Web Element of the specified Locator if partially equal to the expected value.     |
| `dont_see_partial_attribute_value` | Verifies the attribute value of the Web Element of the specified Locator if not partially equal to the expected value. |
| `see_text`                         | Verifies the text value of the Web Element of the specified Locator if equal to the expected value.                    |
| `dont_see_text`                    | Verifies the text value of the Web Element of the specified Locator if not equal to the expected value.                |
| `see_partial_text`                 | Verifies the text value of the Web Element of the specified Locator if partially equal to the expected value.          |
| `dont_see_partial_text`            | Verifies the text value of the Web Element of the specified Locator if not partially equal to the expected value.      |
| `see_dropdown_value`               | Verifies the dropdown value of the Web Element of the specified Locator if equal to the expected value.                |
| `dont_see_dropdown_value`          | Verifies the dropdown value of the Web Element of the specified Locator if not equal to the expected value.            |
| `see_partial_dropdown_value`       | Verifies the dropdown value of the Web Element of the specified Locator if equal to the expected value.                |
| `dont_see_partial_dropdown_value`  | Verifies the dropdown value of the Web Element of the specified Locator if not partially equal to the expected value.  |
| `counted`                          | Verifies Web Element Instance count is equal to expected count.                                                        |
| `see_alert_message`                | Verifies Javascript Alert Message displayed if equal to expected message                                               |

## **State Assertions**

State Assertions contains functions pertaining to checking the state of Web Elements done by a user in a Web Page. Class for this is `StateAssertions`.

`StateAssertions` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands` Classes:

```python
self.state = StateAssertions(self.driver, self.wait)
self.browser.go_to("https://www.practicesite.com/")
self.state.see(by=By.XPATH, "//input[@name='show-hide-text']")
self.mouse.click(by=By.XPATH, "//input[@id='hide-textbox']")
self.state.dont_see(by=By.XPATH,"//input[@name='show-hide-text']")
```

| Command          | Description                                                                                                                                 |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `see`            | Verifies if Web Element of specified Locator is displayed on Web Page.                                                                      |
| `dont_see`       | Verifies if Web Element of specified Locator is not displayed on Web Page.                                                                  |
| `see_enabled`    | Verifies if Web Element of specified Locator is enabled on Web Page.                                                                        |
| `see_disabled`   | Verifies if Web Element of specified Locator is disabled on Web Page.                                                                       |
| `see_selected`   | Verifies if Web Element of specified Locator within the context of the Web Element of the specified Parent Locator is selected on Web Page. |
| `see_deselected` | Verifies if Web Element of specified Locator is deselected on Web Page.                                                                     |

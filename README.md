# Verifico Python

## **Background**
As observed, testing of certain projects can involve web-based applications. Given that the goal is to automate testing, a web-based automation tool is a must.

## Automation
To eliminate learning curve, Selenium Commands are wrapped into Web Application Automation Commands that are accessible into classes from which related commands are grouped. Note that for commands that manipulates Web Elements, variations of the commands are created to accommodate actions for target Web Elements that are nested (e. g. tables, lists, etc.). Available Command Classes are shown below:

### **Browser Commands**

Browser Commands contains functions relating to actions being done by the user at the Web Browser. Class name for this is `BrowserCommands`.

`BrowserCommands` Class can be instantiated below using the instantiated `WebDriverFactory` and `WaitCommands`:

```python
self.webdriver_factory = WebDriverFactory()
self.driver = self.webdriver_factory.get_driver("GOOGLE_CHROME")
self.wait = WaitCommands(self.driver, 10, 5)
self.browser = BrowserCommands(self.driver)
self.browser.open_browser()
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

#### **Browser Support**
Supported Web Browsers are as follows:
* Google Chrome
* Chromium
* Brave
* Mozilla Firefox
* Safari
* Microsoft Edge
* Internet Explorer

### **Mouse Commands**

Mouse Commands contains functions pertaining to mouse actions done by a user at a Web Page. Class for this is `MouseCommands`.

`MouseCommands` Class can be instantiated below: 

```python
self.mouse_command = MouseCommands(self.driver, self.wait)
self.browser_command.go_to("https://www.google.com/")
self.mouse_command.click((By.XPATH, "//button[@name='Search']"))
```

| Command          | Description                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `point`          | Points mouse to the Web Element of the specified Locator.                                      |
| `click`          | Clicks the Web Element of the specified Locator.                                               |
| `click_js`       | Clicks the Web Element of the specified Locator using Javascript.                              |
| `click_and_hold` | Clicks and holds the Web Element of the specified Locator.                                     |
| `double_click`   | Double-clicks the Web Element of the specified Locator.                                        |
| `drag_and_drop`  | Drags a Web Element and drops it at target Web Element. Used for Elements that can be dragged. |

### **Keyboard Commands**

Keyboard Commands contains functions pertaining to keyboard actions done by a user in a Web Page. Class for this is `KeyboardCommands`.

`KeyboardCommands` Class can be instantiated below:

```python
self.keyboard_command = KeyboardCommands(self.driver, self.wait)
self.browser_command.go_to("https://www.google.com/")
self.keyboard_command.type((By.XPATH, "//input[@name='username']", "user@sample.com"))
self.keyboard_command.type((By.XPATH, "//input[@name='password']", "password123"))
```

| Command  | Description                                                                                                                 |
|----------|-----------------------------------------------------------------------------------------------------------------------------|
| `type`   | Types the specified input text to the Web Element of the specified Locator. Applicable for INPUT and TEXTAREA Web Elements. |
| `press`  | Simulates pressing of characters into the Web Element of the specified Locator.                                             |
| `clear`  | Clears value of the Web Element of the specified Locator. Applicable for INPUT and TEXTAREA Web Elements.                   |

### **Select Commands**

Select Commands contains functions pertaining to actions done by a user on drop-down elements in a Web Page. Class for this is `SelectCommands`.

`SelectCommands` Class can be instantiated below:

```python
self.select_command = SelectCommands(self.driver, self.wait)
self.browser_command.go_to("https://www.google.com/");
self.select_command.select((By.XPATH, "//select[@type='member-type']", "Guest"))
```

| Command    | Description                                                              |
|------------|--------------------------------------------------------------------------|
| `select`   | Selects a Drop-down List Web Element Option of the specified Locator.    |
| `deselect` | De-selects a Drop-down List Web Element Option of the specified Locator. |

### **Get Commands**

Get Commands contains functions pertaining to get value actions done by a user in a Web Page. Class for this is `GetCommands`.

`GetCommands` Class can be instantiated below:

```python
self.get_command = GetCommands(self.driver, self.wait)
self.browser_command.go_to("https://www.google.com/");
self.header = self.get_command.getText((By.XPATH, "//h1[@name='Login Header']"));
```

| Command               | Description                                                                |
|-----------------------|----------------------------------------------------------------------------|
| `get_text`            | Gets the text of the Web Element of the specified Locator.                 |
| `get_attribute_value` | Gets the attribute value of the Web Element of the specified Locator.      |
| `get_dropdown_value`  | Gets the drop-down list value of the Web Element of the specified Locator. |

### **Alert Commands**

Alert Commands contains functions pertaining to Javascript Alerts in a Web Page. Class for this is `AlertCommands`.

`AlertCommands` Class can be instantiated below:

```python
self.alert_command = AlertCommands(self.driver, self.wait)
self.mouse_command.click((By.XPATH, "//input[@id='alertbtn']"))
self.alert_command.type_alert("John")
self.alert_command.accept_alert()
```

| Command        | Description                                    |
|----------------|------------------------------------------------|
| `accept_alert` | Accepts Javascript Alert                       |
| `cancel_alert` | Cancels Javascript Alert                       |
| `type_alert`   | Simulates typing at Javascript Alert Text Box  |

### **Value Assertions**

Value Assertions contains functions pertaining to checking of values done by a user in a Web Page. Class for this is `ValueAssertions`.

`ValueAssertions` Class can be instantiated below:

```python
self.value_assertion = ValueAssertions(self.driver, self.wait)
self.browser_command.go_to("https://www.google.com/")
self.value_assertion.see_url("https://www.google.com/")
self.keyboard_command.type((By.XPATH, "//input[@id='search-box']", "verifico"))
self.value_assertion.see_attribute_value((By.XPATH, "//input[@id='search-box']", "value", "verifico"))
```

| Command                               | Description                                                                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `see_url`                             | Verifies Page URL of Web Page if equal to the expected URL.                                                                 |
| `dont_see_url`                        | Verifies Page URL of Web Page if not equal to the specified URL.                                                            |
| `see_partial_url`                     | Verifies Page URL of Web Page if partially equal to the expected URL.                                                       |
| `dont_see_partial_url`                | Verifies Page URL of Web Page if not partially equal to the expected URL.                                                   |
| `see_title`                           | Verifies Page Title of Web Page if equal to the expected Title.                                                             |
| `dont_see_title`                      | Verifies Page Title of Web Page if not equal to the specified Title.                                                        |
| `see_partial_title`                   | Verifies Page Title of Web Page if partially equal to the expected Title.                                                   |
| `dont_see_partial_title`              | Verifies Page Title of Web Page if not partially equal to the specified Title.                                              |
| `see_attribute_value`                 | Verifies the attribute value of the Web Element of the specified Locator if equal to the expected value.                    |
| `dont_see_attribute_value`            | Verifies the attribute value of the Web Element of the specified Locator if not equal to the expected value.                |
| `see_partial_attribute_value`         | Verifies the attribute value of the Web Element of the specified Locator if partially equal to the expected value.          |
| `dont_see_partial_attribute_value`    | Verifies the attribute value of the Web Element of the specified Locator if not partially equal to the expected value.      |
| `see_text`                            | Verifies the text value of the Web Element of the specified Locator if equal to the expected value.                         |
| `dont_see_text`                       | Verifies the text value of the Web Element of the specified Locator if not equal to the expected value.                     |
| `see_partial_text`                    | Verifies the text value of the Web Element of the specified Locator if partially equal to the expected value.               |
| `dont_see_partial_text`               | Verifies the text value of the Web Element of the specified Locator if not partially equal to the expected value.           |
| `see_dropdown_option`                 | Verifies the Drop-down List value of the Web Element of the specified Locator if equal to the selected value.               |
| `dont_see_dropdown_option`            | Verifies the Drop-down List value of the Web Element of the specified Locator if not equal to the selected value.           |
| `see_partial_dropdown_option`         | Verifies the Drop-down List value of the Web Element of the specified Locator if partially equal to the selected value.     |
| `dont_see_partial_dropdown_option`    | Verifies the Drop-down List value of the Web Element of the specified Locator if not partially equal to the selected value. |
| `see_multiselect_option`              | Verifies the Multi-select value of the Web Element of the specified Locator if it is one of the selected values.            |
| `dont_see_multiselect_option`         | Verifies the Multi-select value of the Web Element of the specified Locator if it is not one of the selected values.        |
| `see_partial_multiselect_option`      | Verifies the Multi-select value of the Web Element of the specified Locator if it is one of the selected values.            |
| `dont_see_partial_multiselect_option` | Verifies the Multi-select value of the Web Element of the specified Locator if it is not one of the selected values.        |
| `see_alert_message`                   | Verifies Javascript Alert Message displayed if equal to expected message                                                    |
| `dont_see_alert_message`              | Verifies Javascript Alert Message displayed if not equal to expected message                                                |

### **State Assertions**

State Assertions contains functions pertaining to checking the state of Web Elements done by a user in a Web Page. Class for this is `StateAssertions`.

`StateAssertions` Class can be instantiated below:

```python
self.state_assertion = StateAssertions(self.driver, self.wait)
self.browser_command.go_to("https://www.practicesite.com/")
self.state_assertion.see((By.XPATH, "//input[@name='show-hide-text']"))
self.mouse_command.click((By.XPATH, "//input[@id='hide-textbox']"))
self.state_assertion.dont_see((By.XPATH,"//input[@name='show-hide-text']"))
```

| Command                     | Description                                                                |
|-----------------------------|----------------------------------------------------------------------------|
| `see`                       | Verifies if Web Element of specified Locator is displayed on Web Page.     |
| `dont_see`                  | Verifies if Web Element of specified Locator is not displayed on Web Page. |
| `enabled`                   | Verifies if Web Element of specified Locator is enabled on Web Page.       |
| `disabled`                  | Verifies if Web Element of specified Locator is disabled on Web Page.      |
| `selected`                  | Verifies if Web Element of specified Locator is selected on Web Page.      |
| `deselected`                | Verifies if Web Element of specified Locator is deselected on Web Page.    |
| `see_alert_is_present`      | Verifies that a Javascript Alert is present on the Web Page.               |
| `dont_see_alert_is_present` | Verifies that a Javascript Alert is not present on the Web Page.           |


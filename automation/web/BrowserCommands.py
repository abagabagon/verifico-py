from selenium import webdriver


class BrowserCommands:

    def __init__(self, driver: webdriver):
        print("Creating instance of BrowserCommands.")
        self.driver = driver

    def __execute(self, task: str, input_value: str):
        print("Performing " + task + " Browser Action.")
        try:
            match str:
                case "OPEN_TAB":
                    self.driver.execute_script("window.open('" + input_value + "', '_blank');")
                case "MAXIMIZE":
                    self.driver.maximize_window()
                case "DELETE_ALL_COOKIES":
                    self.driver.delete_all_cookies()
                case "GO_TO":
                    self.driver.get(input_value)
                case "BACK":
                    self.driver.back()
                case "FORWARD":
                    self.driver.forward()
                case "REFRESH":
                    self.driver.refresh()
                case "CLOSE_TAB":
                    self.driver.close()
                case "CLOSE_BROWSER":
                    self.driver.quit()
                case default:
                    print("Unsupported Browser Action: " + task)
        except Exception as error_message:
            print("Encountered Exception when trying to perform task " + task + " Web Driver: " + str(error_message))
            exit(1)

    def open_tab(self, url: str):
        self.__execute("OPEN_TAB", url)

    def maximize(self):
        self.__execute("MAXIMIZE", None)

    def delete_all_cookies(self):
        self.__execute("DELETE_ALL_COOKIES", None)

    def go_to(self, url: str):
        self.__execute("GO_TO", url)

    def back(self):
        self.__execute("BACK", None)

    def forward(self):
        self.__execute("FORWARD", None)

    def refresh(self):
        self.__execute("REFRESH", None)

    def close_tab(self):
        self.__execute("CLOSE_TAB", None)

    def close_browser(self):
        self.__execute("CLOSE_BROWSER", None)

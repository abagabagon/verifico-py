from selenium import webdriver
from automation.web.WaitCommands import WaitCommands


class AlertCommands:

    def __init__(self, driver: webdriver, wait: WaitCommands):
        self.driver = driver
        self.wait = wait

    def accept_alert(self):
        print("Performing ACCEPT Javascript Alert.");
        alert = self.wait.wait_for_alert_to_be_present()
        alert.accept()

    def cancel_alert(self):
        print("Performing CANCEL Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.dismiss()

    def type_alert(self, input_text: str):
        print("Performing TYPE INTO Javascript Alert.");
        alert = self.wait.wait_for_alert_to_be_present()
        alert.send_keys(input_text)

from enum import Enum

from selenium import webdriver
from automation.web.WaitCommands import WaitCommands
import logging
from enum import Enum, auto


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
        self.log.debug("Performing " + str(AlertAction.ACCEPT) + " Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.accept()

    def cancel_alert(self):
        self.log.debug("Performing " + str(AlertAction.CANCEL) + " Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.dismiss()

    def type_alert(self, input_text: str):
        self.log.debug("Performing " + str(AlertAction.TYPE_INTO).replace("_", " ") + " Javascript Alert.")
        alert = self.wait.wait_for_alert_to_be_present()
        alert.send_keys(input_text)

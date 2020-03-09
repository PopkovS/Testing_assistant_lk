from time import sleep

import pytest

from pages.base_page import BasePage
from pages.locators import Links, TestData
from pages.login_page import LoginLocators


class MyDevicePage(BasePage):
    def go_to_my_devices(self):
        self.login_from_my_dev()
        self.open()

    def go_to_create_group(self):
        self.login_from_my_dev()
        current_link = self.browser.current_url
        if Links.MY_DEVICE_CREATE_GROUP in current_link:
            self.browser.get(Links.MY_DEVICE_CREATE_GROUP)

    def login_from_my_dev(self):
        current_link = self.browser.current_url
        if Links.LOGIN_LINK in current_link:
            self.login()

    def set_groups_fields(self):
        group_name_field = self.browser.find_elements()



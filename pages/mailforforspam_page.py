from time import sleep

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pages.pg_data_base as pgdb
import pyperclip as pypc
import requests
from pages.base_page import BasePage
from pages.locators import LoginLocators, MailForSpamLocators, Links, TestData


class MailForSpamPage(BasePage):

    def check_mail(self, old_lett):
        i = 1
        while True:
            letter_id = last_letter_id()
            if old_lett < letter_id:
                check_button = self.browser.find_element(*MailForSpamLocators.CHECK_BUTTON)
                check_button.click()
                break
            else:
                assert i <= 60, f"Не удалось получить нужное письмо id предыдущего {old_lett}, id последнего {letter_id} "
                check_button = self.browser.find_element(*MailForSpamLocators.CHECK_BUTTON)
                check_button.click()
                i += 1
                continue

    def open_first_letter(self):
        letters = self.browser.find_elements(*MailForSpamLocators.LETTERS)
        letters[0].click()

    def go_to_password_conf(self):
        self.open_first_letter()
        link_to_change_pass = self.browser.find_element(*MailForSpamLocators.LINK_GO_TO_CHANGE_PASS)
        link_to_change_pass.click()

    def get_conf_code(self):
        self.open_first_letter()
        print(self.browser.find_element(*MailForSpamLocators.CONFIRMATION_CODE).text)
        pypc.copy(self.browser.find_element(*MailForSpamLocators.CONFIRMATION_CODE).text)


def last_letter_id():
    link = Links.MAIL_FOR_SPAM_LINK + TestData.TEST_USER.split("@")[0]
    response = requests.get(link).text.split("\n")
    id_list = []
    for i in response:
        i = i.strip()
        if i.startswith("<tr onclick"):
            id_list.append(int(i.replace("'", "/").split("/")[-2]))
    if len(id_list) == 0:
        return 0
    else:
        return max(id_list)


print(last_letter_id())

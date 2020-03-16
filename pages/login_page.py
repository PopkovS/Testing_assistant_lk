from time import sleep

import pyperclip as pypc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
from .locators import LoginLocators, Links, TestData, BaseLocators, RegistrationLocators
from .mailforforspam_page import MailForSpamPage, last_letter_id


class LoginPage(BasePage):
    def set_email(self, email):
        self.fill_email(email)
        self.click_submit()

    def send_confirm_code(self):
        self.is_element_present(*LoginLocators.CONF_CODE_FIELD, timeout=8)
        conf_pass_field = self.browser.find_element(*LoginLocators.CONF_CODE_FIELD)
        cod = pypc.paste()
        conf_pass_field.send_keys(cod)
        self.browser.find_element(*LoginLocators.SUBMIT_CONF_PASS).click()

    def set_password_confirm(self, password, password_conf):
        password_field = self.browser.find_element(*BaseLocators.PASSWORD_FIELD)
        password_field.send_keys(password)
        password_field = self.browser.find_element(*BaseLocators.PASSWORD_CONFIRM_FIELD)
        password_field.send_keys(password_conf)
        self.click_submit()

    def set_password_confirm_wihtout_login(self, password, password_conf):
        password_field = self.browser.find_element(*BaseLocators.PASSWORD_FIELD)
        password_field.send_keys(password)
        password_field = self.browser.find_element(*BaseLocators.PASSWORD_CONFIRM_FIELD)
        password_field.send_keys(password_conf)

    def go_to_login_from_set_password(self):
        self.browser.find_element(*RegistrationLocators.GO_TO_LOGIN_PAGE_FROM_REG).click()

    def go_to_set_password_page(self):
        current_link = self.browser.current_url
        if Links.LOGIN_LINK not in current_link:
            self.browser.get(Links.LOGIN_LINK)
        else:
            self.browser.refresh()
        butt = self.browser.find_element(*LoginLocators.GO_TO_SET_PASS_BUTT)
        butt.click()

    def go_to_resending_page(self):
        current_link = self.browser.current_url

        if Links.RESEND_EMAIL_LINK not in current_link:
            self.open()
            self.is_element_present(*LoginLocators.GO_TO_RESEND_EMAIL_BUTT)
            butt = self.browser.find_element(*LoginLocators.GO_TO_RESEND_EMAIL_BUTT)
            butt.click()
        else:
            self.browser.refresh()

    def go_to_set_password_conf_page(self, user=TestData.USER_NORMAL_EMAIL):
        old_lett = last_letter_id()
        current_link = self.browser.current_url
        if f"{Links.SET_PASSWORD_LINK}Confirm?email={user}" not in current_link:
            self.go_to_set_password_page()
            self.set_email(user)
            self.should_be_title_page()
            self.new_tab()
            print(f"Старый счетчик писем {old_lett}")
            mail_page = MailForSpamPage(self.browser, self.browser.current_url)
            mail_page.check_mail(old_lett)
            mail_page.go_to_link_from_letter()

    def go_to_account_activation(self, old_lett, link=Links.MAIL_FOR_SPAM_NORM_US):
        self.new_tab(link=link)
        print(f"Старый счетчик писем {old_lett}")
        mail_page = MailForSpamPage(self.browser, self.browser.current_url)
        mail_page.check_mail(old_lett, link=link)
        mail_page.go_to_link_from_letter()

    def get_conf_code(self, link=Links.MAIL_FOR_SPAM_NORM_US):
        old_lett = last_letter_id(link)
        self.new_tab(link)
        mail_page = MailForSpamPage(self.browser, self.browser.current_url)
        mail_page.check_mail(old_lett, link)
        mail_page.get_conf_code()
        mail_page.close_tab()
        mail_page.switch_to_tab(0)

    def click_submit(self):
        submit = self.browser.find_element(*BaseLocators.SUBMIT_BUTTON)
        submit.click()

    def fill_password(self, password):
        password_field = self.browser.find_element(*LoginLocators.PASSWORD_USER_FIELD)
        password_field.send_keys(password)

    def fill_email(self, email):
        email_field = self.browser.find_element(*LoginLocators.EMAIL_FIELD)
        email_field.send_keys(email)

    def login_twofac(self, email=TestData.USER_AD_EMAIL, name=TestData.USER_AD_NAME, password=TestData.PASSWORD_USER_AD,
                     link=Links.MAIL_FOR_SPAM_AD_US):
        self.change_user_stat(0, tfac="true", email=email)
        self.login(name, password)
        self.get_conf_code(link=link)
        self.send_confirm_code()
        self.change_user_stat(0, tfac="false", email=email)

    def should_be_resending_email_page(self):
        self.should_be_title_page(text="resending emails", locator=LoginLocators.RESEND_EMAIL_TITLE)
        self.should_be_match_link(link=Links.RESEND_EMAIL_LINK)

    def should_be_err_mess_password(self, var, locator=LoginLocators.ERR_MESS_PASSWORD):
        self.should_be_err_mess(var, locator)

    def should_be_err_mess_email(self, var):
        locator = LoginLocators.ERR_MESS_EMAIL
        self.should_be_err_mess(var, locator)

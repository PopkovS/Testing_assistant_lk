import pyperclip as pypc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
from .locators import LoginLocators, Links, TestData, BaseLocators
from .mailforforspam_page import MailForSpamPage, last_letter_id


class LoginPage(BasePage):
    def set_password(self, email):
        self.fill_email(email)
        self.click_submit()

    def send_confirm_code(self):
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



    # def create_test_user(self):
    #     if pgdb.check_user_exist() is False:
    #         req.send_pack("create_user")
    #         req.request_sending_edit_user(id_user=pgdb.get_id_user())
    #     else:
    #         req.send_pack("edit_user")

    def go_to_set_password_page(self):
        current_link = self.browser.current_url
        if current_link == Links.LOGIN_LINK:
            butt = self.browser.find_element(*LoginLocators.GO_TO_SET_PASS_BUTT)
            butt.click()

    def go_to_set_password_conf_page(self, user=TestData.TEST_USER_NORMAL):
        old_lett = last_letter_id()
        current_link = self.browser.current_url
        if f"{Links.SET_PASSWORD_LINK}Confirm?email={user}" not in current_link:
            self.go_to_set_password_page()
            self.set_password(user)
            self.should_be_title_page()
            self.new_tab()
            print(f"Старый счетчик писем {old_lett}")
            mail_page = MailForSpamPage(self.browser, self.browser.current_url)
            mail_page.check_mail(old_lett)
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

    def should_be_err_mess_password(self, var, locator=LoginLocators.ERR_MESS_PASSWORD):
        self.should_be_err_mess(var, locator)

    def should_be_err_mess_email(self, var):
        locator = LoginLocators.ERR_MESS_EMAIL
        self.should_be_err_mess(var, locator)



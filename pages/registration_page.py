import pyperclip as pypc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pages.pg_data_base as pgdb
from .base_page import BasePage
from .locators import LoginLocators, Links, TestData, RegistrationLocators, BaseLocators
from .mailforforspam_page import MailForSpamPage, last_letter_id


class RegistrationPage(BasePage):
    def go_to_reg_page(self):
        current_link = self.browser.current_url
        if Links.LOGIN_LINK in current_link:
            self.browser.find_element(*RegistrationLocators.GO_TO_REGISTRATION_PAGE).click()
        else:
            self.browser.get(Links.REGISTRATION_LINK)
        self.should_be_title_page(text="registration", locator=RegistrationLocators.REGISTRATION_TITLE)

    def old_letters_count(self, link=Links.MAIL_FOR_SPAM_NEW_US):
        return last_letter_id(link)

    def go_to_account_activation(self, old_lett, link=Links.MAIL_FOR_SPAM_NEW_US):
        self.new_tab(link=link)
        print(f"Старый счетчик писем {old_lett}")
        mail_page = MailForSpamPage(self.browser, self.browser.current_url)
        mail_page.check_mail(old_lett, link=link)
        mail_page.go_to_link_from_letter()

    def go_to_login_page_from_confirm_reg(self):
        self.browser.find_element(*RegistrationLocators.GO_TO_LOGIN_PAGE_FROM_REG).click()

    def registration(self, email, name, password, conf_password):
        email_field = self.browser.find_element(*BaseLocators.EMAIL_FIELD)
        email_field.send_keys(email)
        name_field = self.browser.find_element(*BaseLocators.NAME_FIELD)
        name_field.send_keys(name)
        password_field = self.browser.find_element(*BaseLocators.PASSWORD_FIELD)
        password_field.send_keys(password)
        conf_password_field = self.browser.find_element(*BaseLocators.PASSWORD_CONFIRM_FIELD)
        conf_password_field.send_keys(conf_password)
        self.submit_click()

    def login_new_user(self, email=TestData.NEW_USER, password=TestData.PASSWORD_USER_NORMAL,
                       name=TestData.NEW_USER_NAME):
        self.login(email=email, password=password)
        self.should_be_logged_in(name=name)
        self.logout(name=name)

    def submit_click(self):
        self.browser.find_element(*BaseLocators.SUBMIT_BUTTON).click()

    def check_new_user_exist(self, user=TestData.NEW_USER):
        pgdb.del_new_user(user) if pgdb.check_user_exist(user) else None

    def should_be_err_reg_fields(self, email="", name="", pas="", conf_pass=""):
        self.should_be_err_mess(email, BaseLocators.ERR_EMAIL_FIELD) if email else None
        self.should_be_err_mess(name, BaseLocators.ERR_NAME_FIELD) if name else None
        self.should_be_err_mess(pas, BaseLocators.ERR_PAS_FIELD) if pas else None
        self.should_be_err_mess(conf_pass, BaseLocators.ERR_PAS_CONF_FIELD) if conf_pass else None

    def should_not_be_user_in_bd(self, user=TestData.NEW_USER):
        assert not pgdb.check_user_exist(user), f"Пользователь {user} есть в базe данных, что то пошло не так"

    def should_be_user_in_bd(self, user=TestData.NEW_USER):
        assert pgdb.check_user_exist(user), f"Пользователя {user} нет в базе данных, что то пошло не так"

    def should_be_success_reg_page(self, email=TestData.NEW_USER):
        self.should_be_title_page(text="thanks_for_reg")
        self.is_element_present(*RegistrationLocators.GO_TO_LOGIN_PAGE_FROM_REG)
        self.should_be_match_link(link=Links.REGISTRATION_SEND_MESS + "?email=" + email)

    def should_be_reg_confirm_page(self, email=TestData.NEW_USER):
        self.should_be_title_page(text="reg_confirm", locator=RegistrationLocators.REG_CONFIRM_TITLE)
        self.should_be_title_page(text="reg_confirm_text", locator=RegistrationLocators.REG_CONFIRM_TEXT)
        self.is_element_present(*RegistrationLocators.GO_TO_LOGIN_PAGE_FROM_REG)
        self.should_be_match_link(link="?email=" + email)

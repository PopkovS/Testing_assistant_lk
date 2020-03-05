from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pyperclip as pypc
import pages.pg_data_base as pgdb
import pages.requests_helper as req
from .base_page import BasePage
from .mailforforspam_page import MailForSpamPage, last_letter_id
from .locators import LoginLocators, Links, TestData


class LoginPage(BasePage):
    def login(self, email, password):
        self.fill_email(email)
        self.fill_password(password)
        self.click_submit()

    def set_password(self, email):
        self.fill_email(email)
        self.click_submit()

    def send_confirm_code(self):
        conf_pass_field = self.browser.find_element(*LoginLocators.CONF_CODE_FIELD)
        cod = pypc.paste()
        conf_pass_field.send_keys(cod)
        self.browser.find_element(*LoginLocators.SUBMIT_CONF_PASS).click()

    def set_password_confirm(self, password, password_conf):
        password_field = self.browser.find_element(*LoginLocators.PASSWORD)
        password_field.send_keys(password)
        password_field = self.browser.find_element(*LoginLocators.PASSWORD_CONFIRM)
        password_field.send_keys(password_conf)
        self.click_submit()

    def change_user_stat(self, stat=0, tfac="false"):
        """0-активен, 1 - Заблокирован, 2 - Не подтверждён, 3 - В архиве"""
        stat = int(stat)
        pgdb.change_stausid(stat)
        pgdb.change_twofactor(tfac)

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

    def go_to_set_password_conf_page(self, email=TestData.TEST_USER):
        old_lett = last_letter_id()
        current_link = self.browser.current_url
        if f"{Links.SET_PASSWORD_LINK}Confirm?email={email}" not in current_link:
            self.go_to_set_password_page()
            self.set_password(email)
            self.should_be_title_set_pass()
            self.new_tab()
            print(f"Старый счетчик писем {old_lett}")
            mail_page = MailForSpamPage(self.browser, self.browser.current_url)
            # new_lett = last_letter_id()
            # print(f"Новый счетчик писем {new_lett}")
            mail_page.check_mail(old_lett)#, new_lett)
            mail_page.go_to_password_conf()

    def get_conf_code(self):
        old_lett = last_letter_id()
        self.new_tab()
        mail_page = MailForSpamPage(self.browser, self.browser.current_url)
        # new_lett = last_letter_id()
        mail_page.check_mail(old_lett)
        mail_page.get_conf_code()
        mail_page.close_tab()
        mail_page.switch_to_tab(0)

    def click_submit(self, locator=LoginLocators.LOGIN_SUBMIT):
        submit = self.browser.find_element(*LoginLocators.LOGIN_SUBMIT)
        submit.click()

    def fill_password(self, password):
        password_field = self.browser.find_element(*LoginLocators.PASSWORD_USER_FIELD)
        password_field.send_keys(password)

    def fill_email(self, email):
        email_field = self.browser.find_element(*LoginLocators.EMAIL_FIELD)
        email_field.send_keys(email)

    def should_be_err_mess_password(self, var, locator=LoginLocators.ERR_MESS_PASSWORD):
        # expected_err_mess = self.text_err_field(var)
        self.should_be_err_mess(var, locator)

    def should_be_err_mess_email(self, var):  # , var, locator=LoginLocators.ERR_MESS_EMAIL):
        # expected_err_mess = va
        locator = LoginLocators.ERR_MESS_EMAIL
        self.should_be_err_mess(var, locator)

    def should_be_title_set_pass(self, timeout=5):
        title_ps = LoginLocators.SET_PASS_TITLE
        # wait = WebDriverWait(self.browser, timeout)
        text_expected = self.get_text_from_config("OtherText", "set_pass")
        err_text = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((title_ps))).text
        assert text_expected == err_text, f'Полученный заголовок страницы "{err_text}" отличается ' \
                                          f'от ожидаемого "{text_expected}" '

    def should_be_no_more_necessary_alert(self, n=1):
        number_of_alerts = len(self.browser.find_elements(*LoginLocators.ERR_ALERT))
        assert number_of_alerts == n, f"Количество алертов на экрване ({number_of_alerts}) не соответствует ожидаемому ({n})"

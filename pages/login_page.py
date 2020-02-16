from time import sleep

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pages.pg_data_base as pgdb
import pages.requests_helper as req
from .base_page import BasePage
from .locators import LoginLocators, Links


class LoginPage(BasePage):

    def login(self, email, password):
        self.fill_email(email)
        self.fill_password(password)
        self.click_submit()

    def set_password(self, email):
        self.fill_email(email)

        # self.click_submit()
        self.click_submit()

    def should_be_err_mess_password(self, expected_err_mess="Поле 'Пароль' является обязательным",
                                    locator=LoginLocators.ERR_MESS_PASSWORD):
        self.should_be_err_mess(expected_err_mess, locator)

    def should_be_err_mess_email(self, expected_err_mess="Поле 'Электронная почта\\Логин' является обязательным",
                                 locator=LoginLocators.ERR_MESS_EMAIL):
        self.should_be_err_mess(expected_err_mess, locator)

    def should_be_err_mess(self, expected_err_mess, locator):
        err_mess = locator
        wait = WebDriverWait(self.browser, 5)
        err_mess_text = wait.until(EC.visibility_of_element_located((err_mess))).text
        assert err_mess_text == expected_err_mess, f"Полученное сообщение \"{err_mess}\" не совподает с " \
                                                   f"ожидаемым \"{expected_err_mess}\" "

    def should_be_alert(self, alert_text_expected="Не все поля были заполнены правильно."):
        alert = LoginLocators.ERR_ALERT
        wait = WebDriverWait(self.browser, 5)
        alert_err_text = wait.until(EC.visibility_of_element_located((alert))).text
        assert alert_err_text == alert_text_expected, f"Полученное сообщение в алерте \"{alert_err_text}\" не " \
                                                      f"совподает с ожидаемым \"{alert_text_expected}\" "

    def should_be_no_more_necessary_alert(self, n=1):
        number_of_alerts = len(self.browser.find_elements(*LoginLocators.ERR_ALERT))
        assert number_of_alerts == n, f"Количество алертов на экрване ({number_of_alerts}) не соответствует ожидаемому ({n})"

    def change_user_status_id(self, stat):
        """0-активен, 1 - Заблокирован, 2 - Не подтверждён, 3 - В архиве"""
        stat = int(stat)
        pgdb.edit_stausid(stat)

    def create_test_user(self):
        if pgdb.check_user_exist() is False:
            req.send_pack("create_user")
            req.request_sending_edit_user(id_user=pgdb.get_id_user())
        else:
            req.send_pack("edit_user")

    def go_to_set_password_page(self):
        current_link = self.browser.current_url
        if current_link == Links.LOGIN_LINK:
            butt = self.browser.find_element(*LoginLocators.GO_TO_SET_PASS_BUTT)
            butt.click()

    def click_submit(self, locator=LoginLocators.LOGIN_SUBMIT):
        # wait = WebDriverWait(self.browser, 5)
        # submit = wait.until(EC.visibility_of_element_located(locator))
        submit = self.browser.find_element(*LoginLocators.LOGIN_SUBMIT)
        submit.click()

    def fill_password(self, password):
        password_field = self.browser.find_element(*LoginLocators.PASSWORD_FIELD)
        password_field.send_keys(password)

    def fill_email(self, email):
        email_field = self.browser.find_element(*LoginLocators.EMAIL_FIELD)
        email_field.send_keys(email)


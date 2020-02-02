from time import sleep

from .locators import LoginLocators
from .base_page import BasePage


class LoginPage(BasePage):
    def login(self, email, password):
        email_field = self.browser.find_element(*LoginLocators.EMAIL_FIELD)
        password_field = self.browser.find_element(*LoginLocators.PASSWORD_FIELD)
        email_field.send_keys(email)
        password_field.send_keys(password)
        submit = self.browser.find_element(*LoginLocators.LOGIN_SUBMIT)
        submit.click()

    def should_be_err_mess_email(self, expected_err_mess="Поле 'Электронная почта' является обязательным"):
        err_mess = self.browser.find_element(*LoginLocators.ERR_MESS_EMAIL).text
        assert err_mess == expected_err_mess, f"Полученное сообщение \"{err_mess}\" не совподает с " \
                                              f"ожидаемым \"{expected_err_mess}\" "

    def should_be_err_mess_password(self, expected_err_mess="Поле 'Пароль' является обязательным"):
        err_mess = self.browser.find_element(*LoginLocators.ERR_MESS_PASSWORD).text
        assert err_mess == expected_err_mess, f"Полученное сообщение \"{err_mess}\" не совподает с " \
                                              f"ожидаемым \"{expected_err_mess}\" "

    def should_be_alert(self, alert_text_expected="Не все поля были заполнены правильно."):
        sleep(0.1)
        alert_err_text = self.browser.find_element(*LoginLocators.ERR_ALERT).text
        assert alert_err_text == alert_text_expected, f"Полученное сообщение в алерте \"{alert_err_text}\" не " \
                                                      f"совподает с ожидаемым \"{alert_text_expected}\" "

    def should_be_no_more_necessary_alert(self, n=1):
        number_of_alerts = len(self.browser.find_elements(*LoginLocators.ERR_ALERT))
        assert number_of_alerts <= n, f"Количество алертов на экрване ({number_of_alerts}) превышает ожидаемое ({n})"

    # def should_be_login_url(self):
    #     assert "login" in self.browser.current_url, "This is not a registration page address"
    #
    # def should_be_login_form(self):
    #     assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), "Login form is not presented"
    #
    # def should_be_register_form(self):
    #     assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), "Register form is not presented"

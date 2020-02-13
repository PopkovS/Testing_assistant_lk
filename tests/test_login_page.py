from time import sleep

import pytest
from selenium.webdriver import DesiredCapabilities

from pages.locators import Links, TestData
from pages.login_page import LoginPage


class TestsLoginNegative():
    @pytest.fixture(scope="class", autouse=True)
    def setup_for_module(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.open()

    @pytest.fixture(scope="function", autouse=True)
    def setup_for_function(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        yield page
        page.should_be_no_more_necessary_alert()
        page.should_be_match_link(Links.LOGIN_LINK)
        browser.refresh()

    def test_login_with_empty_fields(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login('', '')
        page.should_be_err_mess_email()
        page.should_be_alert()

    def test_login_with_empty_email_field(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login('', TestData.FAKE_PASSWORD)
        page.should_be_err_mess_email()
        page.should_be_alert()

    def test_login_with_empty_password_field(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(TestData.VALID_EMAIL, '')
        page.should_be_err_mess_password()
        page.should_be_alert()

    def test_login_with_not_format_email(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(TestData.FAKE_PASSWORD, TestData.FAKE_PASSWORD)
        page.should_be_err_mess_email("Неверный формат E-mail")
        page.should_be_alert()

    def test_login_with_dangerous_content_in_email(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(f"<{TestData.VALID_EMAIL}>", TestData.VALID_PASSWORD)
        page.should_be_alert("В данных формы обнаружено опасное содержимое. Убедитесь, что не используете HTML-код при "
                             "заполнении формы")

    def test_login_with_incorrect_email(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(f"1111{TestData.VALID_EMAIL}", TestData.VALID_PASSWORD)
        page.should_be_alert("Неверно указан логин или пароль.")

    def test_login_with_incorrect_password(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(TestData.VALID_EMAIL, f"11{TestData.VALID_PASSWORD}")
        page.should_be_alert("Неверно указан логин или пароль")

    def test_login_with_blocked_user(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(TestData.BLOCKED_EMAIL, TestData.VALID_PASSWORD)
        page.should_be_alert("1Учетная запись заблокирована")

    def test_login_with_not_confirmed_user(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(TestData.NOT_CONFIRMED_EMAIL, TestData.VALID_PASSWORD)
        page.should_be_alert(
            "Учетная запись не подтверждена. На Вашу электронную почту отправлено письмо с инструкциями "
            "для ее подтверждения.")

    def test_login_with_archive_user(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.login(TestData.ARCHIVED_EMAIL, TestData.VALID_PASSWORD)
        page.should_be_alert("Учетная запись находится в архиве")

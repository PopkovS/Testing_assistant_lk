from time import sleep

import pytest
from selenium.webdriver import DesiredCapabilities

from pages.locators import Links, TestData
from pages.login_page import LoginPage


@pytest.fixture(scope="module", autouse=True)
def setup_for_module(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    page.open()


@pytest.fixture(scope="function", autouse=True)
def setup_for_function(browser):
    yield
    browser.refresh()


def test_login_with_empty_fields(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    page.login('', '')
    page.should_be_err_mess_email()
    page.should_be_alert()
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_empty_email_field(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login('', TestData.FAKE_PASSWORD)
    page.should_be_err_mess_email()
    page.should_be_alert()
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_empty_password_field(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(TestData.VALID_EMAIL, '')
    page.should_be_err_mess_password()
    page.should_be_alert()
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_not_fomat_email(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(TestData.FAKE_PASSWORD, TestData.FAKE_PASSWORD)
    page.should_be_err_mess_email("Неверный формат E-mail")
    page.should_be_alert()
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_dangerous_content_in_email(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(f"<{TestData.VALID_EMAIL}>", TestData.VALID_PASSWORD)
    page.should_be_alert("В данных формы обнаружено опасное содержимое. Убедитесь, что не используете HTML-код при "
                         "заполнении формы")
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_incorrect_email(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(f"1111{TestData.VALID_EMAIL}", TestData.VALID_PASSWORD)
    page.should_be_alert("Неверно указан логин или пароль.")
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_incorrect_password(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(TestData.VALID_EMAIL, f"11{TestData.VALID_PASSWORD}")
    page.should_be_alert("Неверно указан логин или пароль.")
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_blocked_user(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(TestData.BLOCKED_EMAIL, TestData.VALID_PASSWORD)
    page.should_be_alert("Учетная запись заблокирована")
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_not_confirmed_user(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(TestData.NOT_CONFIRMED_EMAIL, TestData.VALID_PASSWORD)
    page.should_be_alert("Учетная запись не подтверждена. На Вашу электронную почту отправлено письмо с инструкциями "
                         "для ее подтверждения.")
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)


def test_login_with_archive_user(browser):
    page = LoginPage(browser, Links.LOGIN_LINK)
    # page.open()
    page.login(TestData.ARCHIVED_EMAIL, TestData.VALID_PASSWORD)
    page.should_be_alert("Учетная запись находится в архиве")
    page.should_be_no_more_necessary_alert()
    page.should_be_match_link(Links.LOGIN_LINK)

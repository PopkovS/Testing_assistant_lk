from time import sleep

import pytest

from pages.locators import Links, TestData
from pages.login_page import LoginPage


@pytest.fixture(scope="module", autouse=True)
def setup_for_module(browser):
    global page
    page = LoginPage(browser, Links.LOGIN_LINK)
    page.open()
    page.change_user_status_id(0)
    yield page
    page.change_user_status_id(0)


class TestsLoginNegative():
    @pytest.fixture(scope="function", autouse=True)
    def setup_for_login_neg_function(self, browser):
        yield page
        page.should_be_no_more_necessary_alert()
        page.should_be_match_link(Links.LOGIN_LINK)
        browser.refresh()

    def test_login_with_empty_fields(self, browser):
        page.login('', '')
        page.should_be_err_mess_email()
        page.should_be_alert()

    def test_login_with_empty_email_field(self, browser):
        page.login('', TestData.FAKE_PASSWORD)
        page.should_be_err_mess_email()
        page.should_be_alert()

    def test_login_with_empty_password_field(self, browser):
        page.login(TestData.VALID_EMAIL, '')
        page.should_be_err_mess_password()
        page.should_be_alert()

    def test_login_with_not_format_email(self, browser):
        page.login(TestData.TEST_USER.replace("@", ""), TestData.FAKE_PASSWORD)
        page.should_be_alert("Неверно указан логин или пароль")

    def test_login_with_dangerous_content_in_email(self, browser):
        page.login(f"<{TestData.TEST_USER}>", TestData.VALID_PASSWORD)
        page.should_be_alert("В данных формы обнаружено опасное содержимое. Убедитесь, что не используете HTML-код при "
                             "заполнении формы")

    def test_login_with_incorrect_email(self, browser):
        page.login(f"1111{TestData.TEST_USER}", TestData.VALID_PASSWORD)
        page.should_be_alert("Неудачная попытка аутентификации. Ошибка Active Directory: Connect Error. Время "
                             "ожидания операции истекло")

    def test_login_with_incorrect_password(self, browser):
        page.login(TestData.TEST_USER, f"11{TestData.VALID_PASSWORD}")
        page.should_be_alert("Неверно указан логин или пароль")

    def test_login_with_blocked_user(self, browser):
        page.change_user_status_id(1)
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.should_be_alert("Учетная запись заблокирована")

    def test_login_with_not_confirmed_user(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.change_user_status_id(2)
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.should_be_alert(
            "Учетная запись не подтверждена. На Вашу электронную почту отправлено письмо с инструкциями для ее "
            "подтверждения")

    def test_login_with_archive_user(self, browser):
        page.change_user_status_id(3)
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.should_be_alert("Учетная запись находится в архиве")
        page.change_user_status_id(0)


class TestsSetPasswordNegative():
    @pytest.fixture(scope="class", autouse=True)
    def setup_for_set_pass_neg_class(self, browser):
        page.go_to_set_password_page()
        yield

    @pytest.fixture(scope="function", autouse=True)
    def setup_for_set_pass_neg_function(self, browser):
        page.change_user_status_id(0)
        yield page
        page.should_be_no_more_necessary_alert()
        browser.refresh()

    def test_setpassword_with_empty_email(self, browser):
        page.set_password("")
        page.should_be_err_mess_email("Поле 'Электронная почта' является обязательным.")
        page.should_be_alert()

    def test_setpassword_not_format_email(self, browser):
        page.set_password(TestData.TEST_USER.replace("@", ""))
        page.click_submit()
        page.should_be_err_mess_email("Неверный формат E-mail")
        page.should_be_alert()

    def test_setpassword_with_dangerous_content_in_email(self, browser):
        page.set_password(f"<{TestData.TEST_USER}>")
        page.click_submit()
        page.should_be_err_mess_email("Неверный формат E-mail")
        page.should_be_alert("В данных формы обнаружено опасное содержимое. Убедитесь, что не используете HTML-код при "
                             "заполнении формы")

    def test_setpassword_with_incorrect_email(self, browser):
        page.set_password(f"1111{TestData.TEST_USER}")
        page.should_be_alert("Учетная запись с указанным адресом электронной почты не найдена")

    def test_setpassword_with_blocked_user(self, browser):
        page.change_user_status_id(1)
        page.set_password(TestData.TEST_USER)
        page.should_be_alert("Учетная запись с указанным адресом электронной почты не активна")

    def test_setpassword_not_confirmed_user(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.change_user_status_id(2)
        page.set_password(TestData.TEST_USER)
        page.should_be_alert("Учетная запись с указанным адресом электронной почты не активна")

    def test_setpassword_with_archive_user(self, browser):
        page.change_user_status_id(3)
        page.set_password(TestData.TEST_USER)
        page.should_be_alert("Учетная запись с указанным адресом электронной почты не активна")



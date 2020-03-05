from time import sleep

import pytest

from pages.locators import Links, TestData
from pages.login_page import LoginPage, LoginLocators
from pages.mailforforspam_page import MailForSpamPage


@pytest.fixture(scope="module", autouse=True)
def setup_for_module(browser):
    global page
    page = LoginPage(browser, Links.LOGIN_LINK)
    page.change_user_stat(0)
    page.open()
    yield page
    page.change_user_stat(0)


class TestsLoginNegative():
    @pytest.fixture(scope="function", autouse=True)
    def setup_for_login_neg_function(self, browser):
        page.change_user_stat(0)
        browser.refresh()
        yield page
        page.should_be_no_more_necessary_alert()
        page.should_be_match_link(Links.LOGIN_LINK)

    def test_login_with_empty_fields(self, browser):
        page.login('', '')
        page.should_be_err_mess_email("email_or_log_empty")
        page.should_be_alert("not_valid_pass_or_log")

    def test_login_with_empty_email_field(self, browser):
        page.login('', TestData.FAKE_PASSWORD)
        page.should_be_err_mess_email("email_or_log_empty")
        page.should_be_alert("not_valid_pass_or_log")

    def test_login_with_empty_password_field(self, browser):
        page.login(TestData.VALID_EMAIL, '')
        page.should_be_err_mess_password("pass_empty")
        page.should_be_alert("not_valid_pass_or_log")

    def test_login_with_not_format_email(self, browser):
        page.login(TestData.TEST_USER.replace("@", ""), TestData.FAKE_PASSWORD)
        page.should_be_alert("err_pass_or_log")

    def test_login_with_dangerous_content_in_email(self, browser):
        page.login(f"<{TestData.TEST_USER}>", TestData.VALID_PASSWORD)
        page.should_be_alert("dang_cont")

    def test_login_with_incorrect_email(self, browser):
        page.login(f"1111{TestData.TEST_USER}", TestData.VALID_PASSWORD)
        page.should_be_alert("err_ad", expec=10)

    def test_login_with_incorrect_password(self, browser):
        page.login(TestData.TEST_USER, f"11{TestData.VALID_PASSWORD}")
        page.should_be_alert("err_pass_or_log", expec=10)

    def test_login_with_blocked_user(self, browser):
        page.change_user_stat(1)
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.should_be_alert("acc_blocked", expec=10)

    def test_login_with_not_confirmed_user(self, browser):
        page.change_user_stat(2)
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.should_be_alert("acc_not_conf", expec=12)

    def test_login_with_archive_user(self, browser):
        page.change_user_stat(3)
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.should_be_alert("acc_archive", expec=10)
        page.change_user_stat(0)


class TestsSetPasswordNegative():
    @pytest.fixture(scope="class", autouse=True)
    def setup_for_set_pass_neg_class(self, browser):
        page.go_to_set_password_page()
        yield
        page.go_to_page()
        sleep(5)

    @pytest.fixture(scope="function", autouse=True)
    def setup_for_set_pass_neg_function(self, browser):
        page.change_user_stat(0)
        browser.refresh()
        yield page
        page.should_be_no_more_necessary_alert()

    def test_setpassword_with_empty_email(self, browser):
        page.set_password("")
        page.should_be_err_mess_email("email_empty")
        page.should_be_alert("not_valid_pass_or_log")

    def test_setpassword_not_format_email(self, browser):
        page.set_password(TestData.TEST_USER.replace("@", ""))
        page.click_submit()
        page.should_be_err_mess_email("not_valid_email")
        page.should_be_alert("not_valid_pass_or_log")

    def test_setpassword_with_dangerous_content_in_email(self, browser):
        page.set_password(f"<{TestData.TEST_USER}>")
        page.click_submit()
        page.should_be_err_mess_email("not_valid_email")
        page.should_be_alert("dang_cont")

    def test_setpassword_with_incorrect_email(self, browser):
        page.set_password(f"1111{TestData.TEST_USER}")
        page.should_be_alert("acc_not_found")

    def test_setpassword_with_blocked_user(self, browser):
        page.change_user_stat(1)
        page.set_password(TestData.TEST_USER)
        page.should_be_alert("acc_not_active")

    def test_setpassword_not_confirmed_user(self, browser):
        page = LoginPage(browser, Links.LOGIN_LINK)
        page.change_user_stat(2)
        page.set_password(TestData.TEST_USER)
        page.should_be_alert("acc_not_active")

    def test_setpassword_with_archive_user(self, browser):
        page.change_user_stat(3)
        page.set_password(TestData.TEST_USER)
        page.should_be_alert("acc_not_active")


class TestsSetPasswordConfirmNegative():
    @pytest.fixture(scope="class", autouse=True)
    def setup_for_set_pass_confirm_neg_class(self, browser):
        browser.refresh()
        page.change_user_stat(0)
        page.go_to_set_password_conf_page()
        yield page
        page.close_tab()
        page.switch_to_tab(0)
        page.go_to_page()
        sleep(3)

    @pytest.fixture(scope="function", autouse=True)
    def setup_for_set_pass_neg_function(self, browser):
        yield page
        browser.refresh()

    def test_setpassword_conf_with_empty_fields(self, browser):
        page.set_password_confirm("", "")
        page.should_be_err_mess("pass_empty",
                                LoginLocators.ERR_MESS_CHANGE_PASS)
        page.should_be_err_mess("conf_pass_empty",
                                LoginLocators.ERR_MESS_CHANGE_CONF_PASS)
        page.should_be_alert("not_valid_pass_or_log")

    def test_setpassword_conf_with_empty_password(self, browser):
        page.set_password_confirm("", TestData.VALID_PASSWORD)
        page.click_submit()
        page.should_be_err_mess("pass_empty_misha",
                                LoginLocators.ERR_MESS_CHANGE_PASS)
        page.should_be_err_mess("pass_and_cof_pass_diff",
                                LoginLocators.ERR_MESS_CHANGE_CONF_PASS)
        page.should_be_alert("err_to_admin")

    def test_setpassword_conf_with_empty_conf_password(self, browser):
        page.set_password_confirm(TestData.VALID_PASSWORD, "")
        page.should_be_err_mess("conf_pass_empty",
                                LoginLocators.ERR_MESS_CHANGE_CONF_PASS)
        page.should_be_alert("err_to_admin")

    def test_setpassword_conf_with_diff_passwords(self, browser):
        page.set_password_confirm("123", "1234")
        page.click_submit()
        page.should_be_err_mess("pass_and_cof_pass_diff",
                                LoginLocators.ERR_MESS_CHANGE_CONF_PASS)
        page.should_be_alert("err_to_admin")


class TestsLoginPositive():
    @pytest.fixture(scope="class", autouse=True)
    def setup_for_set_pass_confirm_neg_class(self, browser):
        page.change_user_stat(0, tfac="false")
        yield page

    @pytest.fixture(scope="function", autouse=True)
    def setup_for_set_pass_neg_function(self, browser):
        page.go_to_page()
        yield page
        page.logout()
        browser.refresh()

    def test_login(self, browser):
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.should_be_logged_in()

    def test_login_with_twofactor(self, browser):
        page.change_user_stat(0, tfac="true")
        page.login(TestData.TEST_USER, TestData.VALID_PASSWORD)
        page.get_conf_code()
        page.send_confirm_code()
        page.should_be_logged_in()
        page.change_user_stat(0, tfac="false")

from time import sleep

import pytest

from pages.locators import Links, TestData, BaseLocators
from pages.registration_page import RegistrationPage
from pages.mailforforspam_page import MailForSpamPage


@pytest.fixture(scope="module", autouse=True)
def setup_for_module(browser):
    global page
    page = RegistrationPage(browser, Links.LOGIN_LINK)
    page.check_new_user_exist()
    page.change_sys_paran(auth_ad="False")
    page.open()
    page.go_to_reg_page()
    yield page


class TestsRegNegative():
    @pytest.fixture(scope="function", autouse=True)
    def setup_for_login_neg_function(self, browser):
        browser.refresh()
        yield page
        page.should_be_no_more_necessary_alert()
        page.should_not_be_user_in_bd()

    def test_reg_with_empty_fields(self, browser):
        page.registration("", "", "", "")
        page.should_be_err_reg_fields(email="email_empty",
                                      name="name_empty",
                                      pas="pass_empty",
                                      conf_pass="conf_pass_empty_what")
        page.should_be_alert("not_valid_pass_or_log")

    def test_reg_with_empty_email(self, browser):
        page.registration("",
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_err_reg_fields(email="email_empty")
        page.should_be_alert("not_valid_pass_or_log")

    def test_reg_with_empty_name(self, browser):
        page.registration(email=TestData.NEW_USER,
                          name="",
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_err_reg_fields(name="name_empty")
        page.should_be_alert("not_valid_pass_or_log")

    def test_reg_with_empty_pass_and_conf_pass(self, browser):
        page.registration(email=TestData.NEW_USER,
                          name=TestData.NEW_USER_NAME,
                          password="",
                          conf_password="")
        page.should_be_err_reg_fields(pas="pass_empty",
                                      conf_pass="conf_pass_empty_what")
        page.should_be_alert("not_valid_pass_or_log")

    def test_reg_with_empty_pass(self, browser):
        page.registration(email=TestData.NEW_USER,
                          name=TestData.NEW_USER_NAME,
                          password="",
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.submit_click()
        page.should_be_err_reg_fields(pas="pass_empty")
        page.should_be_alert("err_to_admin")

    def test_reg_with_empty_conf_pass(self, browser):
        page.registration(email=TestData.NEW_USER,
                          name=TestData.NEW_USER_NAME,
                          password="",
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.submit_click()
        page.should_be_err_reg_fields(pas="pass_empty", conf_pass="pass_and_cof_pass_diff")
        page.should_be_alert("err_to_admin")

    def test_reg_with_diff_passwords(self, browser):
        page.registration(email=TestData.NEW_USER,
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_AD)
        page.submit_click()
        page.should_be_err_reg_fields(conf_pass="pass_and_cof_pass_diff")
        page.should_be_alert("err_to_admin")

    def test_reg_with_not_format_email(self, browser):
        page.registration(email=TestData.NEW_USER.replace("@", ""),
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_err_reg_fields(email="not_valid_email")
        page.should_be_alert("not_valid_pass_or_log")

    def test_reg_with_taken_email(self, browser):
        page.registration(email=TestData.TEST_USER_NORMAL,
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_alert("email_is_taken", text=TestData.TEST_USER_NORMAL)

    def test_reg_with_dangerous_content_in_email(self, browser):
        page.registration(email=f"<{TestData.NEW_USER}>",
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_err_reg_fields(email="not_valid_email")
        page.should_be_alert("dang_cont")

    def test_reg_with_dangerous_content_in_name(self, browser):
        page.registration(email=TestData.NEW_USER,
                          name=f"<{TestData.NEW_USER_NAME}>",
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_alert("dang_cont")


class TestsNegativeAfterReg():
    @pytest.fixture(scope="function", autouse=True)
    def setup_for_login_neg_function(self, browser):
        browser.refresh()
        page.go_to_reg_page()
        yield page
        page.check_new_user_exist()

    def test_reg_link_from_letters(self):
        page.registration(email=TestData.NEW_USER,
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_success_reg_page()
        page.go_to_login_page_from_confirm_reg()
        page.login(email=TestData.NEW_USER,
                   password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_alert("acc_not_conf")
        page.should_be_user_in_bd()


class TestsRegPositive():
    @pytest.fixture(scope="function", autouse=True)
    def setup_for_login_neg_function(self, browser):
        browser.refresh()
        global mail_num
        mail_num = page.old_letters_count()
        page.go_to_reg_page()
        yield page
        page.should_be_user_in_bd()
        page.check_new_user_exist()

    def test_reg_link_from_letters(self):
        page.registration(email=TestData.NEW_USER,
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_success_reg_page()
        page.go_to_account_activation(old_lett=mail_num)
        page.should_be_reg_confirm_page()
        page.go_to_login_page_from_confirm_reg()
        page.login_new_user()
        page.close_tab()

    def test_reg_link_from_reg_page(self):
        page.registration(email=TestData.NEW_USER,
                          name=TestData.NEW_USER_NAME,
                          password=TestData.PASSWORD_USER_NORMAL,
                          conf_password=TestData.PASSWORD_USER_NORMAL)
        page.should_be_success_reg_page()
        page.go_to_account_activation(old_lett=mail_num)
        page.should_be_reg_confirm_page()
        page.close_tab()
        page.go_to_login_page_from_confirm_reg()
        page.login_new_user()

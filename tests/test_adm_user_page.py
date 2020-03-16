from time import sleep

import pytest

from pages.locators import Links, TestData
from pages.adm_user_page import AdmUserPage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.mailforforspam_page import MailForSpamPage


@pytest.fixture(scope="module", autouse=True)
def setup_for_module(browser):
    global page
    global reg_page
    reg_page = RegistrationPage(browser, Links.LOGIN_LINK)
    page = AdmUserPage(browser, Links.LOGIN_LINK)
    page.open()
    page.change_user_stat()
    yield page


class TestImportFromAdPositive():
    @pytest.fixture(scope="function", autouse=True)
    def setup_for_import_from_ad_positive(self, browser):
        page.check_new_user_exist()
        page.go_to_adm_user()
        yield page
        page.browser.save_screenshot("screenshot" + __name__ + ".png")
        page.save_screen()

    def test_import_user_from_ad_login(self, browser, us_name=TestData.NEW_USER_NAME):
        page.go_to_ad_import_user(us_name)
        page.set_add_user_from_ad(email=TestData.NEW_USER_EMAIL)
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        page.logout()
        reg_page.login_new_user(email=us_name,
                                name=us_name,
                                password=TestData.PASSWORD_USER_AD)
        reg_page.should_be_user_in_bd()

    def test_import_user_from_and_login_twofac(self, browser, us_name=TestData.NEW_USER_NAME):
        page.go_to_ad_import_user(us_name)
        page.set_add_user_from_ad(email=TestData.NEW_USER_EMAIL, name=us_name + "test")
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        page.logout()
        log_page = LoginPage(browser, Links.LOGIN_LINK)
        log_page.login_twofac(email=TestData.NEW_USER_EMAIL, name=us_name,
                              password=TestData.PASSWORD_USER_AD, link=Links.MAIL_FOR_SPAM_NEW_US)
        page.logout(name=us_name + "test")
        reg_page.should_be_user_in_bd()

    def test_import_user_from_and_with_email_login(self, us_name=TestData.NEW_USER_NAME2):
        page.check_new_user_exist(user=TestData.NEW_USER_EMAIL2.lower())
        page.go_to_ad_import_user(us_name)
        page.set_add_user_from_ad(name=us_name + "test")
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        page.logout()
        reg_page.login_new_user(email=us_name,
                                name=us_name + "test",
                                password=TestData.PASSWORD_USER_AD)
        reg_page.should_be_user_in_bd(TestData.NEW_USER_EMAIL2.lower())
        page.check_new_user_exist(user=TestData.NEW_USER_EMAIL2.lower())

    def test_import_two_user_from_and_with(self, us_name=TestData.NEW_USER_NAME2, us_email=TestData.NEW_USER_EMAIL2,
                                           two_us_email=TestData.NEW_USER_NAME + "@" + TestData.AD_SERVE,
                                           two_us_name=TestData.NEW_USER_NAME):
        page.check_new_user_exist(user=us_email.lower())
        page.check_new_user_exist(user=two_us_email)
        page.go_to_ad_import_user(user=us_name, two_user=two_us_name)
        page.set_add_user_from_ad()
        page.should_be_alert(var="success_imports_ad", text="2")
        page.close_alert()
        page.logout()
        reg_page.login_new_user(email=two_us_name,
                                name=two_us_name,
                                password=TestData.PASSWORD_USER_AD)
        reg_page.should_be_user_in_bd(us_email.lower())
        reg_page.should_be_user_in_bd(two_us_email)
        page.check_new_user_exist(us_email.lower())
        page.check_new_user_exist(two_us_email)




class TestAccountBindingFromAdPositive():
    @pytest.fixture(scope="function", autouse=True)
    def setup_for_account_binding(self, browser):
        page.check_new_user_exist(user=TestData.NEW_USER_EMAIL2.lower())
        reg_page.full_registration(email=TestData.NEW_USER_EMAIL2.lower(),
                                   name=TestData.NEW_USER_NAME2,
                                   password=TestData.PASSWORD_USER_NORMAL,
                                   link=Links.MAIL_FOR_SPAM_NEW_US2)
        page.go_to_adm_user()
        page.go_to_ad_import_user(TestData.NEW_USER_NAME2)
        yield page

    def test_account_binding_and_login(self, us_name=TestData.NEW_USER_NAME2,
                                       email=TestData.NEW_USER_EMAIL2):
        page.set_add_user_from_ad(name=TestData.NEW_USER_NAME2 + "test", join_email="True")
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        page.logout()
        reg_page.login_new_user(email=us_name,
                                name=us_name + "test",
                                password=TestData.PASSWORD_USER_AD)
        reg_page.should_be_user_in_bd(email.lower())
        page.check_new_user_exist(user=email.lower())

    def test_account_binding_and_login_twofac(self, browser, us_name=TestData.NEW_USER_NAME2,
                                              email=TestData.NEW_USER_EMAIL2):
        page.set_add_user_from_ad(name=us_name + "test", join_email="True")
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        page.logout()
        log_page = LoginPage(browser, Links.LOGIN_LINK)
        log_page.login_twofac(email=email.lower(), name=us_name,
                              password=TestData.PASSWORD_USER_AD, link=Links.MAIL_FOR_SPAM_NEW_US2)
        page.logout(name=us_name + "test")
        reg_page.should_be_user_in_bd(email.lower())
        page.check_new_user_exist(user=email.lower())

    def test_account_binding_blocked_user(self, us_name=TestData.NEW_USER_NAME2):
        page.change_user_stat(email=TestData.NEW_USER_EMAIL2.lower(), stat=1)
        page.set_add_user_from_ad(name=us_name + "test", join_email="True", up_not_active="True")
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        page.logout()
        page.login(email=us_name, password=TestData.PASSWORD_USER_AD)
        page.should_be_alert("acc_blocked")
        page.browser.refresh()

    def test_account_binding_not_confirmed_user(self, us_name=TestData.NEW_USER_NAME2,
                                                email=TestData.NEW_USER_EMAIL2):
        page.change_user_stat(email=TestData.NEW_USER_EMAIL2.lower(), stat=2)
        page.set_add_user_from_ad(name=us_name + "test", join_email="True", up_not_active="True")
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        mail_num = reg_page.old_letters_count()
        page.logout()
        page.change_sys_paran(auth_ad="True", dir_control="False")
        page.login(email=us_name,
                   password=TestData.PASSWORD_USER_AD)
        page.should_be_alert("acc_not_conf")
        page.browser.refresh()
        reg_page.go_to_account_activation(link=Links.MAIL_FOR_SPAM_NEW_US2,
                                          old_lett=mail_num)
        reg_page.should_be_reg_confirm_page(email=email.lower())
        page.close_tab()
        reg_page.login_new_user(email=us_name,
                                name=us_name + "test",
                                password=TestData.PASSWORD_USER_AD)
        reg_page.should_be_user_in_bd(email.lower())
        page.check_new_user_exist(user=email.lower())

    def test_account_binding_archived_user(self, us_name=TestData.NEW_USER_NAME2):
        page.change_user_stat(email=TestData.NEW_USER_EMAIL2.lower(), stat=3)
        page.set_add_user_from_ad(name=us_name + "test", join_email="True", up_not_active="True")
        page.should_be_alert(var="success_import_ad", text="1")
        page.close_alert()
        page.logout()
        page.login(email=us_name, password=TestData.PASSWORD_USER_AD)
        page.should_be_alert("acc_archive")
        page.browser.refresh()

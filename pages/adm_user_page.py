from time import sleep

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pages.pg_data_base as pgdb
from pages.login_page import LoginPage
from .base_page import BasePage
from .locators import LoginLocators, Links, TestData, BaseLocators, RegistrationLocators, Menu, AdmUserLocators
from selenium.webdriver.support import expected_conditions as EC


class AdmUserPage(BasePage):
    def open_user_page(self):
        self.should_be_logged_in()
        adm_button = self.browser.find_element(*Menu.MENU_FIRST_LEVEL_ADM)
        adm_button.click()
        user_button = self.browser.find_element(*Menu.MENU_SECOND_LEVEL_ADM_USR)
        user_button.click()

    def go_to_ad_form(self, element=AdmUserLocators.IMPORT_FROM_AD_BUTT):
        imp_from_ad = self.browser.find_element(*element)
        '''Здесь упадет если окно браузера будет недостаточно широким, можно пофиксить, 
        а можно просто запускать при 1600 900'''
        imp_from_ad.click()
        imp_from_ad.click() if not self.is_element_present(*AdmUserLocators.CONNECTION_WITH_AD) else None

    def import_click(self):
        import_button = self.browser.find_element(*AdmUserLocators.IMPORT_BUTT)
        import_button.click()

    def set_add_user_from_ad(self, name="", email="", up_atr="", join_email='', up_not_active=''):
        if name:
            name_field = self.browser.find_element(*BaseLocators.NAME_FIELD)
            name_field.clear()
            name_field.send_keys(name)
        if email:
            email_field = self.browser.find_element(*BaseLocators.EMAIL_FIELD)
            email_field.clear()
            email_field.send_keys(email)
        self.browser.find_element(*AdmUserLocators.UPDATE_ATR_CHBOX).click() if up_atr else None
        self.browser.find_element(*AdmUserLocators.JOIN_EMAIL_CHBOX).click() if join_email else None
        self.browser.find_element(*AdmUserLocators.UPDATE_NOT_ACT_CHBOX).click() if up_not_active else None

        submit = self.browser.find_element(*BaseLocators.SUBMIT_UNIVERSAL_BUTT)
        submit.click()

    def connect_with_ad(self, serv=TestData.AD_SERVE, name=TestData.AD_NAME,
                        password=TestData.AD_PASSWORD):
        serv_field = self.browser.find_element(*AdmUserLocators.AD_SERVER_FIELD)
        serv_field.send_keys(serv)
        name_field = self.browser.find_element(*AdmUserLocators.AD_NAME_FIELD)
        name_field.send_keys(name)
        pass_field = self.browser.find_element(*AdmUserLocators.AD_PASSWORD_FIELD)
        pass_field.send_keys(password)
        submit_ad = self.browser.find_element(*BaseLocators.SUBMIT_UNIVERSAL_BUTT)
        submit_ad.click()
        title_ad_page = self.is_element_present(*AdmUserLocators.TITLE_IMPORT_AD_PAGE, timeout=10)
        assert title_ad_page, "Неудалось получить заголовок 'Импорт учетных записей из Active Directory'" \
                              "со станицы импота из AD"

    def login_twocfacktor_new_user_ad(self, browser="", email=TestData.NEW_USER_EMAIL, name=TestData.NEW_USER_NAME,
                                      password=TestData.PASSWORD_USER_AD):
        login_page = LoginPage(browser, Links.LOGIN_LINK)
        login_page.login_twofac(email=email, name=name,
                                password=password, link=Links.MAIL_FOR_SPAM_NEW_US)

    def go_to_adm_user(self):
        current_link = self.browser.current_url
        self.change_sys_paran(auth_ad="False")
        if Links.LOGIN_LINK in current_link:
            self.login(email=TestData.USER_NORMAL_EMAIL, password=TestData.PASSWORD_USER_NORMAL)
        self.change_sys_paran(dir_control="True")
        self.open_user_page()

    def go_to_ad_import_user(self, user, two_user=''):
        self.go_to_ad_form()
        self.connect_with_ad()
        self.search_and_choose(user)
        self.search_and_choose(two_user) if two_user else None
        self.import_click()

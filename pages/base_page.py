import configparser
import math
import os
import socket
import sys
import traceback
import pages.pg_data_base as pgdb
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.locators import Links, TestData, LoginLocators, BaseLocators

main_link = "http://lk.corp.ast.safib.ru/"


class BasePage():
    def __init__(self, browser, url, timeout=3):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((how, what)))
            # self.browser.find_element(how, what)
        except TimeoutException:
            # except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False

        return True

    def go_to_page(self):
        # current_link = self.browser.current_url
        # if f"{self.url}" not in current_link:
        self.open()

    def change_user_stat(self, stat=0, tfac="false", user=TestData.TEST_USER_NORMAL):
        """0-активен, 1 - Заблокирован, 2 - Не подтверждён, 3 - В архиве"""
        stat = int(stat)
        pgdb.change_stausid(stat, user)
        pgdb.change_twofactor(tfac,user)

    def change_sys_paran(self, auth_ad="True", dir_control="False"):
        pgdb.change_auth_ad(auth_ad)
        pgdb.change_direct_control(dir_control)

    def save_screen(self):
        name_scr = traceback.extract_stack(None, 2)[0][2]
        print(name_scr)
        self.browser.save_screenshot(f".\\screenshots\\{name_scr}.png")

    def new_tab(self, link=Links.MAIL_FOR_SPAM_NORM_US, i=1):
        self.browser.execute_script(f'window.open("{link}","_blank");')
        self.switch_to_tab(i)

    def switch_to_tab(self, i=1):
        new_window = self.browser.window_handles[i]
        self.browser.switch_to.window(new_window)

    def close_tab(self, i=1):
        # new_window = self.browser.window_handles[i]
        self.browser.close()
        self.switch_to_tab(0)

    def get_text_from_config(self, section, var, file="test_data_message.ini"):
        path = os.path.join(sys.path[1], file)
        config = configparser.ConfigParser()
        config.read(path, 'utf-8')
        text = config[section][var]
        return text

    def text_alert(self, var):
        text = self.get_text_from_config("ErrAlert", var)
        return text

    def text_err_field(self, var):
        text = self.get_text_from_config("ErrFieldMess", var)
        return text

    def login(self, email=TestData.TEST_USER_NORMAL, password=TestData.PASSWORD_USER_NORMAL):
        email_field = self.browser.find_element(*LoginLocators.EMAIL_FIELD)
        email_field.send_keys(email)
        password_field = self.browser.find_element(*LoginLocators.PASSWORD_USER_FIELD)
        password_field.send_keys(password)
        submit = self.browser.find_element(*BaseLocators.SUBMIT_BUTTON)
        submit.click()

    def logout(self, name=TestData.TEST_USER_NAME):
        self.should_be_logged_in(name)
        avatar_user = self.browser.find_element(*BaseLocators.USER_MENU)
        avatar_user.click()
        exit_but = self.browser.find_element(*BaseLocators.LOGOUT_BUT)
        exit_but.click()

    def should_be_logged_in(self, name=TestData.TEST_USER_NAME):
        assert self.is_element_present(*BaseLocators.USER_MENU,
                                       timeout=10), "Не удалось найти ссылку c именем пользователя на " \
                                                    "странице "
        text_user_name = self.browser.find_element(*BaseLocators.USER_MENU).text
        assert text_user_name == name, f"Фактическое имя пользователя {text_user_name} не " \
                                                          f"совпадает с ожидаемым {name} "

    def should_be_alert(self, var, expec=5, text=""):
        alert = LoginLocators.ERR_ALERT
        wait = WebDriverWait(self.browser, expec)
        alert_text_expected = self.text_alert(var)
        alert_err_text = wait.until(EC.visibility_of_element_located((alert))).text
        assert alert_text_expected.replace("@&&@", text) == alert_err_text, f"Полученное сообщение в алёрте \"{alert_err_text}\" не совподает с " \
                                                      f"ожидаемым \"{alert_text_expected}\" "

    def should_be_err_mess(self, var, locator):
        err_mess = locator
        expected_err_mess = self.text_err_field(var)
        wait = WebDriverWait(self.browser, 5)
        err_mess_text = wait.until(EC.visibility_of_element_located((err_mess))).text
        assert err_mess_text == expected_err_mess, f"Полученное сообщение \"{err_mess_text}\" не совподает с " \
                                                   f"ожидаемым \"{expected_err_mess}\" "

    def should_be_match_link(self, link):
        current_link = self.browser.current_url
        assert link in current_link, f"Текщий адрес \"{current_link}\" не содержит ожидаемого фрагмента \"{link}\""

    def should_be_title_page(self, timeout=5, file_name="OtherText", text="set_pass",
                             locator=LoginLocators.SET_PASS_TITLE):
        title_ps = locator
        text_expected = self.get_text_from_config(file_name, text)
        err_text = WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((title_ps))).text
        assert text_expected == err_text, f'Полученный заголовок страницы "{err_text}" отличается ' \
                                          f'от ожидаемого "{text_expected}" '

    def should_be_no_more_necessary_alert(self, n=1):
        number_of_alerts = len(self.browser.find_elements(*LoginLocators.ERR_ALERT))
        assert number_of_alerts == n, f"Количество алертов на экрване ({number_of_alerts}) не соответствует ожидаемому ({n})"
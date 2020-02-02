import math

from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

main_link = "http://lk.pub.ast.safib.ru/"

class BasePage():
    def __init__(self, browser, url, timeout=3):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
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

    def should_be_match_link (self, link):
        current_link = self.browser.current_url
        assert link in current_link, f"Текщий адрес \"{current_link}\" не содержит ожидаемого фрагмента \"{link}\""


    # def go_to_login_page(self):
    #     login_link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
    #     login_link.click()
    #
    # def go_to_basket_page(self):
    #     login_link = self.browser.find_element(*BasketPageLocators.BASKET_LINK)
    #     login_link.click()

    # def should_be_login_link(self):
    #     assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"
    #
    # def should_be_basket_link(self):
    #     assert self.is_element_present(*BasketPageLocators.BASKET_LINK), "Basket link is not presented"
    #
    # def should_be_authorized_user(self):
    #     assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
    #                                                                  " probably unauthorised user"

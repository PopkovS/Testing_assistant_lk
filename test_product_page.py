import time

import pytest

from .pages.basket_page import BasketPage
from .pages.login_page import LoginPage
from .pages.product_page import ProductPage


# link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"

@pytest.mark.need_review
@pytest.mark.parametrize('numlink', [0, 1, 2, 3, 4, 5, 6, pytest.param(7, marks=pytest.mark.xfail), 8, 9])
def test_guest_can_add_product_to_basket(browser, numlink):
    link = f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{numlink}"
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.add_to_basket_from_product_page()
    product_page.solve_quiz_and_get_code()
    product_page.should_be_product_page()


@pytest.mark.xfail(reason="This test should fall")
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.add_to_basket_from_product_page()
    product_page.solve_quiz_and_get_code()
    product_page.should_not_be_product_message()


def test_guest_cant_see_success_message(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.should_not_be_product_message()


def test_message_disappeared_after_adding_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
    product_page = ProductPage(browser, link)
    product_page.open()
    product_page.add_to_basket_from_product_page()
    product_page.solve_quiz_and_get_code()
    product_page.should_be_disappear_product_message()


def test_guest_should_see_login_link_on_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.should_be_login_link()

@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.should_be_login_link()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
    page = ProductPage(browser, link)
    page.open()
    page.should_be_basket_link()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_not_be_product_in_basket()
    basket_page.should_be_basket_is_empty()


@pytest.mark.with_authorized_user
class TestUserAddToBasketFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        link = "http://selenium1py.pythonanywhere.com/en-gb/accounts/login/"
        login_page = LoginPage(browser, link)
        login_page.open()
        login_page.register_new_user(str(time.time()) + "@fakemail.org", "stepik4313")
        login_page.should_be_authorized_user()

    @pytest.mark.need_review
    @pytest.mark.parametrize('numlink', [0, 1, 2, 3, 4, 5, 6, pytest.param(7, marks=pytest.mark.xfail), 8, 9])
    def test_user_can_add_product_to_basket(self, browser, numlink):
        link = f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{numlink}"
        product_page = ProductPage(browser, link)
        product_page.open()
        product_page.add_to_basket_from_product_page()
        product_page.solve_quiz_and_get_code()
        product_page.should_be_product_page()

    def test_user_cant_see_success_message(self, browser):
        link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
        product_page = ProductPage(browser, link)
        product_page.open()
        product_page.should_not_be_product_message()

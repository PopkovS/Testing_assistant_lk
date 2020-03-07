import pytest
from pages.my_device_page import MyDevicePage
from pages.locators import Links


@pytest.fixture(scope="module", autouse=True)
def setup_for_module(browser):
    global page
    page = MyDevicePage(browser, Links.MY_DEVICE)
    page.go_to_my_devices()
    yield page
    page.change_user_stat(0)


# class TestsCreateGroupNegative():
    # def test_test1(self, browser):


    # @pytest.fixture(scope="function", autouse=True)
    # def setup_for_login_neg_function(self, browser):
    #     page.change_user_stat(0)
    #     browser.refresh()
    #     yield page
    #     page.should_be_no_more_necessary_alert()
    #     page.should_be_match_link(Links.LOGIN_LINK)

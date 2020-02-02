# from time import sleep
# from .pages.locators import Links
# from .pages.test_page import ATest1Page
from faker import Faker
fake = Faker()
text = fake.password()
print(text)
# link = "http://lk.corp.ast.safib.ru/Account/Login"
#
#
# def test_login_ass(browser):
#     page = ATest1Page(browser, Links.LOGIN_LINK)
#     page.open()
#     page.login_in_assistant("test@safib.ru", "1")
#
#
# def test_2login_ass(browser):
#     page = ATest1Page(browser, link)
#     page.open()
#     page.login_in_assistant("test@safib.ru", "1")
#
#
# def test_3login_ass(browser):
#     page = ATest1Page(browser, link)
#     page.open()
#     page.login_in_assistant("test@safib.ru", "1")
#
#
# def test_4login_ass(browser):
#     page = ATest1Page(browser, link)
#     page.open()
#     page.login_in_assistant("test@safib.ru", "1")

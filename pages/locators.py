from selenium.webdriver.common.by import By
from faker import Faker


# from pages.pg_data_base import PGDB

class Links():
    MAIN_LINK = "http://lk.corp.ast.safib.ru/"
    LOGIN_LINK = MAIN_LINK + "Account/Login"
    ACCESS_RECOVERY_LINK = MAIN_LINK + "Account/SetPassword"
    SET_PASSWORD_LINK = MAIN_LINK + "Account/SetPassword"


class TestData():
    f = Faker()
    FAKE_EMAIL = f.email()
    FAKE_PASSWORD = f.password()
    VALID_EMAIL = "PopkovSergei0805@yandex.ru"
    VALID_PASSWORD = "123"  # очень не надёжной способ хернёй занимаемся
    TEST_USER = "testassistanttest@mailforspam.com"


# class ErrorAlertText():


class LoginLocators():
    EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#PasswordUser[name=\"PasswordUser\"]")
    LOGIN_SUBMIT = (By.CSS_SELECTOR, ".btn.btn-primary.block.full-width.m-b")
    ERR_MESS_EMAIL = (By.CSS_SELECTOR, "#Email+span")
    # ERR_MESS_EMAIL = (By.CSS_SELECTOR, "#Email+[data-valmsg-for=\"Email\"]")
    ERR_MESS_PASSWORD = (By.CSS_SELECTOR, ".s-error-message.field-validation-valid[data-valmsg-for=\"PasswordUser\"]")
    ERR_ALERT = (By.CSS_SELECTOR, ".toast.toast-error .toast-message")
    GO_TO_SET_PASS_BUTT = (By.CSS_SELECTOR, ".other [href=\"/Account/SetPassword\"]")

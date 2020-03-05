import self as self
from selenium.webdriver.common.by import By
from faker import Faker


# from pages.pg_data_base import PGDB

class Links():
    MAIN_LINK = "http://lk.corp.ast.safib.ru/"
    LOGIN_LINK = MAIN_LINK + "Account/Login"
    ACCESS_RECOVERY_LINK = MAIN_LINK + "Account/SetPassword"
    SET_PASSWORD_LINK = MAIN_LINK + "Account/SetPassword"
    MAIL_FOR_SPAM_LINK = "https://www.mailforspam.co/mail/"


class TestData():
    f = Faker()
    FAKE_EMAIL = f.email()
    FAKE_PASSWORD = f.password()
    VALID_EMAIL = "PopkovSergei0805@yandex.ru"
    VALID_PASSWORD = "123"
    TEST_USER = "testassistanttest@mailforspam.com"
    TEST_USER_NAME = "test_user"


# class ErrorAlertText():


class LoginLocators():
    EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]")
    PASSWORD_USER_FIELD = (By.CSS_SELECTOR, "#PasswordUser[name=\"PasswordUser\"]")
    PASSWORD = (By.CSS_SELECTOR, "#Password")
    PASSWORD_CONFIRM = (By.CSS_SELECTOR, "#ConfirmPassword")
    LOGIN_SUBMIT = (By.CSS_SELECTOR, ".btn.btn-primary.block.full-width.m-b")
    SUBMIT_CONF_PASS = (By.CSS_SELECTOR, "#btnOk.btn.btn-primary.block.full-width.m-b")
    ERR_MESS_EMAIL = (By.CSS_SELECTOR, "#Email+span")
    # ERR_MESS_EMAIL = (By.CSS_SELECTOR, "#Email+[data-valmsg-for=\"Email\"]")
    ERR_MESS_PASSWORD = (By.CSS_SELECTOR, ".s-error-message.field-validation-valid[data-valmsg-for=\"PasswordUser\"]")
    ERR_MESS_CHANGE_PASS = (By.CSS_SELECTOR, "span[for=\"Password\"]")
    ERR_MESS_CHANGE_CONF_PASS = (By.CSS_SELECTOR, "span[for=\"ConfirmPassword\"]")
    ERR_ALERT = (By.CSS_SELECTOR, ".toast.toast-error")  # .toast-message"
    GO_TO_SET_PASS_BUTT = (By.CSS_SELECTOR, ".other [href=\"/Account/SetPassword\"]")
    SET_PASS_TITLE = (By.CSS_SELECTOR, ".account-login-cont>.info-capt")
    CONF_CODE_FIELD = (By.CSS_SELECTOR, "[placeholder=\"Код подтверждения\"]")


class BaseLocators():
    USER_MENU = (By.CSS_SELECTOR, ".dropdown-toggle>.uname")
    LOGOUT_BUT = (By.CSS_SELECTOR, ".btn.btn-primary.exit[href=\"/Account/Logoff\"]")


class MailForSpamLocators():
    CHECK_BUTTON = (By.CSS_SELECTOR, "#button.buttonGo")
    LETTERS = (By.CSS_SELECTOR, "tr[onclick]")
    LINK_GO_TO_CHANGE_PASS = (By.XPATH, "//a[text()=\"ссылке\"]")
    CONFIRMATION_CODE = (By.CSS_SELECTOR, "[align=\"left\"]>div>b")



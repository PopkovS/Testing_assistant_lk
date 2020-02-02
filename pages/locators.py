from selenium.webdriver.common.by import By
from faker import Faker

class Links():
    MAIN_LINK = "http://lk.pub.ast.safib.ru/"
    LOGIN_LINK = MAIN_LINK + "Account/Login"
    ACCESS_RECOVERY_LINK = MAIN_LINK + "Account/SetPassword"

class TestData():
    f = Faker()
    FAKE_EMAIL = f.email()
    FAKE_PASSWORD = f.password()
    VALID_EMAIL = "PopkovSergei0805@yandex.ru"
    VALID_PASSWORD = "123" #очень не надёжной хернёй занимаемся
    BLOCKED_EMAIL = "popkovsergei080522@ro.ru"
    NOT_CONFIRMED_EMAIL = "assistant.safib2@bk.ru"
    ARCHIVED_EMAIL = "fdron80@gmail.com"



class LoginLocators():
    EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#PasswordUser[name=\"PasswordUser\"]")
    LOGIN_SUBMIT = (By.CSS_SELECTOR, ".btn.btn-primary.block.full-width.m-b")
    ERR_MESS_EMAIL = (By.CSS_SELECTOR, ".field-validation-valid.s-error-message[data-valmsg-for=\"Email\"]")
    ERR_MESS_PASSWORD = (By.CSS_SELECTOR, ".s-error-message.field-validation-valid[data-valmsg-for=\"PasswordUser\"]")
    ERR_ALERT = (By.CSS_SELECTOR, ".toast.toast-error .toast-message")

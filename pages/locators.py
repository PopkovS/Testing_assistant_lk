from selenium.webdriver.common.by import By

class Links():
    MAIN_LINK = "http://lk.pub.ast.safib.ru/"
    AUTHORIZATION_LINK = MAIN_LINK + "Account/Login"



class AuthorizationAndRegistrationLocators():
    EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#PasswordUser[name=\"PasswordUser\"]")
    LOGIN_SUBMIT = (By.CSS_SELECTOR, ".btn.btn-primary.block.full-width.m-b")

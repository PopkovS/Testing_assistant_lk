import self as self
from selenium.webdriver.common.by import By
from faker import Faker


class TestData():
    f = Faker()
    FAKE_EMAIL = f.email()
    FAKE_PASSWORD = f.password()
    USER_AD_EMAIL = "testassistantAD@mailforspam.com"
    USER_AD_NAME = USER_AD_EMAIL.replace(".", "@").split("@")[0]
    PASSWORD_USER_AD = "Password1"
    USER_NORMAL_EMAIL = "testassistantNormal@mailforspam.com"
    PASSWORD_USER_NORMAL = "Password2"
    USER_NORMAL_NAME = USER_NORMAL_EMAIL.replace(".", "@").split("@")[0]
    NEW_USER_EMAIL = "testassistNewUser@mailforspam.com"
    NEW_USER_NAME = NEW_USER_EMAIL.replace(".", "@").split("@")[0]
    NEW_USER_EMAIL2 = "testassistNewUser2@mailforspam.com"
    NEW_USER_NAME2 = NEW_USER_EMAIL2.replace(".", "@").split("@")[0]
    AD_SERVE = "test.local"
    AD_NAME = "user1"
    AD_PASSWORD = "Password1"


class Links():
    MAIN_LINK = "http://lk.corp.ast.safib.ru"
    LOGIN_LINK = MAIN_LINK + "/Account/Login"
    REGISTRATION_LINK = MAIN_LINK + "/Account/Register"
    REGISTRATION_SEND_MESS = MAIN_LINK + "/Account/SendMessageRegister"
    ACCESS_RECOVERY_LINK = MAIN_LINK + "/Account/SetPassword"
    MY_DEVICE = MAIN_LINK + "/ClientDevice"
    MY_DEVICE_CREATE_GROUP = MY_DEVICE + "/CreateGroup?orgid=0"
    SET_PASSWORD_LINK = MAIN_LINK + "/Account/SetPassword"
    RESEND_EMAIL_LINK = MAIN_LINK + "/Account/ReConfirmRegister"
    MAIL_FOR_SPAM_LINK = "https://www.mailforspam.co/mail/"
    ADM_USERS = MAIN_LINK + "/User"
    MAIL_FOR_SPAM_NORM_US = MAIL_FOR_SPAM_LINK + TestData.USER_NORMAL_EMAIL.lower().split("@")[0]
    MAIL_FOR_SPAM_AD_US = MAIL_FOR_SPAM_LINK + TestData.USER_AD_EMAIL.lower().split("@")[0]
    MAIL_FOR_SPAM_NEW_US = MAIL_FOR_SPAM_LINK + TestData.NEW_USER_EMAIL.lower().split("@")[0]
    MAIL_FOR_SPAM_NEW_US2 = MAIL_FOR_SPAM_LINK + TestData.NEW_USER_EMAIL2.lower().split("@")[0]


class LoginLocators():
    EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]")
    PASSWORD_USER_FIELD = (By.CSS_SELECTOR, "#PasswordUser[name=\"PasswordUser\"]")
    SUBMIT_CONF_PASS = (By.CSS_SELECTOR, "#btnOk.btn.btn-primary.block.full-width.m-b")
    ERR_MESS_EMAIL = (By.CSS_SELECTOR, "#Email+span")
    ERR_MESS_PASSWORD = (By.CSS_SELECTOR, ".s-error-message.field-validation-valid[data-valmsg-for=\"PasswordUser\"]")
    ERR_MESS_CHANGE_PASS = (By.CSS_SELECTOR, "span[for=\"Password\"]")
    ERR_MESS_CHANGE_CONF_PASS = (By.CSS_SELECTOR, "span[for=\"ConfirmPassword\"]")
    # ERR_ALERT = (By.CSS_SELECTOR, ".toast.toast-error")  # .toast-message"
    GO_TO_SET_PASS_BUTT = (By.CSS_SELECTOR, '.other [href="/Account/SetPassword"]')
    GO_TO_RESEND_EMAIL_BUTT = (By.CSS_SELECTOR, '[title="Повторная отправка инструкций"]')
    RESEND_EMAIL_TITLE = (By.CSS_SELECTOR, '.account-login-cont>:nth-child(1) ')
    SET_PASS_TITLE = (By.CSS_SELECTOR, ".account-login-cont>.info-capt")
    CONF_CODE_FIELD = (By.CSS_SELECTOR, "[placeholder=\"Код подтверждения\"]")


class RegistrationLocators():
    GO_TO_REGISTRATION_PAGE = (By.CSS_SELECTOR, ".register[href=\"/Account/Register\"]")
    GO_TO_LOGIN_PAGE_FROM_REG = (By.CSS_SELECTOR, '.s-button[href="/"]')
    NAME_USER_FIELD = (By.CSS_SELECTOR, '#Name[name="Name"]')
    REGISTRATION_TITLE = (By.CSS_SELECTOR, ".account-login-cont>.header")
    REG_CONFIRM_TITLE = (By.CSS_SELECTOR, ".account-login-cont>.info-capt")
    REG_CONFIRM_TEXT = (By.CSS_SELECTOR, ".account-login-cont>.info")


class AdmUserLocators():
    IMPORT_FROM_AD_BUTT = (By.CSS_SELECTOR, '.btn.btn-primary.btn-w-m-i[href="/User/ImportFromADCredentials"]')
    AD_SERVER_FIELD = (By.ID, "ServerName")
    AD_NAME_FIELD = (By.ID, "UN")
    AD_PASSWORD_FIELD = (By.ID, "Pwd")
    UPDATE_ATR_CHBOX = (By.CSS_SELECTOR, "#UpdateDataIfUserFindedByObjectGuid+.iCheck-helper")
    JOIN_EMAIL_CHBOX = (By.CSS_SELECTOR, "#UpdateDataIfUserFindedByEmail+.iCheck-helper")
    UPDATE_NOT_ACT_CHBOX = (By.CSS_SELECTOR, "#UpdateDataIfUserNonActive+.iCheck-helper")
    CONNECTION_WITH_AD = (By.CSS_SELECTOR, ".ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front")
    TITLE_IMPORT_AD_PAGE = (By.XPATH, '//div/h2[text()="Импорт учетных записей из Active Directory"]')
    IMPORT_BUTT = (By.CSS_SELECTOR, '[data-url="/User/ImportFromADSelectTargetsParam"]')


class MyDevicesLocators():
    ADD_GROUP_BUTTON = (By.CSS_SELECTOR, '[href="/ClientDevice/CreateGroup?orgid=0"]')
    ADD_DEVICE_BUTTON = (By.CSS_SELECTOR, '[href="/ClientDevice/Create?orgid=0"]')
    REFRESH_GROUP_LIST = (By.CSS_SELECTOR, "#ClientDeviceTable_0_refresh")
    SAVE_GROUP_BUTTON = (By.CSS_SELECTOR, '.ctrls>.btn.btn-primary')
    CANCEL_GROUP_BUTTON = (By.CSS_SELECTOR, '.ctrls>.btn.btn-primary+.btn.btn-white')
    GROUP_NAME_FIELD = (By.CSS_SELECTOR, ".text-box.single-line")
    SELECT_PARENT_GROUP = (By.CSS_SELECTOR, "#select2-GroupId-container")
    DESCRIPTION_DEVICE_FIELD = (By.CSS_SELECTOR, "##Description")


class BaseLocators():
    EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#Password")
    PASSWORD_CONFIRM_FIELD = (By.CSS_SELECTOR, "#ConfirmPassword")
    HID_FIELD = (By.CSS_SELECTOR, "#HID")
    NAME_FIELD = (By.CSS_SELECTOR, "#Name")
    ERR_EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]+span")
    ERR_HID_FIELD = (By.CSS_SELECTOR, "#HID+span")
    ERR_NAME_FIELD = (By.CSS_SELECTOR, "#Name+span")
    ERR_PAS_FIELD = (By.CSS_SELECTOR, "#Password+span")
    ERR_PAS_CONF_FIELD = (By.CSS_SELECTOR, "#ConfirmPassword+span")
    USER_MENU = (By.CSS_SELECTOR, ".dropdown-toggle>.uname")
    LOGOUT_BUTT = (By.CSS_SELECTOR, ".btn.btn-primary.exit[href=\"/Account/Logoff\"]")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".btn.btn-primary.block.full-width.m-b")
    SUBMIT_UNIVERSAL_BUTT = (By.CSS_SELECTOR, '.btn.btn-sm.btn-primary[type="submit"]')
    SEARCH_FIELD = (By.CSS_SELECTOR, '.form-control.input-sm[type="search"]')
    # CHECKBOX_IN_TABLE = (By.CSS_SELECTOR, "tbody > tr")
    CHECKBOX_IN_TABLE = (By.CSS_SELECTOR, "tbody>tr>td:nth-child(2)")
    ALERT = (By.CSS_SELECTOR, "#toast-container")  # .toast-message"


class Menu():
    MENU_FIRST_LEVEL_MY_AS = (By.XPATH, '//span[text()="Мой ассистент"]')
    MENU_FIRST_LEVEL_MY_ORG = (By.XPATH, '//span[text()="Мои организации"]')
    MENU_FIRST_LEVEL_ADM = (By.XPATH, '//span[text()="Администрирование"]')
    MENU_SECOND_LEVEL_ADM_USR = (By.CSS_SELECTOR, 'li>[href="/User"]')


class MailForSpamLocators():
    CHECK_BUTTON = (By.CSS_SELECTOR, "#button.buttonGo")
    LETTERS = (By.CSS_SELECTOR, "tr[onclick]")
    LINK_GO_TO_CHANGE_PASS = (By.XPATH, '//a[text()="ссылке"]')
    CONFIRMATION_CODE = (By.CSS_SELECTOR, "[align=\"left\"]>div>b")

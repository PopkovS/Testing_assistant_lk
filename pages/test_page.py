from .base_page import BasePage
from .locators import AuthorizationAndRegistrationLocators


class ATest1Page(BasePage):
    def login_link(self):
        link = self.main_link + "Account/Login"
        return link

    def login_in_assistant(self, email, password):
        email_field = self.browser.find_element(*AuthorizationAndRegistrationLocators.EMAIL_FIELD)
        password_field = self.browser.find_element(*AuthorizationAndRegistrationLocators.PASSWORD_FIELD)
        email_field.send_keys(email)
        password_field.send_keys(password)
        author_submit_button = self.browser.find_element(*AuthorizationAndRegistrationLocators.LOGIN_SUBMIT)
        author_submit_button.click()

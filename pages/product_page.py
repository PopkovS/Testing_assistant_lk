from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def add_to_basket_from_product_page(self):
        add_to_basket_button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON)
        add_to_basket_button.click()

    def should_be_product_page(self):
        self.browser.delete_all_cookies()
        self.should_be_some_price_for_product_and_in_basket(self.price_in_basket_text())
        self.should_be_some_product_name_on_page_and_in_message(self.product_name_in_message_text())

    def price_in_basket_text(self):
        price_in_basket = (self.browser.find_element(*ProductPageLocators.PRICE_IN_BASKET).text.replace('\n', ': ').split(': '))[1]
        return price_in_basket

    def product_name_in_message_text(self):
        product_name_in_message = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME_IN_MESSAGE).text
        return product_name_in_message

    def should_not_be_product_message(self):
        assert self.is_not_element_present(*ProductPageLocators.PRODUCT_NAME_IN_MESSAGE), "Product messages should " \
                                                                                          "not be "

    def should_be_disappear_product_message(self):
        assert self.is_disappeared(*ProductPageLocators.PRODUCT_NAME_IN_MESSAGE), "Product message did not disappear"

    def should_be_some_price_for_product_and_in_basket(self, price_to_compare):
        price_on_pages_on_product = self.browser.find_element(*ProductPageLocators.PRICE_ON_PAGES_OF_PRODUCT).text
        assert price_on_pages_on_product == price_to_compare, f"Price product: \"{price_on_pages_on_product}\" " \
                                                             f"differs from price in basket: \"{price_to_compare}\" "

    def should_be_some_product_name_on_page_and_in_message(self, product_name_to_compare):
        product_name_on_page = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME_ON_PAGE).text
        assert product_name_on_page == product_name_to_compare, f"The product price on the page: \"{product_name_on_page}\""\
                                                                f" differs from the product price in the message: \"{product_name_to_compare}\""
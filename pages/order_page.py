from locators.page_locators import OrderPageLocators
from pages.cart_page import CartPage


class OrderPage(CartPage):
    order = OrderPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    def get_order_page_title(self) -> str:
        """Get order page title"""
        return self.action_get_text(self.order.PAGE_TITLE)

    def get_order_page_subtitle(self) -> str:
        """Get order page subtitle"""
        return self.action_get_text(self.order.PAGE_SUBTITLE)

    def get_order_page_text(self) -> str:
        """Get order page text"""
        return self.action_get_text(self.order.PAGE_TEXT)

    def click_order_back_button(self) -> None:
        """Click back button"""
        self.action_left_click(self.element_is_visible(self.order.BACK_BUTTON))

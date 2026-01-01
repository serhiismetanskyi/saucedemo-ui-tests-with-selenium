from selenium.webdriver.remote.webelement import WebElement

from locators.page_locators import CartPageLocators
from pages.inventory_page import InventoryPage


class CartPage(InventoryPage):
    cart = CartPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    def get_cart_page_title(self) -> str:
        """Get cart page title"""
        return self.action_get_text(self.cart.PAGE_TITLE)

    def get_item_count(self) -> int:
        """Get number of items in cart"""
        return len(self.elements_are_visible(self.cart.CART_ITEM))

    def get_all_cart_item_elements(self) -> list[WebElement]:
        """Get all cart item elements"""
        return self.elements_are_visible(self.cart.CART_ITEM)

    def get_list_of_cart_item_names(self) -> list[str]:
        """Get list of cart item names"""
        item_names = self.elements_are_visible(self.cart.CART_ITEM_NAME)
        return self.action_get_text_from_elements(item_names)

    def get_list_of_cart_item_descs(self) -> list[str]:
        """Get list of cart item descriptions"""
        item_descs = self.elements_are_visible(self.cart.CART_ITEM_DESC)
        return self.action_get_text_from_elements(item_descs)

    def get_list_of_cart_item_prices(self) -> list[float]:
        """Get list of cart item prices"""
        item_prices = self.elements_are_visible(self.cart.CART_ITEM_PRICE)
        return [float(price.text.replace("$", "")) for price in item_prices]

    def get_list_of_remove_buttons(self) -> list[WebElement]:
        """Get all remove buttons"""
        return self.elements_are_visible(self.cart.REMOVE_BUTTON)

    def remove_all_from_cart(self) -> None:
        """Remove all products from cart"""
        remove_buttons = self.get_list_of_remove_buttons()
        self.logger.info(f"Removing {len(remove_buttons)} products from cart")
        self.action_left_click_on_elements(remove_buttons)

    def calc_cart_item_total_price(self) -> float:
        """Calculate total price of items"""
        item_prices = self.get_list_of_cart_item_prices()
        return sum(item_prices)

    def calc_cart_tax_price(self) -> float:
        """Calculate tax price"""
        item_total_price = self.calc_cart_item_total_price()
        tax_price = (item_total_price * 8) / 100
        return round(tax_price, 2)

    def calc_cart_total_price(self) -> float:
        """Calculate total price with tax"""
        item_total_price = self.calc_cart_item_total_price()
        tax_price = self.calc_cart_tax_price()
        total_price = item_total_price + tax_price
        return round(total_price, 2)

    def get_list_of_cart_calc_prices(self) -> list[float]:
        """Get sorted list of all calculated prices"""
        item_total_price = self.calc_cart_item_total_price()
        tax_price = self.calc_cart_tax_price()
        total_price = self.calc_cart_total_price()
        prices = [item_total_price, tax_price, total_price]
        return sorted(prices)

    def check_cart_is_empty(self) -> bool:
        """Check if cart is empty"""
        cart_item = self.element_is_not_visible(self.cart.CART_ITEM)
        return cart_item

    def click_continue_shopping(self) -> None:
        """Click continue shopping button"""
        self.logger.info("Clicking continue shopping")
        self.action_left_click(self.element_is_visible(self.cart.CONTINUE_SHOPPING_BUTTON))

    def click_checkout(self) -> None:
        """Click checkout button"""
        self.logger.info("Clicking checkout")
        self.action_left_click(self.element_is_visible(self.cart.CHECKOUT_BUTTON))

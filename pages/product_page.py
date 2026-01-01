from locators.page_locators import ProductPageLocators
from pages.inventory_page import InventoryPage


class ProductPage(InventoryPage):
    product = ProductPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_name(self) -> str:
        """Get product name"""
        return self.action_get_text(self.product.NAME)

    def get_product_desc(self) -> str:
        """Get product description"""
        return self.action_get_text(self.product.DESC)

    def get_product_price(self) -> float:
        """Get product price"""
        product_price = self.action_get_text(self.product.PRICE)
        return float(product_price.replace("$", ""))

    def click_add_product_to_cart(self) -> None:
        """Click add to cart button"""
        self.action_left_click(self.element_is_visible(self.product.ADD_TO_CART_BUTTON))

    def click_remove_product_from_cart(self) -> None:
        """Click remove button"""
        self.action_left_click(self.element_is_visible(self.product.REMOVE_BUTTON))

    def click_back_to_products_button(self) -> None:
        """Click back to products button"""
        self.action_left_click(self.element_is_visible(self.product.BACK_BUTTON))

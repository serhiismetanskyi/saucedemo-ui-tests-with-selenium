import random

from selenium.webdriver.remote.webelement import WebElement

from locators.page_locators import InventoryPageLocators
from pages.login_page import LoginPage


class InventoryPage(LoginPage):
    inventory = InventoryPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    def get_products_page_title(self) -> str:
        """Get products page title"""
        return self.action_get_text(self.inventory.PAGE_TITLE)

    def open_hamburger_menu(self) -> None:
        """Open hamburger menu"""
        self.action_left_click(self.element_is_visible(self.inventory.HAMBURGER_ICON))

    def click_logout_button(self) -> None:
        """Click logout button"""
        self.action_left_click(self.element_is_visible(self.inventory.LOGOUT_BUTTON))

    def logout(self) -> None:
        """Logout from application"""
        self.logger.info("Logging out")
        self.open_hamburger_menu()
        self.click_logout_button()

    def get_menu_links(self) -> list[WebElement]:
        """Get all menu links"""
        return self.elements_are_visible(self.inventory.HAMBURGER_MENU)

    def get_menu_links_text(self) -> list[str]:
        """Get text from all menu links"""
        menu_links = self.get_menu_links()
        return self.action_get_text_from_elements(menu_links)

    def open_cart_page(self) -> None:
        """Open cart page"""
        self.action_left_click(self.element_is_visible(self.inventory.CART_ICON))

    def check_cart_count_exists(self) -> bool:
        """Check if cart count badge exists"""
        cart_count = self.element_is_present(self.inventory.CART_COUNT)
        return cart_count is not None

    def check_cart_count_not_exist(self) -> bool:
        """Check if cart count badge doesn't exist"""
        return self.element_is_not_visible(self.inventory.CART_COUNT)

    def get_cart_item_count(self) -> int:
        """Get number of items in cart"""
        if self.check_cart_count_exists():
            return int(self.action_get_text(self.inventory.CART_COUNT))
        return 0

    def get_products_count(self) -> int:
        """Get total number of products"""
        return len(self.elements_are_visible(self.inventory.INVENTORY_ITEM))

    def get_all_product_elements(self) -> list[WebElement]:
        """Get all product elements"""
        return self.elements_are_visible(self.inventory.INVENTORY_ITEM)

    def get_list_of_product_urls(self) -> list[str]:
        """Get list of product URLs"""
        product_links = self.elements_are_present(self.inventory.INVENTORY_ITEM_URL)
        urls = self.action_get_attr_from_elements(product_links, "id")
        urls_with_id = []
        for product_id in urls:
            # Get number from id like 'item_4_title_link' -> '4'
            if product_id and "item_" in product_id:
                num_id = product_id.split("_")[1]
                url = f"https://www.saucedemo.com/inventory-item.html?id={num_id}"
                urls_with_id.append(url)
        return urls_with_id

    def get_list_of_product_names(self) -> list[str]:
        """Get list of product names"""
        product_names = self.elements_are_visible(self.inventory.INVENTORY_ITEM_NAME)
        return self.action_get_text_from_elements(product_names)

    def get_list_of_product_descs(self) -> list[str]:
        """Get list of product descriptions"""
        product_descs = self.elements_are_visible(self.inventory.INVENTORY_ITEM_DESC)
        return self.action_get_text_from_elements(product_descs)

    def get_list_of_product_prices(self) -> list[float]:
        """Get list of product prices"""
        product_prices = self.elements_are_visible(self.inventory.INVENTORY_ITEM_PRICE)
        return [float(price.text.replace("$", "")) for price in product_prices]

    def get_list_of_add_to_cart_buttons(self) -> list[WebElement]:
        """Get all add to cart buttons"""
        return self.elements_are_visible(self.inventory.ADD_TO_CART_BUTTON)

    def get_list_of_remove_from_cart_buttons(self) -> list[WebElement]:
        """Get all remove buttons"""
        return self.elements_are_visible(self.inventory.REMOVE_BUTTON)

    def add_all_to_cart(self) -> None:
        """Add all products to cart"""
        add_to_cart_buttons = self.get_list_of_add_to_cart_buttons()
        self.logger.info(f"Adding {len(add_to_cart_buttons)} products to cart")
        self.action_left_click_on_elements(add_to_cart_buttons)

    def remove_all_from_cart(self) -> None:
        """Remove all products from cart"""
        remove_from_cart_buttons = self.get_list_of_remove_from_cart_buttons()
        self.logger.info(f"Removing {len(remove_from_cart_buttons)} products")
        self.action_left_click_on_elements(remove_from_cart_buttons)

    def open_random_product(self) -> None:
        """Open random product page"""
        product_urls_list = self.get_list_of_product_urls()
        url_index = random.randrange(0, len(product_urls_list))
        product_url = product_urls_list[url_index]
        self.open_url(product_url)

    def open_products_sort_menu(self) -> None:
        """Open products sort dropdown"""
        self.action_left_click(self.element_is_visible(self.inventory.SORT_MENU))

    def sort_products_a_to_z(self) -> None:
        """Sort products alphabetically A to Z"""
        self.logger.info("Sorting: A to Z")
        self.open_products_sort_menu()
        self.element_is_present(self.inventory.SORT_A_Z).click()

    def sort_products_z_to_a(self) -> None:
        """Sort products alphabetically Z to A"""
        self.logger.info("Sorting: Z to A")
        self.open_products_sort_menu()
        self.element_is_present(self.inventory.SORT_Z_A).click()

    def sort_products_low_to_high(self) -> None:
        """Sort products by price low to high"""
        self.logger.info("Sorting: Price Low to High")
        self.open_products_sort_menu()
        self.element_is_present(self.inventory.SORT_LOW_HIGH).click()

    def sort_products_high_to_low(self) -> None:
        """Sort products by price high to low"""
        self.logger.info("Sorting: Price High to Low")
        self.open_products_sort_menu()
        self.element_is_present(self.inventory.SORT_HIGH_LOW).click()

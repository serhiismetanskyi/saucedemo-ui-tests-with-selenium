import pytest

from data.tests_data import InventoryPage, Links, Users
from tests.test_base import BaseTest
from utils.logger import get_logger, log_assertion, log_test_end, log_test_start


class TestProduct(BaseTest):
    """Product page tests"""

    logger = get_logger(__name__)

    @pytest.mark.parametrize(
        "username, password",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD),
        ],
    )
    def test_open_product(self, username, password):
        """Test opening product page"""
        log_test_start(self.logger, "test_open_product", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        all_product_names = self.pages["inventory_page"].get_list_of_product_names()
        all_product_prices = self.pages["inventory_page"].get_list_of_product_prices()
        self.pages["inventory_page"].open_random_product()
        actual_product_name = self.pages["product_page"].get_product_name()
        actual_product_price = self.pages["product_page"].get_product_price()

        self.logger.info(f"Product: {actual_product_name}, Price: {actual_product_price}")
        assert self.pages["product_page"].find_value_in_data(actual_product_name, all_product_names) is True, (
            "The product name does not match to product name from inventory page"
        )
        assert self.pages["product_page"].find_value_in_data(actual_product_price, all_product_prices) is True, (
            "The product price does not match to product price from inventory page"
        )

        log_test_end(self.logger, "test_open_product", "PASSED")

    @pytest.mark.parametrize(
        "username, password",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD),
        ],
    )
    def test_add_product_to_cart(self, username, password):
        """Test adding product to cart"""
        log_test_start(self.logger, "test_add_product_to_cart", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_random_product()
        actual_product_name = self.pages["product_page"].get_product_name()
        actual_product_price = self.pages["product_page"].get_product_price()
        self.pages["product_page"].click_add_product_to_cart()
        self.pages["product_page"].open_cart_page()
        actual_cart_item_count = self.pages["cart_page"].get_cart_item_count()
        all_cart_item_names = self.pages["cart_page"].get_list_of_cart_item_names()
        all_cart_item_prices = self.pages["cart_page"].get_list_of_cart_item_prices()

        log_assertion(self.logger, 1, actual_cart_item_count, "Cart contains 1 item")
        assert actual_cart_item_count == 1, "The shopping cart does not contain a product'"

        self.logger.info(f"Product in cart: {actual_product_name}, {actual_product_price}")
        assert self.pages["cart_page"].find_value_in_data(actual_product_name, all_cart_item_names) is True, (
            "The item name in cart does not match to name from product page"
        )
        assert self.pages["cart_page"].find_value_in_data(actual_product_price, all_cart_item_prices) is True, (
            "The item price in cart does not match to price from product page"
        )

        log_test_end(self.logger, "test_add_product_to_cart", "PASSED")

    @pytest.mark.parametrize(
        "username, password",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD),
        ],
    )
    def test_remove_product_from_cart(self, username, password):
        """Test removing product from cart"""
        log_test_start(self.logger, "test_remove_product_from_cart", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_random_product()
        self.pages["product_page"].click_add_product_to_cart()
        actual_cart_item_count = self.pages["product_page"].get_cart_item_count()

        log_assertion(self.logger, 1, actual_cart_item_count, "Cart contains 1 item")
        assert actual_cart_item_count == 1, "The shopping cart does not contain a product"

        self.pages["product_page"].click_remove_product_from_cart()
        expected_cart_is_empty = self.pages["cart_page"].check_cart_is_empty()
        expected_cart_item_count_not_exist = self.pages["cart_page"].check_cart_count_not_exist()

        self.logger.info(
            f"Cart empty: {expected_cart_is_empty}, Cart count not exist: {expected_cart_item_count_not_exist}"
        )
        assert expected_cart_is_empty is True, "The cart contains items"
        assert expected_cart_item_count_not_exist is True, "The cart contains items"

        log_test_end(self.logger, "test_remove_product_from_cart", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, InventoryPage.PRODUCTS_TITLE, Links.PRODUCTS),
        ],
    )
    def test_back_to_products(self, username, password, expected_title, expected_url):
        """Test back to products button"""
        log_test_start(self.logger, "test_back_to_products", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_random_product()
        self.pages["product_page"].click_back_to_products_button()
        actual_title_after_back_from_product = self.pages["inventory_page"].get_products_page_title()
        expected_title_after_back_from_product = expected_title
        actual_url_after_back_from_product = self.pages["inventory_page"].action_get_url()
        expected_url_after_back_from_product = expected_url

        log_assertion(
            self.logger,
            expected_title_after_back_from_product,
            actual_title_after_back_from_product,
            "Title after back validation",
        )
        assert expected_title_after_back_from_product == actual_title_after_back_from_product, (
            f"The actual title '{actual_title_after_back_from_product}' does not match the expected title '{expected_title_after_back_from_product}'"
        )

        log_assertion(
            self.logger,
            expected_url_after_back_from_product,
            actual_url_after_back_from_product,
            "URL after back validation",
        )
        assert expected_url_after_back_from_product == actual_url_after_back_from_product, (
            f"The actual url '{actual_url_after_back_from_product}' does not match the expected url '{expected_url_after_back_from_product}'"
        )

        log_test_end(self.logger, "test_back_to_products", "PASSED")

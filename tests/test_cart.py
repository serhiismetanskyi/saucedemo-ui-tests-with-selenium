import pytest

from data.tests_data import CartPage, InventoryPage, Links, Users
from tests.test_base import BaseTest
from utils.logger import get_logger, log_assertion, log_test_end, log_test_start


class TestCart(BaseTest):
    """Cart page tests"""

    logger = get_logger(__name__)

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, CartPage.CART_TITLE, Links.CART),
        ],
    )
    def test_open_cart(self, username, password, expected_title, expected_url):
        """Test opening cart page"""
        log_test_start(self.logger, "test_open_cart", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        actual_cart_title = self.pages["cart_page"].get_cart_page_title()
        expected_cart_title = expected_title
        actual_cart_url = self.pages["cart_page"].action_get_url()
        expected_cart_url = expected_url

        log_assertion(self.logger, expected_cart_title, actual_cart_title, "Cart title validation")
        assert expected_cart_title == actual_cart_title, (
            f"The actual title '{actual_cart_title}' does not match the expected title '{expected_cart_title}'"
        )

        log_assertion(self.logger, expected_cart_url, actual_cart_url, "Cart URL validation")
        assert expected_cart_url == actual_cart_url, (
            f"The actual url '{actual_cart_url}' does not match the expected url '{expected_cart_url}'"
        )

        log_test_end(self.logger, "test_open_cart", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, InventoryPage.PRODUCTS_TITLE, Links.PRODUCTS),
        ],
    )
    def test_click_continue_shopping(self, username, password, expected_title, expected_url):
        """Test continue shopping button from cart"""
        log_test_start(self.logger, "test_click_continue_shopping", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_continue_shopping()
        actual_title_after_back_from_cart = self.pages["inventory_page"].get_products_page_title()
        expected_title_after_back_from_cart = expected_title
        actual_url_after_back_from_cart = self.pages["inventory_page"].action_get_url()
        expected_url_after_back_from_cart = expected_url

        log_assertion(
            self.logger,
            expected_title_after_back_from_cart,
            actual_title_after_back_from_cart,
            "Title after back validation",
        )
        assert expected_title_after_back_from_cart == actual_title_after_back_from_cart, (
            f"The actual title '{actual_title_after_back_from_cart}' does not match the expected title '{expected_title_after_back_from_cart}'"
        )

        log_assertion(
            self.logger, expected_url_after_back_from_cart, actual_url_after_back_from_cart, "URL after back validation"
        )
        assert expected_url_after_back_from_cart == actual_url_after_back_from_cart, (
            f"The actual url '{actual_url_after_back_from_cart}' does not match the expected url '{expected_url_after_back_from_cart}'"
        )

        log_test_end(self.logger, "test_click_continue_shopping", "PASSED")

    @pytest.mark.parametrize(
        "username, password",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD),
        ],
    )
    def test_remove_all_from_cart(self, username, password):
        """Test removing all items from cart"""
        log_test_start(self.logger, "test_remove_all_from_cart", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].add_all_to_cart()
        actual_product_count = self.pages["inventory_page"].get_products_count()
        expected_cart_item_count = self.pages["inventory_page"].get_cart_item_count()

        log_assertion(self.logger, expected_cart_item_count, actual_product_count, "Cart count matches product count")
        assert expected_cart_item_count == actual_product_count, (
            f"The actual product count '{actual_product_count}' does not match the expected cart item count '{expected_cart_item_count}'"
        )

        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].remove_all_from_cart()
        expected_cart_is_empty = self.pages["cart_page"].check_cart_is_empty()
        expected_cart_item_count_not_exist = self.pages["cart_page"].check_cart_count_not_exist()

        self.logger.info(
            f"Cart is empty: {expected_cart_is_empty}, Cart count not exist: {expected_cart_item_count_not_exist}"
        )
        assert expected_cart_is_empty is True, "The cart contains items"
        assert expected_cart_item_count_not_exist is True, "The cart contains items"

        log_test_end(self.logger, "test_remove_all_from_cart", "PASSED")

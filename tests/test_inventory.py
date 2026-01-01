import pytest

from data.tests_data import InventoryPage, Users
from tests.test_base import BaseTest
from utils.logger import get_logger, log_assertion, log_test_end, log_test_start


class TestInventory(BaseTest):
    """Inventory page tests"""

    logger = get_logger(__name__)

    @pytest.mark.parametrize(
        "username, password, expected_links",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, InventoryPage.HAMBURGER_MENU_LIST),
        ],
    )
    def test_check_menu_links(self, username, password, expected_links):
        """Test menu links are displayed correctly"""
        log_test_start(self.logger, "test_check_menu_links", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_hamburger_menu()
        actual_menu_links = self.pages["inventory_page"].get_menu_links_text()
        expected_menu_links = expected_links

        log_assertion(self.logger, expected_menu_links, actual_menu_links, "Menu links validation")
        assert actual_menu_links == expected_menu_links, (
            f"List of menu links {actual_menu_links} does not match the expected {expected_menu_links}"
        )

        log_test_end(self.logger, "test_check_menu_links", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_purchase_one_item(self, username, password):
        """Test purchasing single item"""
        log_test_start(self.logger, "test_purchase_one_item", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_random_product()
        actual_product_price = self.pages["product_page"].get_product_price()
        self.pages["product_page"].click_add_product_to_cart()
        self.pages["inventory_page"].open_cart_page()
        all_cart_item_prices = self.pages["cart_page"].get_list_of_cart_item_prices()

        self.logger.info(f"Product price: {actual_product_price}, Cart prices: {all_cart_item_prices}")
        assert self.pages["cart_page"].find_value_in_data(actual_product_price, all_cart_item_prices) is True, (
            "The product price does not match to item price from cart page"
        )

        expected_cart_calc_prices = self.pages["cart_page"].get_list_of_cart_calc_prices()
        self.pages["cart_page"].click_checkout()
        first_name = self.data["generator"].first_name()
        last_name = self.data["generator"].last_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].fill_checkout_form(first_name, last_name, zip_code)
        self.pages["checkout_page"].click_continue_checkout()
        actual_overview_total_prices = self.pages["overview_page"].get_list_of_overview_total_prices()
        expected_overview_calc_prices = self.pages["overview_page"].get_list_of_overview_calc_prices()

        log_assertion(
            self.logger, expected_cart_calc_prices, actual_overview_total_prices, "Cart prices match overview prices"
        )
        assert expected_cart_calc_prices == pytest.approx(actual_overview_total_prices, rel=1e-9), (
            "The item prices from cart page does not match to item price from overview page"
        )

        log_assertion(
            self.logger,
            expected_overview_calc_prices,
            actual_overview_total_prices,
            "Overview calc prices match total prices",
        )
        assert expected_overview_calc_prices == pytest.approx(actual_overview_total_prices, rel=1e-9), (
            "The item prices from overview page does not match to total_prices from overview page"
        )

        self.pages["overview_page"].click_finish_overview()
        expected_cart_item_count_not_exist = self.pages["order_page"].check_cart_count_not_exist()

        self.logger.info(f"Cart count not exist: {expected_cart_item_count_not_exist}")
        assert expected_cart_item_count_not_exist is True, "The cart contains items"

        log_test_end(self.logger, "test_purchase_one_item", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_purchase_all_item(self, username, password):
        """Test purchasing all items"""
        log_test_start(self.logger, "test_purchase_all_item", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        all_product_names = self.pages["inventory_page"].get_list_of_product_names()
        all_product_prices = self.pages["inventory_page"].get_list_of_product_prices()

        self.logger.info(f"Found {len(all_product_names)} products")
        assert len(all_product_names) > 0, "No products found on inventory page"

        self.pages["inventory_page"].add_all_to_cart()
        self.pages["inventory_page"].open_cart_page()
        all_cart_item_names = self.pages["cart_page"].get_list_of_cart_item_names()
        all_cart_item_prices = self.pages["cart_page"].get_list_of_cart_item_prices()

        log_assertion(self.logger, all_product_names, all_cart_item_names, "Product names match cart item names")
        assert all_product_names == all_cart_item_names, (
            "The product names in inventory do not match to item names from cart page"
        )

        log_assertion(self.logger, all_product_prices, all_cart_item_prices, "Product prices match cart item prices")
        assert all_product_prices == pytest.approx(all_cart_item_prices, rel=1e-9), (
            "The product prices in inventory do not match to item prices from cart page"
        )

        expected_cart_calc_prices = self.pages["cart_page"].get_list_of_cart_calc_prices()
        self.pages["cart_page"].click_checkout()
        first_name = self.data["generator"].first_name()
        last_name = self.data["generator"].last_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].fill_checkout_form(first_name, last_name, zip_code)
        self.pages["checkout_page"].click_continue_checkout()
        actual_overview_total_prices = self.pages["overview_page"].get_list_of_overview_total_prices()
        expected_overview_calc_prices = self.pages["overview_page"].get_list_of_overview_calc_prices()

        log_assertion(
            self.logger, expected_cart_calc_prices, actual_overview_total_prices, "Cart prices match overview prices"
        )
        assert expected_cart_calc_prices == pytest.approx(actual_overview_total_prices, rel=1e-9), (
            "The item prices from cart page does not match to item price from overview page"
        )

        log_assertion(
            self.logger,
            expected_overview_calc_prices,
            actual_overview_total_prices,
            "Overview calc prices match total prices",
        )
        assert expected_overview_calc_prices == pytest.approx(actual_overview_total_prices, rel=1e-9), (
            "The item prices from overview page does not match to total_prices from overview page"
        )

        self.pages["overview_page"].click_finish_overview()
        expected_cart_item_count_not_exist = self.pages["order_page"].check_cart_count_not_exist()

        self.logger.info(f"Cart count not exist: {expected_cart_item_count_not_exist}")
        assert expected_cart_item_count_not_exist is True, "The cart contains items"

        log_test_end(self.logger, "test_purchase_all_item", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_add_to_cart(self, username, password):
        """Test adding and removing products from cart"""
        log_test_start(self.logger, "test_add_to_cart", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        all_product_elements = self.pages["inventory_page"].get_all_product_elements()
        self.pages["inventory_page"].add_all_to_cart()
        actual_cart_item_count = self.pages["inventory_page"].get_cart_item_count()
        expected_cart_item_count = len(all_product_elements)

        log_assertion(self.logger, expected_cart_item_count, actual_cart_item_count, "Cart contains all products")
        assert expected_cart_item_count == actual_cart_item_count, "The cart does not contain all products"

        self.pages["inventory_page"].remove_all_from_cart()
        expected_cart_item_count_not_exist = self.pages["inventory_page"].check_cart_count_not_exist()

        self.logger.info(f"Cart count not exist: {expected_cart_item_count_not_exist}")
        assert expected_cart_item_count_not_exist is True, "The cart contains items"

        log_test_end(self.logger, "test_add_to_cart", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_sort_a_to_z(self, username, password):
        """Test sorting products alphabetically A to Z"""
        log_test_start(self.logger, "test_sort_a_to_z", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].sort_products_a_to_z()
        all_product_names = self.pages["inventory_page"].get_list_of_product_names()

        self.logger.info(f"Product names: {all_product_names}")
        for i in range(len(all_product_names) - 1):
            assert all_product_names[i] <= all_product_names[i + 1], (
                f"Products {all_product_names[i]} and {all_product_names[i + 1]} are not ordered correctly."
            )

        log_test_end(self.logger, "test_sort_a_to_z", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_sort_z_to_a(self, username, password):
        """Test sorting products alphabetically Z to A"""
        log_test_start(self.logger, "test_sort_z_to_a", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].sort_products_z_to_a()
        all_product_names = self.pages["inventory_page"].get_list_of_product_names()

        self.logger.info(f"Product names: {all_product_names}")
        for i in range(len(all_product_names) - 1):
            assert all_product_names[i] >= all_product_names[i + 1], (
                f"Products {all_product_names[i]} and {all_product_names[i + 1]} are not ordered correctly."
            )

        log_test_end(self.logger, "test_sort_z_to_a", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_sort_low_to_high(self, username, password):
        """Test sorting products by price low to high"""
        log_test_start(self.logger, "test_sort_low_to_high", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].sort_products_low_to_high()
        all_product_prices = self.pages["inventory_page"].get_list_of_product_prices()

        self.logger.info(f"Product prices: {all_product_prices}")
        for i in range(len(all_product_prices) - 1):
            assert all_product_prices[i] <= all_product_prices[i + 1], (
                f"Products {all_product_prices[i]} and {all_product_prices[i + 1]} are not ordered correctly."
            )

        log_test_end(self.logger, "test_sort_low_to_high", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_sort_high_to_low(self, username, password):
        """Test sorting products by price high to low"""
        log_test_start(self.logger, "test_sort_high_to_low", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].sort_products_high_to_low()
        all_product_prices = self.pages["inventory_page"].get_list_of_product_prices()

        self.logger.info(f"Product prices: {all_product_prices}")
        for i in range(len(all_product_prices) - 1):
            assert all_product_prices[i] >= all_product_prices[i + 1], (
                f"Products {all_product_prices[i]} and {all_product_prices[i + 1]} are not ordered correctly."
            )

        log_test_end(self.logger, "test_sort_high_to_low", "PASSED")

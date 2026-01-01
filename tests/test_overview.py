import pytest

from data.tests_data import InventoryPage, Links, OrderPage, OverviewPage, Users
from tests.test_base import BaseTest
from utils.logger import get_logger, log_assertion, log_test_end, log_test_start


class TestOverview(BaseTest):
    """Overview page tests"""

    logger = get_logger(__name__)

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, OverviewPage.OVERVIEW_TITLE, Links.OVERVIEW),
        ],
    )
    def test_open_overview(self, username, password, expected_title, expected_url):
        """Test opening overview page"""
        log_test_start(self.logger, "test_open_overview", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        first_name = self.data["generator"].first_name()
        last_name = self.data["generator"].last_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].fill_checkout_form(first_name, last_name, zip_code)
        self.pages["checkout_page"].click_continue_checkout()
        actual_overview_title = self.pages["overview_page"].get_overview_page_title()
        expected_overview_title = expected_title
        actual_overview_url = self.pages["overview_page"].action_get_url()
        expected_overview_url = expected_url

        log_assertion(self.logger, expected_overview_title, actual_overview_title, "Overview title validation")
        assert expected_overview_title == actual_overview_title, (
            f"The actual title '{actual_overview_title}' does not match the expected title '{expected_overview_title}'"
        )

        log_assertion(self.logger, expected_overview_url, actual_overview_url, "Overview URL validation")
        assert expected_overview_url == actual_overview_url, (
            f"The actual url '{actual_overview_url}' does not match the expected url '{expected_overview_url}'"
        )

        log_test_end(self.logger, "test_open_overview", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, InventoryPage.PRODUCTS_TITLE, Links.PRODUCTS),
        ],
    )
    def test_cancel_overview(self, username, password, expected_title, expected_url):
        """Test cancel button from overview page"""
        log_test_start(self.logger, "test_cancel_overview", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        first_name = self.data["generator"].first_name()
        last_name = self.data["generator"].last_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].fill_checkout_form(first_name, last_name, zip_code)
        self.pages["checkout_page"].click_continue_checkout()
        self.pages["overview_page"].click_cancel_overview()
        actual_title_after_cancel_overview = self.pages["inventory_page"].get_products_page_title()
        expected_title_after_cancel_overview = expected_title
        actual_url_after_cancel_overview = self.pages["inventory_page"].action_get_url()
        expected_url_after_cancel_overview = expected_url

        log_assertion(
            self.logger,
            expected_title_after_cancel_overview,
            actual_title_after_cancel_overview,
            "Title after cancel validation",
        )
        assert expected_title_after_cancel_overview == actual_title_after_cancel_overview, (
            f"The actual title '{actual_title_after_cancel_overview}' does not match the expected title '{expected_title_after_cancel_overview}'"
        )

        log_assertion(
            self.logger,
            expected_url_after_cancel_overview,
            actual_url_after_cancel_overview,
            "URL after cancel validation",
        )
        assert expected_url_after_cancel_overview == actual_url_after_cancel_overview, (
            f"The actual url '{actual_url_after_cancel_overview}' does not match the expected url '{expected_url_after_cancel_overview}'"
        )

        log_test_end(self.logger, "test_cancel_overview", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, OrderPage.ORDER_TITLE, Links.ORDER),
        ],
    )
    def test_finish_overview(self, username, password, expected_title, expected_url):
        """Test finish button completes order"""
        log_test_start(self.logger, "test_finish_overview", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        first_name = self.data["generator"].first_name()
        last_name = self.data["generator"].last_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].fill_checkout_form(first_name, last_name, zip_code)
        self.pages["checkout_page"].click_continue_checkout()
        self.pages["overview_page"].click_finish_overview()
        actual_title_after_finish_overview = self.pages["order_page"].get_order_page_title()
        expected_title_after_finish_overview = expected_title
        actual_url_after_finish_overview = self.pages["order_page"].action_get_url()
        expected_url_after_finish_overview = expected_url

        log_assertion(
            self.logger,
            expected_title_after_finish_overview,
            actual_title_after_finish_overview,
            "Order title validation",
        )
        assert expected_title_after_finish_overview == actual_title_after_finish_overview, (
            f"The actual title '{actual_title_after_finish_overview}' does not match the expected title '{expected_title_after_finish_overview}'"
        )

        log_assertion(
            self.logger, expected_url_after_finish_overview, actual_url_after_finish_overview, "Order URL validation"
        )
        assert expected_url_after_finish_overview == actual_url_after_finish_overview, (
            f"The actual url '{actual_url_after_finish_overview}' does not match the expected url '{expected_url_after_finish_overview}'"
        )

        log_test_end(self.logger, "test_finish_overview", "PASSED")

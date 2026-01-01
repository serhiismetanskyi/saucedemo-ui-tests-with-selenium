import pytest

from data.tests_data import CartPage, CheckoutPage, Errors, Links, OverviewPage, Users
from tests.test_base import BaseTest
from utils.logger import get_logger, log_assertion, log_test_end, log_test_start


class TestCheckout(BaseTest):
    """Checkout page tests"""

    logger = get_logger(__name__)

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, CheckoutPage.CHECKOUT_TITLE, Links.CHECKOUT)],
    )
    def test_open_checkout(self, username, password, expected_title, expected_url):
        """Test opening checkout page"""
        log_test_start(self.logger, "test_open_checkout", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        actual_checkout_title = self.pages["checkout_page"].get_checkout_page_title()
        expected_checkout_title = expected_title
        actual_checkout_url = self.pages["checkout_page"].action_get_url()
        expected_checkout_url = expected_url

        log_assertion(self.logger, expected_checkout_title, actual_checkout_title, "Checkout title validation")
        assert expected_checkout_title == actual_checkout_title, (
            f"The actual title '{actual_checkout_title}' does not match the expected title '{expected_checkout_title}'"
        )

        log_assertion(self.logger, expected_checkout_url, actual_checkout_url, "Checkout URL validation")
        assert expected_checkout_url == actual_checkout_url, (
            f"The actual url '{actual_checkout_url}' does not match the expected url '{expected_checkout_url}'"
        )

        log_test_end(self.logger, "test_open_checkout", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, CartPage.CART_TITLE, Links.CART)],
    )
    def test_cancel_checkout(self, username, password, expected_title, expected_url):
        """Test cancel checkout button"""
        log_test_start(self.logger, "test_cancel_checkout", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        self.pages["checkout_page"].click_cancel_checkout()
        actual_title_after_cancel_checkout = self.pages["cart_page"].get_cart_page_title()
        expected_title_after_cancel_checkout = expected_title
        actual_url_after_cancel_checkout = self.pages["cart_page"].action_get_url()
        expected_url_after_cancel_checkout = expected_url

        log_assertion(
            self.logger,
            expected_title_after_cancel_checkout,
            actual_title_after_cancel_checkout,
            "Title after cancel validation",
        )
        assert expected_title_after_cancel_checkout == actual_title_after_cancel_checkout, (
            f"The actual title '{actual_title_after_cancel_checkout}' does not match the expected title '{expected_title_after_cancel_checkout}'"
        )

        log_assertion(
            self.logger,
            expected_url_after_cancel_checkout,
            actual_url_after_cancel_checkout,
            "URL after cancel validation",
        )
        assert expected_url_after_cancel_checkout == actual_url_after_cancel_checkout, (
            f"The actual url '{expected_url_after_cancel_checkout}' does not match the expected url '{actual_url_after_cancel_checkout}'"
        )

        log_test_end(self.logger, "test_cancel_checkout", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_title, expected_url",
        [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, OverviewPage.OVERVIEW_TITLE, Links.OVERVIEW)],
    )
    def test_fill_checkout(self, username, password, expected_title, expected_url):
        """Test filling checkout form"""
        log_test_start(self.logger, "test_fill_checkout", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        check_form = self.pages["checkout_page"].check_checkout_form()

        self.logger.info(f"Checkout form check: {check_form}")
        assert check_form is True, "The checkout form does not contain all fields"

        first_name = self.data["generator"].first_name()
        last_name = self.data["generator"].last_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].fill_checkout_form(first_name, last_name, zip_code)

        self.logger.info(f"Filled form with: {first_name}, {last_name}, {zip_code}")
        assert self.pages["checkout_page"].get_first_name() == first_name, "The first name field does not contain value"
        assert self.pages["checkout_page"].get_last_name() == last_name, "The last name field does not contain value"
        assert self.pages["checkout_page"].get_zip_code() == zip_code, "The zip code field does not contain value"

        self.pages["checkout_page"].click_continue_checkout()
        actual_title_after_continue_checkout = self.pages["overview_page"].get_overview_page_title()
        expected_title_after_continue_checkout = expected_title
        actual_url_after_continue_checkout = self.pages["overview_page"].action_get_url()
        expected_url_after_continue_checkout = expected_url

        log_assertion(
            self.logger,
            expected_title_after_continue_checkout,
            actual_title_after_continue_checkout,
            "Overview title validation",
        )
        assert actual_title_after_continue_checkout == expected_title_after_continue_checkout, (
            f"The actual title '{actual_title_after_continue_checkout}' does not match the expected title '{expected_title_after_continue_checkout}'"
        )

        log_assertion(
            self.logger,
            expected_url_after_continue_checkout,
            actual_url_after_continue_checkout,
            "Overview URL validation",
        )
        assert actual_url_after_continue_checkout == expected_url_after_continue_checkout, (
            f"The actual url '{actual_url_after_continue_checkout}' does not match the expected url '{expected_url_after_continue_checkout}'"
        )

        log_test_end(self.logger, "test_fill_checkout", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, Errors.MANDATORY_FIRSTNAME)],
    )
    def test_mandatory_first_name(self, username, password, expected_message):
        """Test mandatory first name field"""
        log_test_start(self.logger, "test_mandatory_first_name", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        last_name = self.data["generator"].last_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].enter_last_name(last_name)
        self.pages["checkout_page"].enter_zip_code(zip_code)
        self.pages["checkout_page"].click_continue_checkout()
        actual_error_message_about_first_name = self.pages["checkout_page"].get_checkout_error_message()
        expected_error_message_about_first_name = expected_message

        log_assertion(
            self.logger,
            expected_error_message_about_first_name,
            actual_error_message_about_first_name,
            "Mandatory first name error validation",
        )
        assert expected_error_message_about_first_name == actual_error_message_about_first_name, (
            f"The actual error message '{actual_error_message_about_first_name}' does not match the expected error message '{expected_error_message_about_first_name}'"
        )

        log_test_end(self.logger, "test_mandatory_first_name", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, Errors.MANDATORY_LASTNAME)],
    )
    def test_mandatory_last_name(self, username, password, expected_message):
        """Test mandatory last name field"""
        log_test_start(self.logger, "test_mandatory_last_name", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        first_name = self.data["generator"].first_name()
        zip_code = self.data["generator"].zip_code()
        self.pages["checkout_page"].enter_first_name(first_name)
        self.pages["checkout_page"].enter_zip_code(zip_code)
        self.pages["checkout_page"].click_continue_checkout()
        actual_error_message_about_last_name = self.pages["checkout_page"].get_checkout_error_message()
        expected_error_message_about_last_name = expected_message

        log_assertion(
            self.logger,
            expected_error_message_about_last_name,
            actual_error_message_about_last_name,
            "Mandatory last name error validation",
        )
        assert expected_error_message_about_last_name == actual_error_message_about_last_name, (
            f"The actual error message '{actual_error_message_about_last_name}' does not match the expected error message '{expected_error_message_about_last_name}'"
        )

        log_test_end(self.logger, "test_mandatory_last_name", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, Errors.MANDATORY_ZIP)],
    )
    def test_mandatory_zip_code(self, username, password, expected_message):
        """Test mandatory zip code field"""
        log_test_start(self.logger, "test_mandatory_zip_code", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        first_name = self.data["generator"].first_name()
        last_name = self.data["generator"].last_name()
        self.pages["checkout_page"].enter_first_name(first_name)
        self.pages["checkout_page"].enter_last_name(last_name)
        self.pages["checkout_page"].click_continue_checkout()
        actual_error_message_about_zip_code = self.pages["checkout_page"].get_checkout_error_message()
        expected_error_message_about_zip_code = expected_message

        log_assertion(
            self.logger,
            expected_error_message_about_zip_code,
            actual_error_message_about_zip_code,
            "Mandatory zip code error validation",
        )
        assert expected_error_message_about_zip_code == actual_error_message_about_zip_code, (
            f"The actual error message '{actual_error_message_about_zip_code}' does not match the expected error message '{expected_error_message_about_zip_code}'"
        )

        log_test_end(self.logger, "test_mandatory_zip_code", "PASSED")

    @pytest.mark.parametrize("username, password", [(Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD)])
    def test_close_error_message(self, username, password):
        """Test closing error message"""
        log_test_start(self.logger, "test_close_error_message", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].open_cart_page()
        self.pages["cart_page"].click_checkout()
        self.pages["checkout_page"].click_continue_checkout()
        self.pages["checkout_page"].click_checkout_error_button()
        actual_error_message_not_exist = self.pages["checkout_page"].error_checkout_message_not_exist()
        expected_error_message_not_exist = True

        log_assertion(
            self.logger,
            expected_error_message_not_exist,
            actual_error_message_not_exist,
            "Error message closed validation",
        )
        assert expected_error_message_not_exist == actual_error_message_not_exist, (
            "The error message is existed on the page"
        )

        log_test_end(self.logger, "test_close_error_message", "PASSED")

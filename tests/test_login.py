import pytest

from data.tests_data import Errors, Links, Users
from tests.test_base import BaseTest
from utils.logger import get_logger, log_assertion, log_test_end, log_test_start


class TestLogin(BaseTest):
    logger = get_logger(__name__)

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            (Users.WRONG_USER_NAME, Users.WRONG_USER_PASSWORD, Errors.WRONG_LOGIN_MESSAGE),
        ],
    )
    def test_invalid_login(self, username, password, expected_message):
        """Test login with invalid credentials"""
        log_test_start(self.logger, "test_invalid_login", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        actual_error_message = self.pages["login_page"].get_login_error_message()
        expected_error_message = expected_message

        log_assertion(self.logger, expected_error_message, actual_error_message, "Error message validation")
        assert expected_error_message == actual_error_message, (
            f"The actual error message '{actual_error_message}' does not match the expected error message '{expected_error_message}'"
        )

        log_test_end(self.logger, "test_invalid_login", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, Links.PRODUCTS),
        ],
    )
    def test_valid_login(self, username, password, expected_url):
        """Test login with valid credentials"""
        log_test_start(self.logger, "test_valid_login", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        actual_url_after_login = self.pages["login_page"].action_get_url()
        expected_url_after_login = expected_url

        log_assertion(self.logger, expected_url_after_login, actual_url_after_login, "URL after login validation")
        assert expected_url_after_login == actual_url_after_login, (
            f"The actual url '{actual_url_after_login}' after logout does not match the expected url '{expected_url_after_login}'"
        )

        log_test_end(self.logger, "test_valid_login", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            (Users.LOCKED_USER_NAME, Users.LOCKED_USER_PASSWORD, Errors.LOCKED_LOGIN_MESSAGE),
        ],
    )
    def test_login_by_locked_user(self, username, password, expected_message):
        """Test login with locked user"""
        log_test_start(self.logger, "test_login_by_locked_user", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        actual_error_message = self.pages["login_page"].get_login_error_message()
        expected_error_message = expected_message

        log_assertion(self.logger, expected_error_message, actual_error_message, "Locked user error message validation")
        assert expected_error_message == actual_error_message, (
            f"The actual error message '{actual_error_message}' does not match the expected error message '{expected_error_message}'"
        )

        log_test_end(self.logger, "test_login_by_locked_user", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_url",
        [
            (Users.STANDARD_USER_NAME, Users.STANDARD_USER_PASSWORD, Links.BASE_URL),
        ],
    )
    def test_logout(self, username, password, expected_url):
        """Test logout functionality"""
        log_test_start(self.logger, "test_logout", {"username": username, "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["inventory_page"].logout()
        check_form = self.pages["login_page"].check_login_form()
        actual_url_after_logout = self.pages["login_page"].action_get_url()
        expected_url_after_logout = expected_url

        self.logger.info(f"Login form check result: {check_form}")
        assert check_form is True, "The login form does not contain all fields"

        log_assertion(self.logger, expected_url_after_logout, actual_url_after_logout, "URL after logout validation")
        assert expected_url_after_logout == actual_url_after_logout, (
            f"The actual url '{actual_url_after_logout}' after logout does not match the expected url '{expected_url_after_logout}'"
        )

        log_test_end(self.logger, "test_logout", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            (Users.STANDARD_USER_NAME, Users.EMPTY_STRING, Errors.MANDATORY_PASSWORD),
        ],
    )
    def test_mandatory_password(self, username, password, expected_message):
        """Test mandatory password field"""
        log_test_start(self.logger, "test_mandatory_password", {"username": username, "password": "empty"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["login_page"].click_login_button()
        actual_error_message_about_password = self.pages["login_page"].get_login_error_message()
        expected_error_message_about_password = expected_message

        log_assertion(
            self.logger,
            expected_error_message_about_password,
            actual_error_message_about_password,
            "Mandatory password error message validation",
        )
        assert expected_error_message_about_password == actual_error_message_about_password, (
            f"The actual error message '{actual_error_message_about_password}' does not match the expected error message '{expected_error_message_about_password}'"
        )

        log_test_end(self.logger, "test_mandatory_password", "PASSED")

    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            (Users.EMPTY_STRING, Users.STANDARD_USER_PASSWORD, Errors.MANDATORY_USERNAME),
        ],
    )
    def test_mandatory_username(self, username, password, expected_message):
        """Test mandatory username field"""
        log_test_start(self.logger, "test_mandatory_username", {"username": "empty", "password": "***"})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].login(username, password)
        self.pages["login_page"].click_login_button()
        actual_error_message_about_username = self.pages["login_page"].get_login_error_message()
        expected_error_message_about_username = expected_message

        log_assertion(
            self.logger,
            expected_error_message_about_username,
            actual_error_message_about_username,
            "Mandatory username error message validation",
        )
        assert expected_error_message_about_username == actual_error_message_about_username, (
            f"The actual error message '{actual_error_message_about_username}' does not match the expected error message '{expected_error_message_about_username}'"
        )

        log_test_end(self.logger, "test_mandatory_username", "PASSED")

    def test_close_error_message(self):
        """Test closing error message"""
        log_test_start(self.logger, "test_close_error_message", {})

        self.pages["login_page"].open_login_page()
        self.pages["login_page"].click_login_button()
        self.pages["login_page"].click_login_error_button()
        actual_error_message_not_exist = self.pages["login_page"].error_login_message_not_exist()
        expected_error_message_not_exist = True

        log_assertion(
            self.logger,
            expected_error_message_not_exist,
            actual_error_message_not_exist,
            "Error message should be closed",
        )
        assert expected_error_message_not_exist == actual_error_message_not_exist, (
            "The error message is existed on the page"
        )

        log_test_end(self.logger, "test_close_error_message", "PASSED")

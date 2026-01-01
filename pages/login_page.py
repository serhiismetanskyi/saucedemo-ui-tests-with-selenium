from locators.page_locators import LoginPageLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    login_page = LoginPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    def open_login_page(self) -> None:
        """Open login page"""
        self.logger.info("Opening login page")
        self.init_site()

    def enter_password(self, password) -> None:
        """Enter password in login form"""
        self.logger.info(f"Entering password: {'*' * len(str(password))}")
        self.action_fill_text(self.element_is_visible(self.login_page.PASSWORD), password)

    def enter_username(self, username) -> None:
        """Enter username in login form"""
        self.logger.info(f"Entering username: {username}")
        self.action_fill_text(self.element_is_visible(self.login_page.USERNAME), username)

    def click_login_button(self) -> None:
        """Click login button"""
        self.logger.info("Clicking login button")
        self.action_left_click(self.element_is_visible(self.login_page.LOGIN_BUTTON))

    def login(self, username: str, password: str) -> None:
        """Perform login with credentials"""
        self.logger.info(f"Login attempt: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def clear_username(self) -> None:
        """Clear username field"""
        self.action_clear_text(self.element_is_visible(self.login_page.USERNAME))

    def clear_password(self) -> None:
        """Clear password field"""
        self.action_clear_text(self.element_is_visible(self.login_page.PASSWORD))

    def clear_login_form(self) -> None:
        """Clear all login form fields"""
        self.clear_username()
        self.clear_password()

    def check_login_form(self) -> bool:
        """Check if login form is displayed"""
        username = self.element_is_visible(self.login_page.USERNAME)
        password = self.element_is_visible(self.login_page.PASSWORD)
        login_button = self.element_is_visible(self.login_page.LOGIN_BUTTON)
        return username is not None and password is not None and login_button is not None

    def error_login_message_exists(self) -> bool:
        """Check if error message is visible"""
        error_message = self.element_is_visible(self.login_page.ERROR_MESSAGE)
        return error_message is not None

    def error_login_message_not_exist(self) -> bool:
        """Check if error message is not visible"""
        return self.element_is_not_visible(self.login_page.ERROR_MESSAGE)

    def get_login_error_message(self) -> str | None:
        """Get login error message text"""
        if self.error_login_message_exists():
            error_message = self.action_get_text(self.login_page.ERROR_MESSAGE)
            self.logger.info(f"Error: {error_message}")
            return error_message
        self.logger.info("No error message")
        return None

    def click_login_error_button(self) -> None:
        """Click error message close button"""
        self.action_left_click(self.element_is_visible(self.login_page.ERROR_BUTTON))

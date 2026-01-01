from locators.page_locators import CheckoutPageLocators
from pages.cart_page import CartPage


class CheckoutPage(CartPage):
    checkout = CheckoutPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    def get_checkout_page_title(self) -> str:
        """Get checkout page title"""
        return self.action_get_text(self.checkout.PAGE_TITLE)

    def enter_first_name(self, first_name) -> None:
        """Enter first name"""
        self.action_fill_text(self.element_is_visible(self.checkout.FIRST_NAME), first_name)

    def enter_last_name(self, last_name) -> None:
        """Enter last name"""
        self.action_fill_text(self.element_is_visible(self.checkout.LAST_NAME), last_name)

    def enter_zip_code(self, zip_code) -> None:
        """Enter zip code"""
        self.action_fill_text(self.element_is_visible(self.checkout.ZIP_CODE), zip_code)

    def fill_checkout_form(self, first_name: str, last_name: str, zip_code: int) -> None:
        """Fill all checkout form fields"""
        self.logger.info(f"Filling checkout form: {first_name} {last_name}, {zip_code}")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_zip_code(zip_code)

    def check_checkout_form(self) -> bool:
        """Check if checkout form is displayed"""
        first_name = self.element_is_visible(self.checkout.FIRST_NAME)
        last_name = self.element_is_visible(self.checkout.LAST_NAME)
        zip_code = self.element_is_visible(self.checkout.ZIP_CODE)
        return first_name is not None and last_name is not None and zip_code is not None

    def get_first_name(self) -> str:
        """Get first name value"""
        return self.action_get_attr(self.checkout.FIRST_NAME, "value")

    def get_last_name(self) -> str:
        """Get last name value"""
        return self.action_get_attr(self.checkout.LAST_NAME, "value")

    def get_zip_code(self) -> str:
        """Get zip code value"""
        return self.action_get_attr(self.checkout.ZIP_CODE, "value")

    def clear_first_name(self) -> None:
        """Clear first name field"""
        self.action_clear_text(self.element_is_visible(self.checkout.FIRST_NAME))

    def clear_last_name(self) -> None:
        """Clear last name field"""
        self.action_clear_text(self.element_is_visible(self.checkout.LAST_NAME))

    def clear_zip_code(self) -> None:
        """Clear zip code field"""
        self.action_clear_text(self.element_is_visible(self.checkout.ZIP_CODE))

    def clear_checkout_form(self) -> None:
        """Clear all checkout form fields"""
        self.clear_first_name()
        self.clear_last_name()
        self.clear_zip_code()

    def error_checkout_message_exists(self) -> bool:
        """Check if error message exists"""
        error_message = self.element_is_visible(self.checkout.ERROR_MESSAGE)
        return error_message is not None

    def error_checkout_message_not_exist(self) -> bool:
        """Check if error message doesn't exist"""
        error_message = self.element_is_not_visible(self.checkout.ERROR_MESSAGE)
        return error_message

    def get_checkout_error_message(self) -> str | None:
        """Get checkout error message text"""
        if self.error_checkout_message_exists():
            return self.action_get_text(self.checkout.ERROR_MESSAGE)
        return None

    def click_checkout_error_button(self) -> None:
        """Click error close button"""
        self.action_left_click(self.element_is_visible(self.checkout.ERROR_BUTTON))

    def click_cancel_checkout(self) -> None:
        """Click cancel button"""
        self.logger.info("Clicking cancel")
        self.action_left_click(self.element_is_visible(self.checkout.CANCEL_BUTTON))

    def click_continue_checkout(self) -> None:
        """Click continue button"""
        self.logger.info("Clicking continue")
        self.action_left_click(self.element_is_visible(self.checkout.CONTINUE_BUTTON))

import os

from dotenv import load_dotenv

load_dotenv()


class Links:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
    PRODUCTS = os.getenv("PRODUCTS", "https://www.saucedemo.com/inventory.html")
    PRODUCT = os.getenv("PRODUCT", "https://www.saucedemo.com/inventory-item.html?id=0")
    CART = os.getenv("CART", "https://www.saucedemo.com/cart.html")
    CHECKOUT = os.getenv("CHECKOUT", "https://www.saucedemo.com/checkout-step-one.html")
    OVERVIEW = os.getenv("OVERVIEW", "https://www.saucedemo.com/checkout-step-two.html")
    ORDER = os.getenv("ORDER", "https://www.saucedemo.com/checkout-complete.html")


class Users:
    STANDARD_USER_NAME = os.getenv("STANDARD_USER_NAME", "standard_user")
    STANDARD_USER_PASSWORD = os.getenv("STANDARD_USER_PASSWORD", "secret_sauce")

    WRONG_USER_NAME = os.getenv("WRONG_USER_NAME", "wrong_user")
    WRONG_USER_PASSWORD = os.getenv("WRONG_USER_PASSWORD", "secret_sauce")

    LOCKED_USER_NAME = os.getenv("LOCKED_USER_NAME", "locked_out_user")
    LOCKED_USER_PASSWORD = os.getenv("LOCKED_USER_PASSWORD", "secret_sauce")

    EMPTY_STRING = ""


class Errors:
    WRONG_LOGIN_MESSAGE = "Epic sadface: Username and password do not match any user in this service"
    LOCKED_LOGIN_MESSAGE = "Epic sadface: Sorry, this user has been locked out."
    MANDATORY_USERNAME = "Epic sadface: Username is required"
    MANDATORY_PASSWORD = "Epic sadface: Password is required"
    MANDATORY_FIRSTNAME = "Error: First Name is required"
    MANDATORY_LASTNAME = "Error: Last Name is required"
    MANDATORY_ZIP = "Error: Postal Code is required"


class LoginPage:
    pass


class InventoryPage:
    HAMBURGER_MENU_LIST = ["All Items", "About", "Logout", "Reset App State"]
    PRODUCTS_TITLE = "Products"


class ProductPage:
    pass


class CartPage:
    CART_TITLE = "Your Cart"


class CheckoutPage:
    CHECKOUT_TITLE = "Checkout: Your Information"


class OverviewPage:
    OVERVIEW_TITLE = "Checkout: Overview"


class OrderPage:
    ORDER_TITLE = "Checkout: Complete!"
    ORDER_SUBTITLE = "Thank you for your order!"
    ORDER_TEXT = "Your order has been dispatched, and will arrive just as fast as the pony can get there!"

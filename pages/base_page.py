from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait

from data.tests_data import Links
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.url = Links.BASE_URL
        self.wait = WebDriverWait(self.driver, 15, 0.3)
        self.logger = get_logger(self.__class__.__name__)

    def init_site(self) -> None:
        """Open base URL"""
        self.logger.info(f"Opening base URL: {self.url}")
        self.driver.get(self.url)

    def open_url(self, url) -> None:
        """Open specific URL"""
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def element_is_visible(self, element) -> WebElement:
        """Wait for element to be visible"""
        self.logger.debug(f"Waiting for element to be visible: {element}")
        self.go_to_element(self.element_is_present(element))
        return self.wait.until(expected.visibility_of_element_located(element))

    def elements_are_visible(self, element) -> list[WebElement]:
        """Get all visible elements"""
        self.logger.debug(f"Getting all visible elements: {element}")
        return self.wait.until(expected.visibility_of_all_elements_located(element))

    def element_is_present(self, element) -> WebElement:
        """Wait for element to be present in DOM"""
        self.logger.debug(f"Waiting for element to be present: {element}")
        return self.wait.until(expected.presence_of_element_located(element))

    def elements_are_present(self, element) -> list[WebElement]:
        """Get all present elements"""
        self.logger.debug(f"Getting all present elements: {element}")
        return self.wait.until(expected.presence_of_all_elements_located(element))

    def element_is_not_visible(self, element) -> bool:
        """Check if element is not visible"""
        self.logger.debug(f"Checking element is not visible: {element}")
        return self.wait.until(expected.invisibility_of_element_located(element))

    def element_is_clickable(self, element) -> WebElement:
        """Wait for element to be clickable"""
        self.logger.debug(f"Waiting for element to be clickable: {element}")
        return self.wait.until(expected.element_to_be_clickable(element))

    def scroll_to_bottom(self) -> None:
        """Scroll page to bottom"""
        self.logger.debug("Scrolling to bottom of page")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def go_to_element(self, element) -> None:
        """Scroll to element"""
        self.logger.debug("Scrolling to element")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def action_double_click(self, element) -> None:
        """Perform double click"""
        self.logger.debug("Performing double click")
        action = ActionChains(self.driver)
        self.highlight_element(element, "green")
        action.double_click(element)
        action.perform()

    def action_right_click(self, element) -> None:
        """Perform right click"""
        self.logger.debug("Performing right click")
        action = ActionChains(self.driver)
        self.highlight_element(element, "green")
        action.context_click(element)
        action.perform()

    def action_left_click(self, element) -> None:
        """Perform left click"""
        self.logger.debug("Performing left click")
        action = ActionChains(self.driver)
        self.highlight_element(element, "green")
        action.click(element)
        action.perform()

    def action_left_click_on_elements(self, elements: list) -> None:
        """Click on multiple elements"""
        self.logger.debug(f"Clicking on {len(elements)} elements")
        for element in elements:
            self.action_left_click(element)

    def action_fill_text(self, element, txt: str) -> None:
        """Fill text into element"""
        self.logger.debug(f"Filling text: '{txt}'")
        element: WebElement = self.wait.until(expected.element_to_be_clickable(element))
        element.clear()
        self.highlight_element(element, "green")
        element.send_keys(txt)

    def action_clear_text(self, element) -> None:
        """Clear text from element"""
        self.logger.debug("Clearing text from element")
        element: WebElement = self.wait.until(expected.element_to_be_clickable(element))
        self.highlight_element(element, "green")
        element.clear()

    def action_get_text(self, element) -> str:
        """Get element text"""
        element: WebElement = self.wait.until(expected.visibility_of_element_located(element))
        self.highlight_element(element, "green")
        text = element.text
        self.logger.debug(f"Got text: '{text}'")
        return text

    def action_get_text_from_elements(self, elements: list[WebElement]) -> list[str]:
        """Get text from multiple elements"""
        self.logger.debug(f"Getting text from {len(elements)} elements")
        return [element.text for element in elements]

    def get_element_by_text(self, elements: list[WebElement], name: str) -> WebElement:
        """Find element by text content"""
        self.logger.debug(f"Finding element by text: '{name}'")
        name = name.lower()
        return [element for element in elements if element.text.lower() == name][0]

    def action_get_attr(self, element, attribute) -> str:
        """Get element attribute"""
        self.logger.debug(f"Getting attribute '{attribute}' from element")
        element: WebElement = self.wait.until(expected.visibility_of_element_located(element))
        self.highlight_element(element, "green")
        return element.get_attribute(attribute)

    def action_get_attr_from_elements(self, elements: list[WebElement], attribute) -> list[str]:
        """Get attribute from multiple elements"""
        self.logger.debug(f"Getting attribute '{attribute}' from {len(elements)} elements")
        return [element.get_attribute(attribute) for element in elements]

    def action_get_url(self) -> str:
        """Get current page URL"""
        pages_url = self.driver.current_url
        self.logger.debug(f"Current URL: {pages_url}")
        return pages_url

    def action_drag_and_drop_by_offset(self, element, x_coords, y_coords) -> None:
        """Drag and drop element by offset"""
        self.logger.debug(f"Dragging element by offset: x={x_coords}, y={y_coords}")
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, x_coords, y_coords)
        action.perform()

    def action_drag_and_drop_to_element(self, what, where) -> None:
        """Drag and drop element to another element"""
        self.logger.debug("Dragging element to another element")
        action = ActionChains(self.driver)
        action.drag_and_drop(what, where)
        action.perform()

    def action_move_to_element(self, element) -> None:
        """Move cursor to element"""
        self.logger.debug("Moving cursor to element")
        action = ActionChains(self.driver)
        self.wait.until(expected.visibility_of(element))
        action.move_to_element(element)
        action.perform()

    def highlight_element(self, element, color: str) -> None:
        """Highlight element with color"""
        original_style = element.get_attribute("style")
        new_style = f"background-color: {color}; border: 1px solid #000; {original_style}"
        self.driver.execute_script(
            "var tmpArguments = arguments;setTimeout(function () {tmpArguments[0].setAttribute('style', '"
            + new_style
            + "');},0);",
            element,
        )
        self.driver.execute_script(
            "var tmpArguments = arguments;setTimeout(function () {tmpArguments[0].setAttribute('style', '"
            + original_style
            + "');},400);",
            element,
        )

    def find_value_in_data(self, value, data: list) -> bool:
        """Check if value exists in data"""
        self.logger.debug(f"Checking if value '{value}' exists in data")
        return value in data

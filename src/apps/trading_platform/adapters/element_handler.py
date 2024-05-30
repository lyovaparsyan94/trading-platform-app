import logging
from collections.abc import Callable
from time import sleep
from typing import Any

from selenium.common.exceptions import (
    ElementNotSelectableException,
    ElementNotVisibleException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger('element_handler')


class ElementHandler:
    def __init__(self, driver) -> None:
        """
        Initialize an ElementHandler instance.

        Args:
            driver: The Selenium WebDriver instance.
        """
        self.driver = driver

    def wait_for_element(self, locator: str, by_type: str = By.XPATH, timeout: int = 30, poll_frequency: float = 0.5,
                         name: str = ''):
        """
        Wait for an element to become visible.

        Args:
            locator (str): The locator string (e.g., XPath) of the element.
            by_type (str, optional): The type of locator (default is By.XPATH).
            timeout (int, optional): Maximum time to wait for the element (default is 30 seconds).
            poll_frequency (float, optional): Polling frequency (default is 0.5 seconds).
            name (str, optional): Name of the element for logging purposes.

        Returns:
            WebElement: The located element.
        """
        element = None
        self.driver.implicitly_wait(0)
        try:
            wait = WebDriverWait(self.driver, timeout=timeout, ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException, StaleElementReferenceException,
                ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))
        except Exception:
            logger.info(f"Element '{name}' NOT appeared ")
        return element

    def is_element_present(self, locator: str, by_type: str = By.XPATH, name: str = '') -> bool:
        """
        Check if an element is present on the page.

        Args:
            locator (str): The locator string (e.g., XPath) of the element.
            by_type (str, optional): The type of locator (default is 'xpath').
            name (str, optional): Name of the element for logging purposes.

        Returns:
            bool: True if the element is present, False otherwise.
        """
        try:
            element = self.driver.find_element(by_type, locator)
            if element is not None:
                return True
            return False
        except NoSuchElementException:
            logger.info(f"Element '{name}'  not found {name}")
            return False
        except Exception:
            logger.info(f"Unknown error '{name}'")
            return False

    def is_shown_warning(self, warning_xpath: str = '', name: str = None) -> bool:
        """
        Check if a warning element is displayed.

        Args:
            warning_xpath (str, optional): The XPath of the warning element (default is '').
            name (str, optional): Name of the warning element for logging purposes.

        Returns:
            bool: True if the warning element is displayed, False otherwise.
        """
        if warning_xpath is None:
            return True
        try:
            self.driver.implicitly_wait(3)
            element = self.driver.find_element(By.XPATH, warning_xpath)
            if element.is_displayed():
                return True
            logger.info(f"The warning element '{name}' is showing")
            return False
        except Exception:
            logger.info(f"The warning element '{name}' not shown")
            return False

    @staticmethod
    def wait_for_result(func: Callable[..., Any], period: int = 60, interval: int = 4) -> Callable[..., Any]:
        """
        Decorator that waits for a result from the given function.

        Args:
            func (Callable[..., Any]): The function to be wrapped.
            period (int, optional): Total waiting time in seconds. Defaults to 60.
            interval (int, optional): Time between retries in seconds. Defaults to 4.

        Returns:
            Callable[..., Any]: The wrapped function with retry logic.
        """

        def wrapper(self, *args, **kwargs) -> Callable:
            """
            Wrapper function that adds retry logic to the original function.

            Args:
                self: Instance of the class.
                *args: Positional arguments for the original function.
                **kwargs: Keyword arguments for the original function.

            Returns:
                Any: Result of the original function or None if timed out.
            """
            for i in range(period):
                logger.info(f"waiting for message from: {func.__name__}")
                result = func(self, *args, **kwargs)
                if result:
                    logger.info(f"function {func.__name__} completed with result: {result}")
                    return result
                if kwargs.get('old_codes', False):
                    logger.info("comparing with old_codes..")
                    return result
                sleep(interval)
            logger.info(f"Timed out waiting for {func.__name__}")

        return wrapper

    def highlight(self, *elements, color: str = 'yellow', show_time: int = 1) -> None:
        """
        Highlights (blinks) multiple Selenium WebDriver elements.

        Args:
            *elements (WebElement): Variable-length argument list of elements to highlight.
            color (str, optional): The desired background color (e.g., 'yellow', 'cyan', etc.). Defaults to 'yellow'.
            show_time (int, optional): The duration (in seconds) to keep the highlight. Defaults to 1.

        Notes:
            - The original styles of the elements are preserved.
            - After the specified time, the elements are restored to their original styles.
        """

        original_styles = [elem.get_attribute('style') for elem in elements]
        for elem in elements:
            self.apply_style(f"background: {color}; border: 3px solid red;", elem)

        sleep(show_time)
        for elem, orig_style in zip(elements, original_styles):
            self.apply_style(orig_style, elem)

    def apply_style(self, css_style: str, elem) -> None:
        """
        Applies the specified CSS style to the given element.

        Args:
            css_style (str): The CSS style to apply.
            elem (WebElement): The element to modify.
        """
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", elem, css_style)

    def slow_input(self, field_to_fill, sequence: str) -> None:
        """
        Slowly input a sequence of characters into a field.

        Args:
            field_to_fill: The input field element.
            sequence (str): The sequence of characters to input.

        Returns:
            None
        """
        for symbol in sequence:
            field_to_fill.send_keys(symbol)
            sleep(0.10)
        logger.info(f'filled {sequence}')

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from src.constants import SelEnum, Condition
from src.logger import prwarn, prerror

def wait_for(c: Condition, wait: WebDriverWait, sel: SelEnum) -> WebElement | None:
    """
    Wait for a selector to satisfy the given condition and return the WebElement.

    Args:
        condition: LocatorEnum type
        wait: WebDriverWait instance
        selector: SelEnum element

    Returns:
        WebElement if found, otherwise None
    """
    try:
        return wait.until(c.value(sel))
    except TimeoutException:
        prwarn(f"Timeout while waiting for {sel}")
        return None
    except Exception as e:
        prerror(f"Error while waiting for {sel}: {e}")
        return None

def find(driver, selector: SelEnum, multiple=False) -> WebElement | list[WebElement] | None:
    """
    Find an element and return it. 
    
    Returns:
        WebElement | list[WebElement] or None if not found
    """
    try:
        if multiple:
            return driver.find_elements(*selector)
        return driver.find_element(*selector)
    except NoSuchElementException:
        return None

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from src.constants import SelEnum, LocatorEnum
from src.logger import prwarn, prerror

def wait_for(condition: LocatorEnum, wait: WebDriverWait, selector: SelEnum) -> WebElement | None:
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
        return wait.until(condition.value(selector))
    except TimeoutException:
        prwarn(f"Timeout while waiting for {selector}")
        return None
    except Exception as e:
        prerror(f"Error while waiting for {selector}: {e}")
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

from selenium.common.exceptions import TimeoutException, \
    NoSuchElementException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from typing import Literal, overload

from src.constants import SelEnum
from src.logger import prdebug, prerror

def wait_for(
    c, 
    wait: WebDriverWait, 
    sel: SelEnum
) -> WebElement | None:
    """
    Wait for a selector to satisfy the given condition 
    and return the WebElement.

    Args:
        condition: Condition function
        wait: WebDriverWait instance
        selector: SelEnum element

    Returns:
        WebElement if found, otherwise None
    """
    try:
        return wait.until(c(sel))
    except TimeoutException:
        prdebug(f"Timeout while waiting for {sel}")
    except WebDriverException as e:
        prerror(f"Driver error while waiting for {sel}: {e}")
    
    return None

@overload
def find(
    driver,
    sel: SelEnum | tuple[str, str],
    *,
    multiple: Literal[True]
) -> list[WebElement]: ...
@overload
def find(
    driver,
    sel: SelEnum | tuple[str, str],
    *,
    multiple: Literal[False] = False
) -> WebElement | None: ...
def find(
    driver: WebDriver | WebElement,
    sel: SelEnum | tuple[str, str],
    *,
    multiple: bool = False
) -> WebElement | None | list[WebElement]:
    """
    Find an element and return it.
    Also supports finding multiple elements. 

    Args:
        driver: WebDriver or WebElement instance
        sel: SelEnum element or tuple
        multiple: bool
    
    Returns:
        Optional[WebElement] | List[WebElement]
    """
    try:
        if multiple:
            return driver.find_elements(*sel)
        return driver.find_element(*sel)

    except (NoSuchElementException, StaleElementReferenceException):
        prdebug(f"Element not found: {sel}")
        
    except WebDriverException as e:
        prerror(f"Driver error while finding element {sel}: {e}")
    
    return [] if multiple else None

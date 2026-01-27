import traceback
import time
import random
import re
import functools

from selenium.webdriver.support.ui import WebDriverWait
from difflib import SequenceMatcher
from pathlib import Path
from selenium.webdriver.remote.webelement import WebElement
from typing import overload, Literal
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidElementStateException,
)

from src.constants import SwalSelectors, Condition
from src.locators import wait_for, find
from src.logger import prerror, prdebug
from src.models import Swal
from src.config import CONFIG

def handle_exceptions(default=None):
    """
    A decorator that catches and logs any exceptions then returns a default value.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                tb = traceback.format_exc()
                prdebug(f"Exception in {func.__name__}: {e}\n{tb}")
                return default
        return wrapper
    return decorator

@overload
def parse_num(el: WebElement | str | None, is_percent: Literal[True]) -> float | None: ...
@overload
def parse_num(el: WebElement | str | None, is_percent: Literal[False] = False) -> int | None: ...
def parse_num(el: WebElement | str | None, is_percent: bool = False) -> int | float | None:
    if el:
        string = el.text.strip() if isinstance(el, WebElement) else el.strip()
        num = re.search(r'\d+', string)
        if num:
            res = int(num.group())
            if is_percent:
                res = float(res) / 100
            return res
    return None

def parse_text(el: WebElement | str | None) -> str | None:
    if el:
        return el.text.strip() if isinstance(el, WebElement) else el.strip()
    return None

def parse_img(el: WebElement | None) -> str | None:
    if el:
        return str(el.get_attribute("src"))
    return None

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def compare_list(a: str, b: list[str]) -> float:
    """Compare a string against a list of strings. """
    return any(similarity(a, item) for item in b)

def random_sleep(amount: float = 2.0, r: float = 0.5):
    """Sleep for certain amount of time with a random jitter. """
    time.sleep(max(0.0, amount + random.uniform(-r, r)))

def is_docker():
    """Check if running in a Docker container. """
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())

def scroll_into(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

def click_el(driver, element, retries=5):
    for i in range(retries):
        try:
            wait_for(Condition.CLICKABLE, WebDriverWait(driver, CONFIG.wait_timeout), element)
            scroll_into(driver, element)
            element.click()
            return True
        except (ElementClickInterceptedException,
                StaleElementReferenceException,
                ElementNotInteractableException,
                InvalidElementStateException) as e:
            prdebug(f"Click attempt {i + 1} failed: {e}")
    return False

def get_swal(driver) -> Swal:
    """Get 'SweetAlert' (swal) alert. """
    def _find(d, w, sel):
        if wait_for(Condition.PRESENCE, w, sel):
            return find(d, sel)
    wait = WebDriverWait(driver, 1)

    try:
        swal = _find(driver, wait, SwalSelectors.MODAL)
        if swal:
            title = _find(swal, wait, SwalSelectors.TITLE)
            text = _find(swal, wait, SwalSelectors.TEXT)
            icon = _find(swal, wait, SwalSelectors.ICON)
            
            confirm_button = _find(swal, wait, SwalSelectors.CONFIRM_BUTTON)

            # Some alerts have content and footer instead of title, text and icon
            if not title or not text:
                content = _find(swal, wait, SwalSelectors.CONTENT)
                if content:
                    title = _find(content, wait, SwalSelectors.CONTENT_TITLE)
                    text = _find(content, wait, SwalSelectors.CONTENT_TEXT)
                    icon = _find(content, wait, SwalSelectors.CONTENT_ICON)

            title = title.text.strip() if title else None
            text = text.text.strip() if text else None
            icon = icon.get_attribute("src") if icon else None
            prdebug(f"Got Swal: title={title}, text={text}, icon={icon}, confirm_button={confirm_button}")
            return Swal(
                title=title,
                text=text,
                icon=icon,
                confirm_button=confirm_button
            )

    except Exception as e:
        prerror(f"Error while getting swal alert: {e}\n{traceback.format_exc()}")
    
    return Swal()

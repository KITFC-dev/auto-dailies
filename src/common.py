import traceback
import time
import random
import re

from selenium.webdriver.support.ui import WebDriverWait
from difflib import SequenceMatcher
from pathlib import Path
from selenium.webdriver.remote.webelement import WebElement
from typing import overload, Literal

from src.constants import SwalSelectors, Condition
from src.locators import wait_for, find
from src.logger import prerror, prdebug
from src.models import Swal
from src.config import CONFIG

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
            scroll_into(driver, element)
            element.click()
            return True
        except Exception:
            driver.execute_script("arguments[0].click();", element)
            return True
        prdebug(f"Click attempt {i + 1} failed.")
    return False

def get_swal(driver) -> Swal:
    """Get 'SweetAlert' (swal) alert. """
    def _find(d, w, sel):
        if wait_for(Condition.PRESENCE, w, sel):
            return find(d, sel)
    wait = WebDriverWait(driver, CONFIG.wait_timeout)

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

import time
import random

from selenium.webdriver.support.ui import WebDriverWait
from difflib import SequenceMatcher
from pathlib import Path

from src.constants import SwalSelectors, Condition
from src.locators import wait_for, find
from src.logger import prerror
from src.models import Swal
from src.config import CONFIG

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def compare_list(a: str, b: list[str]) -> float:
    """Compare a string against a list of strings. """
    return any(similarity(a, item) for item in b)

def random_sleep(amount: float = 2.0, r: float = 0.5):
    """Sleep for certain amount of time with a random jitter. """
    time.sleep(max(0.0, amount + random.uniform(-r, r)))

def diff_text(label: str, init_val: int, curr_val: int) -> str:
    """Generates a diff stylized text from id. """
    if init_val < curr_val:
        diff = '+'
    elif init_val > curr_val:
        diff = '-'
    else:
        diff = ' '

    return f"{diff} {label.title()}: {init_val} -> {curr_val}\n"

def is_docker():
    """Check if running in a Docker container. """
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())

def scroll_into(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

def get_swal(driver) -> Swal:
    """Get 'SweetAlert' (swal) alert. """
    wait = WebDriverWait(driver, CONFIG.wait_timeout)

    try:
        wait_for(Condition.VISIBLE, wait, SwalSelectors.MODAL)
        swal = find(driver, SwalSelectors.MODAL)
        if swal:
            title = find(swal, SwalSelectors.TITLE)
            text = find(swal, SwalSelectors.TEXT)
            icon = find(swal, SwalSelectors.ICON)
            
            wait_for(Condition.VISIBLE, wait, SwalSelectors.CONFIRM_BUTTON)
            confirm_button = find(swal, SwalSelectors.CONFIRM_BUTTON)

            # Some alerts have content and footer instead of title, text and icon
            if not title or not text:
                content = find(swal, SwalSelectors.CONTENT)
                if content:
                    title = find(content, SwalSelectors.CONTENT_TITLE)
                    text = find(content, SwalSelectors.CONTENT_TEXT)
                    icon = find(content, SwalSelectors.CONTENT_ICON)
            
            return Swal(
                title=title.text.strip() if title else None,
                text=text.text.strip() if text else None,
                icon=icon.get_attribute("src") if icon else None,
                confirm_button=confirm_button
            )

    except Exception as e:
        prerror(f"Error while getting swal alert: {e}")
    
    return Swal()

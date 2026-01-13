from typing import List, Tuple

from selenium.webdriver.support.ui import WebDriverWait

from src.logger import prwarn
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL, StateSelectors, LocatorEnum
from src.locators import wait_for

def run_get_balance(driver):
    res = {}
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(BASE_URL)

    try:
        # Elements to fetch
        elements: List[Tuple[StateSelectors, str]] = [
            (StateSelectors.BALANCE, "balance"),
            (StateSelectors.COINS, "coins")
        ]

        # Get elements
        for sel, name in elements:
            e = wait_for(LocatorEnum.PRESENCE, wait, sel)
            if not e:
                prwarn(f"Couldn't find {name} element")
                continue

            e = e.text.strip() or str(e.get_attribute("textContent")).strip()
            res[name] = int(e.replace("\u00A0", "").replace(",", ""))

        random_sleep(0.3)
    except Exception as e:
        prwarn(f"Error while getting balance: {e}")

    return res

def run_get_inventory(driver):
    # Will be implemented later
    pass

def get_profile(driver):
    res = {"id": "", "avatar_url": "", "username": "", "is_verified": False}
    # Will be implemented later
    return res
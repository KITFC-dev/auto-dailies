from typing import List, Tuple

from selenium.webdriver.support.ui import WebDriverWait

from src.logger import prwarn
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL, PROFILE_URL, StateSelectors, ProfileSelectors, Condition
from src.locators import wait_for, find

def run_get_balance(driver) -> dict:
    """
    Get user's balance and coins on the website

    Returns:
        dict: {
            "balance": int,
            "coins": int
        }
    """
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
            e = wait_for(Condition.PRESENCE, wait, sel)
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

def get_profile(driver) -> dict:
    """
    Get user's profile information

    Returns:
        dict: {
            "id": str,
            "avatar_url": str,
            "username": str,
            "rice": int,
            "is_verified": bool
        }
    """
    res = {"id": "", "avatar_url": "", "username": "", "rice": 0, "is_verified": False}
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(PROFILE_URL)

    try:
        box = wait_for(Condition.PRESENCE, wait, ProfileSelectors.PANEL_BOX)
        if box:
            # ID
            id = find(box, ProfileSelectors.ID)
            if id is not None:
                res["id"] = id.text.strip()
            
            # Avatar
            avatar = find(box, ProfileSelectors.AVATAR)
            if avatar is not None:
                res["avatar_url"] = avatar.get_attribute("src")
            
            # Username
            username = find(box, ProfileSelectors.USERNAME)
            if username is not None:
                res["username"] = username.text.strip()
            
            # Rice
            rice = find(box, ProfileSelectors.RICE)
            if rice is not None:
                res["rice"] = int(rice.text.strip())
            
            # Verified
            verified = find(box, ProfileSelectors.IS_VERIFIED)
            if verified is not None:
                res["is_verified"] = "true" in str(verified.get_attribute("class"))
    except Exception as e:
        prwarn(f"Error while getting profile data: {e}")

    return res

from selenium.webdriver.support.ui import WebDriverWait
from typing import List

from src.logger import prwarn, prerror
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL, PROFILE_URL, StateSelectors, \
    ProfileSelectors, InventorySelectors, Condition
from src.locators import wait_for, find
from src.models import Balance, InventoryItem, InventoryMeta, \
    Profile

def run_get_balance(driver) -> Balance | None:
    """
    Get user's balance and coins on the website.
    """
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(BASE_URL)

    try:
        balance = wait_for(Condition.PRESENCE, wait, StateSelectors.BALANCE)
        coins = wait_for(Condition.PRESENCE, wait, StateSelectors.COINS)
        if not balance or not coins:
            raise Exception("Balance or coins not found")

        return Balance(balance=int(balance.text.strip()), coins=int(coins.text.strip()))
        random_sleep(0.3)
    except Exception as e:
        prwarn(f"Error while getting balance: {e}")
        return None

def get_profile_inventory(driver) -> List[InventoryItem]:
    """
    Get user's inventory. 
    """
    res = []
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(PROFILE_URL)

    try:
        wait_for(Condition.VISIBLE, wait, InventorySelectors.ITEM_BOX)
        items = find(driver, InventorySelectors.ITEM_BOX, multiple=True)

        for item in items:
            img_loc = find(item, InventorySelectors.IMAGE)
            name_loc = find(item, InventorySelectors.NAME)
            price_loc = find(item, InventorySelectors.PRICE)
            ctype_loc = find(item, InventorySelectors.CURRENCY_TYPE)
            
            currency_type = "unknown"
            if ctype_loc is not None:
                c_type = str(ctype_loc.get_attribute("class"))
                if "coin" in c_type:
                    currency_type = "coin"
                elif "mor" in c_type:
                    currency_type = "mor"

            res.append(InventoryItem(
                    image=img_loc.get_attribute("src") if img_loc else None, 
                    name=name_loc.text.strip() if name_loc else None, 
                    price=int(price_loc.text.strip()) if price_loc else 0, 
                    currency_type=currency_type
                )
            )
    except Exception as e:
        prwarn(f"Error while getting inventory: {e}")

    return res

def run_get_profile(driver) -> Profile | None:
    """
    Get user's profile information. 
    """
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(PROFILE_URL)

    try:
        box = wait_for(Condition.PRESENCE, wait, ProfileSelectors.PANEL_BOX)
        if box:
            id_el = find(box, ProfileSelectors.ID)
            avatar_el = find(box, ProfileSelectors.AVATAR)
            username_el = find(box, ProfileSelectors.USERNAME)
            rice_el = find(box, ProfileSelectors.RICE)
            verified_el = find(box, ProfileSelectors.IS_VERIFIED)

            if id_el is None:
                raise Exception("ID not found")

            id = id_el.text.split("ID")[-1].strip()
            avatar_url = avatar_el.get_attribute("src") if avatar_el else None
            username = username_el.text.strip() if username_el else None
            rice = int(rice_el.text.strip()) if rice_el and rice_el.text.strip().isdigit() else None
            is_verified = "true" in str(verified_el.get_attribute("class")) if verified_el else None

            inventory = get_profile_inventory(driver)
            inventory_meta = InventoryMeta(
                all_coins = sum(i.price for i in inventory if i.currency_type == "coin"),
                all_balance = sum(i.price for i in inventory if i.currency_type == "mor"),
            )

            return Profile(
                id=id,
                avatar_url=avatar_url,
                username=username,
                rice=rice,
                is_verified=is_verified,
                inventory=inventory,
                inventory_meta=inventory_meta
            )
    except Exception as e:
        prerror(f"Error while getting profile data: {e}")

    return None

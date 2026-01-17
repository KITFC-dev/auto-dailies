from selenium.webdriver.support.ui import WebDriverWait

from src.logger import prwarn
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL, PROFILE_URL, StateSelectors, \
    ProfileSelectors, InventorySelectors, Condition
from src.locators import wait_for, find
from src.models import Balance

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

def run_get_profile(driver) -> dict:
    """
    Get whole profile data, including inventory, 
    profile info and other metadata. 
    """
    inventory = get_profile_inventory(driver)
    data = get_profile_data(driver)

    meta = {
        "all_coins": sum(i["price"] for i in inventory if i["currency_type"] == "coin"),
        "all_balance": sum(i["price"] for i in inventory if i["currency_type"] == "mor"),
    }

    return {
        **data,
        "inventory": inventory,
        "inventory_meta": meta
    }

def get_profile_inventory(driver):
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
            # Image
            img_loc = find(item, InventorySelectors.IMAGE)
            image = ""
            if img_loc is not None:
                image = img_loc.get_attribute("src")

            # Name
            name_loc = find(item, InventorySelectors.NAME)
            name = ""
            if name_loc is not None:
                name = name_loc.text.strip()
            
            # Price
            price_loc = find(item, InventorySelectors.PRICE)
            price = 0
            if price_loc is not None:
                price = int(price_loc.text.strip())

            # Currency type
            ctype_loc = find(item, InventorySelectors.CURRENCY_TYPE)
            currency_type = "unknown"
            if ctype_loc is not None:
                c_type = str(ctype_loc.get_attribute("class"))
                if "coin" in c_type:
                    currency_type = "coin"
                elif "mor" in c_type:
                    currency_type = "mor"

            res.append({
                "image": image,
                "name": name,
                "price": price,
                "currency_type": currency_type
            })
    except Exception as e:
        prwarn(f"Error while getting inventory: {e}")

    return res

def get_profile_data(driver) -> dict:
    """
    Get user's profile information. 
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
                res["id"] = id.text.split("ID")[-1].strip()
            
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

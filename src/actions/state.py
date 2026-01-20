from selenium.webdriver.support.ui import WebDriverWait

from src.logger import prwarn, prerror, prsuccess
from src.common import random_sleep, get_swal, similarity
from src.config import CONFIG
from src.constants import PROFILE_URL, IGNORE_ITEMS, StateSelectors, \
    ProfileSelectors, InventorySelectors, Condition, CurrencyType, \
        SellResultType
from src.locators import wait_for, find
from src.models import Balance, InventoryItem, Profile

def get_profile_balance(driver) -> Balance | None:
    """
    Get user's balance and coins on the website.
    """
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != PROFILE_URL:
        driver.get(PROFILE_URL)

    try:
        gold = wait_for(Condition.PRESENCE, wait, StateSelectors.GOLD)
        coins = wait_for(Condition.PRESENCE, wait, StateSelectors.COINS)
        if not gold or not coins:
            raise Exception("Balance or coins not found")

        return Balance(gold=int(gold.text.strip()), coins=int(coins.text.strip()))
        random_sleep(0.3)
    except Exception as e:
        prwarn(f"Error while getting balance: {e}")
        return None

def get_profile_inventory(driver) -> list[InventoryItem]:
    """
    Get user's inventory and sell specified items.
    """
    res = []
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != PROFILE_URL:
        driver.get(PROFILE_URL)

    try:
        wait_for(Condition.VISIBLE, wait, InventorySelectors.ITEM_BOX)

        # Load all items
        while True:
            load_more = wait_for(Condition.VISIBLE, wait, InventorySelectors.LOAD_MORE_BUTTON)
            if load_more:
                load_more.click()
                print("Loading more items...")
                random_sleep(1)
            else:
                break

        items = find(driver, InventorySelectors.ITEM_BOX, multiple=True)

        for item in items:
            img_loc = find(item, InventorySelectors.IMAGE)
            name_loc = find(item, InventorySelectors.NAME)
            price_loc = find(item, InventorySelectors.PRICE)
            ctype_loc = find(item, InventorySelectors.CURRENCY_TYPE)
            sell_button = find(item, InventorySelectors.SELL_BUTTON)
            # Name
            if name_loc:
                name = name_loc.text.strip()
            else:
                continue # skip items without a name
            # Image
            if img_loc:
                image = img_loc.get_attribute("src")
            else:
                image = None
            # Price
            if price_loc:
                price = int(price_loc.text.strip())
            else:
                price = 0
            # Currency type
            currency_type = CurrencyType.UNKNOWN
            if ctype_loc is not None:
                c_type = str(ctype_loc.get_attribute("class"))
                if "coin" in c_type:
                    currency_type = CurrencyType.COIN
                elif "mor" in c_type:
                    currency_type = CurrencyType.GOLD
            
            # Check if we need to sell items
            sell = False
            if CONFIG.sell_inventory and sell_button is not None and \
            (not any(ignored.lower() in name.lower() for ignored in IGNORE_ITEMS)
             or CONFIG.sell_ignored is True):
                # Check for gold items
                if currency_type == CurrencyType.GOLD:
                    if CONFIG.sell_gold:
                        if price <= CONFIG.sell_gold_price_threshold:
                            sell = True
                elif currency_type == CurrencyType.COIN:
                    sell = True

                if sell:
                    try:
                        sell_button.click()
                        swal = get_swal(driver)
                        if swal.title and similarity(swal.title, SellResultType.SUCCESS):
                            prsuccess(f"Successfully sold {name} for {price} {currency_type}")
                        else:
                            raise Exception(f"Error while selling {name}: {swal.title}, {swal.text}")
                        random_sleep(1.5)
                    except Exception as e:
                        prwarn(f"{e}")
                        sell = False

            res.append(InventoryItem( 
                    name=name, 
                    image=image,
                    price=price, 
                    currency_type=currency_type,
                    sold=sell,
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
    if driver.current_url != PROFILE_URL:
        driver.get(PROFILE_URL)

    try:
        box = wait_for(Condition.VISIBLE, wait, ProfileSelectors.PANEL_BOX)
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

            balance = get_profile_balance(driver)
            inventory = get_profile_inventory(driver)

            return Profile(
                id=id,
                avatar_url=avatar_url,
                username=username,
                rice=rice,
                is_verified=is_verified,
                balance=balance if balance else Balance(0, 0),
                inventory=inventory,
            )

    except Exception as e:
        prerror(f"Error while getting profile data: {e}")

    return None

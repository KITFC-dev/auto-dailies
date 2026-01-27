from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from src.logger import prsuccess, prdebug
from src.config import CONFIG
from src.locators import wait_for, find
from src.models import Balance, InventoryItem, Profile
from src.common import random_sleep, get_swal, parse_num, \
    click_el, handle_exceptions, parse_img, parse_text
from src.constants import PROFILE_URL, IGNORE_ITEMS, StateSelectors, \
    ProfileSelectors, InventorySelectors, Condition, CurrencyType

def get_profile_balance(driver) -> Balance:
    """Get user's gold and coins. """
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != PROFILE_URL:
        driver.get(PROFILE_URL)

    gold = parse_num(wait_for(Condition.PRESENCE, wait, StateSelectors.GOLD))
    coins = parse_num(wait_for(Condition.PRESENCE, wait, StateSelectors.COINS))

    return Balance(gold=gold or 0, coins=coins or 0)

def sell_item(driver, i: InventoryItem, sell_button: WebElement | None) -> bool:
    """Helper for selling items from user's inventory. """
    # Check if can sell item
    can_sell = False
    if CONFIG.sell_inventory and sell_button is not None:
        # is item in ignored items list
        if (not any(ignored.lower() in i.name.lower() for ignored in IGNORE_ITEMS) or CONFIG.sell_ignored is True):
            # Check for gold items
            match i.currency_type:
                case CurrencyType.GOLD:
                    if CONFIG.sell_gold:
                        if i.price <= CONFIG.sell_gold_price_threshold:
                            can_sell = True
                case CurrencyType.COIN:
                    can_sell = True
    
    # Sell item
    if can_sell:
        click_el(driver, sell_button)
        swal = get_swal(driver)
        if swal.confirm_button:
            prsuccess(f"Successfully sold {i.name} for {i.price} {i.currency_type}")
            random_sleep(1)
            swal.click_confirm()
        # Cooldown after selling
        random_sleep(2, 1)
    return can_sell

def get_profile_inventory(driver) -> list[InventoryItem]:
    """Get user's inventory items. """
    res = []
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != PROFILE_URL:
        driver.get(PROFILE_URL)

    wait_for(Condition.VISIBLE, wait, InventorySelectors.ITEM_BOX)
    # Load all items
    while True:
        load_more = wait_for(Condition.VISIBLE, wait, InventorySelectors.LOAD_MORE_BUTTON)
        if load_more:
            click_el(driver, load_more)
            random_sleep(1)
        else:
            break

    for item in find(driver, InventorySelectors.ITEM_BOX, multiple=True):
        # Get item info
        name = parse_text(find(item, InventorySelectors.NAME))
        if name is None:
            continue
        image = parse_img(find(item, InventorySelectors.IMAGE))
        price = parse_num(find(item, InventorySelectors.PRICE))
        ctype_loc = find(item, InventorySelectors.CURRENCY_TYPE)
        sell_button = find(item, InventorySelectors.SELL_BUTTON)
        currency_type = CurrencyType.UNKNOWN
        if ctype_loc is not None:
            c_type = str(ctype_loc.get_attribute("class"))
            if "coin" in c_type:
                currency_type = CurrencyType.COIN
            elif "mor" in c_type:
                currency_type = CurrencyType.GOLD
        
        item_data = InventoryItem(
            name=name,
            image=image,
            price=price,
            currency_type=currency_type)
        item_data.sold = sell_item(driver, item_data, sell_button)
        res.append(item_data)
    return res

@handle_exceptions()
def run_profile(driver) -> Profile | None:
    """Get user's profile information. """
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != PROFILE_URL:
        driver.get(PROFILE_URL)

    box = wait_for(Condition.VISIBLE, wait, ProfileSelectors.PANEL_BOX)
    if box:
        # Get profile data
        id_el = find(box, ProfileSelectors.ID)
        if id_el is None:
            raise Exception("ID not found")
        id = id_el.text.split("ID")[-1].strip()
        avatar_url = parse_img(find(box, ProfileSelectors.AVATAR))
        username = parse_text(find(box, ProfileSelectors.USERNAME))
        rice = parse_num(find(box, ProfileSelectors.RICE))
        verified_el = find(box, ProfileSelectors.IS_VERIFIED)
        is_verified = "true" in str(verified_el.get_attribute("class")) if verified_el else None

        # Get other data
        balance = get_profile_balance(driver)
        inventory = get_profile_inventory(driver)

        data = Profile(
            id=id,
            avatar_url=avatar_url,
            username=username,
            rice=rice,
            is_verified=is_verified,
            balance=balance,
            inventory=inventory,
        )
        prdebug(f"Profile data: {data}")
        return data

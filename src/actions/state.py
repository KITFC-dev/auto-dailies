from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.logger import prwarn
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL, StateSelectors

def run_get_balance(driver):
    res = {}
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(BASE_URL)

    try:
        # Wait until elements are present
        bal_el = wait.until(EC.presence_of_element_located(StateSelectors.BALANCE))
        coins_el = wait.until(EC.presence_of_element_located(StateSelectors.COINS))

        # Parse the text, fallback to getAttribute if text is empty
        balance_text = bal_el.text.strip() or str(bal_el.get_attribute("textContent")).strip()
        coins_text   = coins_el.text.strip() or str(coins_el.get_attribute("textContent")).strip()
        res["balance"] = int(balance_text.replace("\u00A0", "").replace(",", ""))
        res["coins"] = int(coins_text.replace("\u00A0", "").replace(",", ""))

        random_sleep(0.3)
    except TimeoutException:
        prwarn("No balance or coins label detected")

    return res

def run_get_inventory(driver):
    # Will be implemented later
    pass

def get_profile(driver):
    res = {"id": "", "avatar_url": "", "username": "", "is_verified": False}
    # Will be implemented later
    return res
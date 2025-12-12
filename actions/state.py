import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import prsuccess, prwarn
from config import ELEMENTS, BASE_URL

def run_get_balance(driver):
    res = {"balance": 0, "coins": 0}
    wait = WebDriverWait(driver, 2)
    driver.get(BASE_URL)

    # Selectors
    balance_locator = (By.CSS_SELECTOR, f"span[data-key='{ELEMENTS['balance_label']}']")
    coins_locator   = (By.CSS_SELECTOR, f"span[data-key='{ELEMENTS['coins_label']}']")

    try:
        # Wait until elements are present
        bal_el = wait.until(EC.presence_of_element_located(balance_locator))
        coins_el = wait.until(EC.presence_of_element_located(coins_locator))

        # Parse the text, fallback to getAttribute if text is empty
        balance_text = bal_el.text.strip() or bal_el.get_attribute("textContent").strip()
        coins_text   = coins_el.text.strip() or coins_el.get_attribute("textContent").strip()
        res["balance"] = int(balance_text.replace("\u00A0", "").replace(",", ""))
        res["coins"] = int(coins_text.replace("\u00A0", "").replace(",", ""))

        time.sleep(0.3)
        prsuccess(f"Got balance ({res['balance']}) and coins ({res['coins']})")
    except Exception:
        prwarn("No balance or coins label detected.")

    return res

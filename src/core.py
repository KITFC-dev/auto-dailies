from src.browser import create_driver
from src.cookies import load_cookies, save_cookies
from src.logger import prinfo, prsuccess, prerror
from src.actions.checkin import run_daily_checkin
from src.actions.giveaway import run_giveaway
from src.actions.case import get_cases, open_case
from src.actions.state import run_get_balance
from src.common import random_sleep
from config import BASE_URL, CHROMIUM_PATH, CHROMEDRIVER_PATH, IGNORE_CASES

def run(cookie_file, headless, checkin, giveaway, cases, wait_after: int = 0):
    """Logs in to the website using the given cookie file and runs given actions """
    driver = create_driver(CHROMIUM_PATH, CHROMEDRIVER_PATH, headless)
    driver.get(BASE_URL)

    # Load cookies to browser
    if not load_cookies(driver, cookie_file):
        prerror(f"No cookie file: {cookie_file}")
        return False
    driver.refresh()

    # Verify if login was successful
    balance = run_get_balance(driver)
    if balance == {}:
        prerror(f"Failed to get balance, the login may have failed. Skipping {cookie_file}")
        return False

    # Run actions
    if cases:
        available_cases = get_cases(driver)
        for case in available_cases:
            # Skip ignored cases
            if case["link"].split("/")[-1] not in IGNORE_CASES:
                if open_case(driver, case["link"]):
                    prsuccess(f"Opened case: {case['name']}")
                    random_sleep(7)
    if checkin:
        run_daily_checkin(driver)
    if giveaway:
        run_giveaway(driver)

    # Calculate earned coins
    balance_after = run_get_balance(driver)
    earned_coins = balance_after["coins"] - balance["coins"]
    earned_balance = balance_after["balance"] - balance["balance"]
    
    # Wait before closing
    if wait_after > 0:
        prinfo(f"Waiting {wait_after} seconds before closing the browser...")
        random_sleep(wait_after, 0)

    # Cleanup
    save_cookies(driver, cookie_file)
    driver.quit()

    return {"earned_coins": earned_coins, "earned_balance": earned_balance}

from src.browser import create_driver, load_cookies, save_cookies
from src.logger import prinfo, prsuccess, prerror, prwebhook
from src.actions.checkin import run_daily_checkin
from src.actions.giveaway import run_giveaway
from src.actions.case import get_cases, open_case
from src.actions.state import run_get_balance
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL, IGNORE_CASES

def run_once(cookie_file):
    """Logs in to the website using the given cookie file and runs given actions """
    driver = create_driver(CONFIG.chromium_path, CONFIG.chromedriver_path, CONFIG.headless if not CONFIG.new_account else False)
    driver.get(BASE_URL)

    res = {}

    # Load cookies to browser
    if cookie_file.split("/")[-1] != CONFIG.new_account:
        if not load_cookies(driver, cookie_file):
            prerror(f"No cookie file: {cookie_file}")
            return False
    else:
        prinfo(f"New account: {cookie_file}, waiting 90 seconds for user to log in...")
        random_sleep(90, 0)
        save_cookies(driver, cookie_file)

    driver.refresh()

    # Verify if login was successful
    balance = run_get_balance(driver)
    if balance == {}:
        prerror(f"Failed to get balance, the login may have failed. Skipping {cookie_file}")
        return False
    
    res["initial_coins"] = balance["coins"]
    res["initial_balance"] = balance["balance"]

    # Run actions
    if CONFIG.checkin:
        run_daily_checkin(driver)
    if CONFIG.giveaway:
        run_giveaway(driver)
    if CONFIG.cases:
        available_cases = get_cases(driver)
        res["available_cases"] = len(available_cases)
        res["opened_cases"] = 0
        for case in available_cases:
            # Skip ignored cases
            if case["link"].split("/")[-1] not in IGNORE_CASES:
                if open_case(driver, case["link"]):
                    prsuccess(f"Opened case: {case['name']}")
                    res["opened_cases"] += 1
                    random_sleep(7)

    # Calculate earned coins
    balance_after = run_get_balance(driver)
    res["coins"] = balance_after["coins"]
    res["balance"] = balance_after["balance"]

    # Wait before closing
    if CONFIG.wait_after > 0:
        prinfo(f"Waiting {CONFIG.wait_after} seconds before closing the browser...")
        random_sleep(CONFIG.wait_after, 0)

    # Cleanup
    save_cookies(driver, cookie_file)
    driver.quit()

    return res

def run():
    # Variables
    done_accounts = []
    failed_accounts = []
    account_results = []

    # Iterate over all accounts
    for name, cookie_file in CONFIG.accounts.items():
        if (name not in CONFIG.accounts if CONFIG.accounts else False):
            continue
        prinfo(f"Processing account: {name}")
        res = run_once(cookie_file)
        if res:
            res["name"] = name
            done_accounts.append(name)
            account_results.append(res)
            prsuccess(f"Account {name} done")
        else:
            failed_accounts.append(name)
            prerror(f"Account {name} failed")

    # Send summary webhook
    earned_coins = sum(i.get("coins", 0) - i.get("initial_coins", 0) for i in account_results)
    earned_balance = sum(i.get("balance", 0) - i.get("initial_balance", 0) for i in account_results)
    prwebhook(
        title="Tasks completed!",
        description=f"Accounts Done: {len(done_accounts)}\nAccounts Failed: {len(failed_accounts)}\n\nEarned Coins: {earned_coins}\nEarned Balance: {earned_balance}",
        color=2818303,
        fields=[{
            "name": res["name"], 
            "value": f"Coins: {res.get('initial_coins', 0)} -> {res.get('coins', 0)}\nBalance: {res.get('initial_balance', 0)} -> {res.get('balance', 0)}", 
            "inline": False}
            for res in account_results],
    )

    prsuccess("All Done!")
    return True

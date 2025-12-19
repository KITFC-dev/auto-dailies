import argparse
import time

from config import BASE_URL, ACCOUNTS, CHROMIUM_PATH, CHROMEDRIVER_PATH, IGNORE_CASES
from browser import create_driver
from utils.cookies import load_cookies, save_cookies
from utils.logger import prinfo, prsuccess, prerror
from actions.checkin import run_daily_checkin
from actions.giveaway import run_giveaway
from actions.case import get_cases, open_case
from actions.state import run_get_balance

def login_and_run(cookie_file, headless, checkin, giveaway, cases, wait_after: int = 0):
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
                    time.sleep(7)
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
        time.sleep(wait_after)

    # Cleanup
    save_cookies(driver, cookie_file)
    driver.quit()

    return {"earned_coins": earned_coins, "earned_balance": earned_balance}

def main(headless=False, checkin=False, giveaway=False, cases=False, accounts=[], wait_after=0):
    """
    Entry point of the program

    Args:
        -H, --headless: Starts the browser in headless mode.
        -C, --checkin: Runs the daily check-in.
        -G, --giveaway: Runs the giveaway.
        -cs, --cases: Open cases.
        -w, --wait-after: Number of seconds to wait before closing the browser.
        --accounts: Specify which accounts to process.
        --webhook_url: Discord webhook URL to send logs to.
    """
    parser = argparse.ArgumentParser(description="AutoDailies")
    parser.add_argument("-H", "--headless", action="store_true", help="Starts the browser in headless mode.")
    parser.add_argument("-c", "--checkin", action="store_true", help="Runs the daily check-in.")
    parser.add_argument("-g", "--giveaway", action="store_true", help="Runs the giveaway.")
    parser.add_argument("-cs", "--cases", action="store_true", help="Open cases.")
    parser.add_argument("-w", "--wait-after", type=int, default=0, help="Number of seconds to wait before closing the browser.")
    parser.add_argument("--accounts", nargs='*', help="Specify which accounts to process. If empty, all accounts will be processed.")
    parser.add_argument("--webhook_url", type=str, default=None, help="Discord webhook URL to send logs to.")
    args = parser.parse_args()

    # Validate arguments
    if args.webhook_url:
        import config
        config.WEBHOOK_URL = args.webhook_url
    prinfo(f"Loading Discord webhook: {config.WEBHOOK_URL}")

    # Variables
    done_accounts = []
    failed_accounts = []
    earned_coins = 0
    earned_balance = 0

    # Iterate over all accounts
    for name, cookie_file in ACCOUNTS.items():
        if (name not in args.accounts if args.accounts else False) or (name not in accounts if accounts else False):
            continue
        prinfo(f"Processing account: {name}")
        res = login_and_run(cookie_file, 
            headless | args.headless, 
            checkin | args.checkin, 
            giveaway | args.giveaway,
            cases | args.cases,
            wait_after=wait_after | args.wait_after
        )
        if res:
            done_accounts.append(name)
            earned_coins += res["earned_coins"]
            earned_balance += res["earned_balance"]
            prsuccess(f"Account {name} done")
        else:
            failed_accounts.append(name)
            prerror(f"Account {name} failed")
    
    prsuccess(f"All done!\n{len(done_accounts)} accounts done\n{len(failed_accounts)} accounts failed\n\nEarned coins: {earned_coins}\nEarned balance: {earned_balance}", webhook=True)

if __name__ == "__main__":
    main(checkin=True, giveaway=True, cases=True, wait_after=0)

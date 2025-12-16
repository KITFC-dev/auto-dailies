import argparse
import time

from config import ACCOUNTS, CHROMIUM_PATH, CHROMEDRIVER_PATH
from browser import create_driver
from utils.cookies import load_cookies, save_cookies
from utils.logger import prinfo, prsuccess, prerror
from actions.checkin import run_daily_checkin
from actions.giveaway import run_giveaway
from actions.state import run_get_balance

def login_and_run(cookie_file, headless, checkin, giveaway, wait_after: int = 0):
    """Logs in to the website using the given cookie file and runs given actions """
    driver = create_driver(CHROMIUM_PATH, CHROMEDRIVER_PATH, headless)
    driver.get("https://genshindrop.io")

    # Load cookies to browser
    if not load_cookies(driver, cookie_file):
        prerror(f"No cookie file: {cookie_file}")
        return
    driver.refresh()

    balance = run_get_balance(driver)
    if balance == {}:
        prerror(f"Failed to get balance, the login may have failed. Skipping {cookie_file}")
        return

    # Run actions
    if checkin:
        run_daily_checkin(driver)
    if giveaway:
        run_giveaway(driver)
    
    # Wait before closing
    if wait_after > 0:
        prinfo(f"Waiting {wait_after} seconds before closing the browser...")
        time.sleep(wait_after)

    # Cleanup
    save_cookies(driver, cookie_file)
    driver.quit()

def main(headless=False, checkin=False, giveaway=False, accounts=[], wait_after=0):
    """
    Entry point of the program

    Args:
        -H, --headless: Starts the browser in headless mode.
        -C, --checkin: Runs the daily check-in.
        -G, --giveaway: Runs the giveaway.
        -w, --wait-after: Number of seconds to wait before closing the browser.
        --accounts: Specify which accounts to process.
    """
    parser = argparse.ArgumentParser(description="AutoDailies")
    parser.add_argument("-H", "--headless", action="store_true", help="Starts the browser in headless mode.")
    parser.add_argument("-c", "--checkin", action="store_true", help="Runs the daily check-in.")
    parser.add_argument("-g", "--giveaway", action="store_true", help="Runs the giveaway.")
    parser.add_argument("--accounts", nargs='*', help="Specify which accounts to process. If empty, all accounts will be processed.")
    parser.add_argument("-w", "--wait-after", type=int, default=0, help="Number of seconds to wait before closing the browser.")
    args = parser.parse_args()

    # Iterate over all accounts
    for name, cookie_file in ACCOUNTS.items():
        if (name not in args.accounts if args.accounts else False) or (name not in accounts if accounts else False):
            continue
        prinfo(f"Processing account: {name}")
        login_and_run(cookie_file, 
                    headless | args.headless, 
                    checkin | args.checkin, 
                    giveaway | args.giveaway,
                    wait_after=wait_after | args.wait_after
                    )
        prsuccess(f"Account {name} done")
    
    prsuccess("All done!")

if __name__ == "__main__":
    main(checkin=True, giveaway=True, wait_after=60)

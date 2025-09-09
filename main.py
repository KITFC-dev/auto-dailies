import argparse

from config import ACCOUNTS, CHROMIUM_PATH, CHROMEDRIVER_PATH
from browser import create_driver
from utils.cookies import load_cookies, save_cookies
from utils.logger import prinfo, prsuccess, prerror
from actions.checkin import run_daily_checkin
from actions.giveaway import run_giveaway

def login_and_run(cookie_file, headless, checkin, giveaway):
    """Logs in to the website using the given cookie file and runs given actions """
    driver = create_driver(CHROMIUM_PATH, CHROMEDRIVER_PATH, headless)
    driver.get("https://genshindrop.io")

    # Load cookies to browser
    if not load_cookies(driver, cookie_file):
        prerror(f"No cookie file: {cookie_file}")
        return

    driver.refresh()

    # Run actions
    if checkin:
        run_daily_checkin(driver)
    if giveaway:
        run_giveaway(driver)

    # Cleanup
    save_cookies(driver, cookie_file)
    driver.quit()

def main(headless=False, checkin=False, giveaway=False):
    """
    Entry point of the program

    Args:
        -H, --headless: Starts the browser in headless mode.
        -C, --checkin: Runs the daily check-in.
        -G, --giveaway: Runs the giveaway.
    """
    parser = argparse.ArgumentParser(description="AutoDailies")
    parser.add_argument("-H", "--headless", action="store_true")
    parser.add_argument("-c", "--checkin", action="store_true")
    parser.add_argument("-g", "--giveaway", action="store_true")
    args = parser.parse_args()

    # Iterate over all accounts
    for name, cookie_file in ACCOUNTS.items():
        prinfo(f"Processing account: {name}")
        login_and_run(cookie_file, headless | args.headless, checkin | args.checkin, giveaway | args.giveaway)
        prsuccess(f"Account {name} done")
    
    prsuccess("All done!")

if __name__ == "__main__":
    main()

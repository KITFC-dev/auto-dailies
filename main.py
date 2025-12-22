import argparse
import config
from config import ACCOUNTS
from src.logger import prinfo, prsuccess, prerror
from src.core import run

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
        res = run(cookie_file, 
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

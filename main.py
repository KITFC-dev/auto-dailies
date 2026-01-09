import argparse
import config
from src.logger import prinfo, prsuccess
from src.core import run_multiple

def main(headless=False, checkin=False, giveaway=False, cases=False, accounts=[], wait_after=0):
    """
    Entry point of AutoDailies.

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

    # Run for multiple accounts
    if run_multiple(
        args=args,
        headless=args.headless,
        checkin=args.checkin,
        giveaway=args.giveaway,
        cases=args.cases,
        accounts=args.accounts if args.accounts else config.ACCOUNTS,
        wait_after=args.wait_after
    ):
        prsuccess("All done!")

if __name__ == "__main__":
    main(checkin=True, giveaway=True, cases=True, wait_after=0)

from src.logger import prsuccess
from src.common import parse_args
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
    args = parse_args()

    # Run tasks for multiple accounts with given arguments
    if run_multiple(args):
        prsuccess("All done!")

if __name__ == "__main__":
    main(checkin=True, giveaway=True, cases=True, wait_after=0)

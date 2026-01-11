import time
import random
import argparse
import config

def parse_args(
    *args,
    **kwargs,
) -> argparse.Namespace:
    """
    Parse command line arguments for AutoDailies.

    Arguments priority:
        1. CLI Arguments
        2. Function Arguments
        3. Config Defaults

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    # Extract function arguments
    headless = kwargs.get("headless", False)
    checkin = kwargs.get("checkin", False)
    giveaway = kwargs.get("giveaway", False)
    cases = kwargs.get("cases", False)
    wait_after = kwargs.get("wait_after", 0)
    accounts = kwargs.get("accounts", [])
    webhook_url = kwargs.get("webhook_url", None)

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="AutoDailies")
    parser.add_argument("-H", "--headless", action="store_true", help="Starts the browser in headless mode.")
    parser.add_argument("-c", "--checkin", action="store_true", help="Runs the daily check-in.")
    parser.add_argument("-g", "--giveaway", action="store_true", help="Runs the giveaway.")
    parser.add_argument("-cs", "--cases", action="store_true", help="Opens the cases.")
    parser.add_argument("-w", "--wait-after", type=int, default=0, help="Number of seconds to wait before closing the browser.")
    parser.add_argument("--accounts", nargs='*', help="Specify which accounts to process. If empty, all accounts will be processed.")
    parser.add_argument("--webhook_url", type=str, default=None, help="Discord webhook URL to send logs to.")

    args = parser.parse_args()

    # Prioritize cli arguments
    args.headless = args.headless or headless
    args.checkin = args.checkin or checkin
    args.giveaway = args.giveaway or giveaway
    args.cases = args.cases or cases
    args.wait_after = args.wait_after if args.wait_after != 0 else wait_after
    args.accounts = args.accounts if args.accounts else accounts
    args.webhook_url = args.webhook_url if args.webhook_url else webhook_url

    # Validate arguments
    if args.webhook_url:
        config.WEBHOOK_URL = args.webhook_url
    
    if not args.accounts:
        args.accounts = config.ACCOUNTS    
    
    return args

def random_sleep(amount: float = 2.0, r: float = 0.5):
    time.sleep(max(0.0, amount + random.uniform(-r, r)))

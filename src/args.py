import argparse
import os
import config

def parse_config(**args) -> argparse.Namespace:
    """
    Parse config options for AutoDailies.

    Arguments priority:
        1. CLI Arguments
        2. Function Arguments
        3. Config Defaults
    """
    # Extract function arguments
    headless = args.get("headless", False)
    checkin = args.get("checkin", False)
    giveaway = args.get("giveaway", False)
    cases = args.get("cases", False)
    wait_after = args.get("wait_after", 0)
    accounts = args.get("accounts", [])
    webhook_url = args.get("webhook_url", None)
    chromium_path = args.get("chromium_path", config.CHROMIUM_PATH)
    chromedriver_path = args.get("chromedriver_path", config.CHROMEDRIVER_PATH)

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="AutoDailies")

    parser.add_argument("-H", "--headless", action="store_true", help="Starts the browser in headless mode.")
    parser.add_argument("-c", "--checkin", action="store_true", help="Runs the daily check-in.")
    parser.add_argument("-g", "--giveaway", action="store_true", help="Runs the giveaway.")
    parser.add_argument("-cs", "--cases", action="store_true", help="Opens the cases.")
    parser.add_argument("-w", "--wait-after", type=int, default=0, help="Number of seconds to wait before closing the browser.")
    parser.add_argument("--accounts", nargs='*', help="Specify which accounts to process. If empty, all accounts will be processed.")
    parser.add_argument("--webhook_url", type=str, default=None, help="Discord webhook URL to send logs to.")
    parser.add_argument("--chromium_path", type=str, default=chromium_path, help="Path to the browser binary.")
    parser.add_argument("--chromedriver_path", type=str, default=chromedriver_path, help="Path to the Chromedriver.")

    args = parser.parse_args()

    # Prioritize cli arguments
    args.headless = args.headless or headless
    args.checkin = args.checkin or checkin
    args.giveaway = args.giveaway or giveaway
    args.cases = args.cases or cases
    args.wait_after = args.wait_after if args.wait_after != 0 else wait_after
    args.accounts = args.accounts if args.accounts else accounts
    args.webhook_url = args.webhook_url if args.webhook_url else webhook_url
    args.chromium_path = os.path.abspath(args.chromium_path) if args.chromium_path else chromium_path
    args.chromedriver_path = os.path.abspath(args.chromedriver_path) if args.chromedriver_path else chromedriver_path

    # Validate arguments
    if args.webhook_url:
        config.webhook_url = args.webhook_url
    
    if not args.accounts:
        args.accounts = config.ACCOUNTS 
    
    return args

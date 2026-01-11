from src.logger import prsuccess
from src.args import parse_config
from src.core import run_multiple

def main(**args):
    """
    Entry point of AutoDailies.

    Args:
        headless (bool): Starts the browser in headless mode.
        checkin (bool): Runs the daily check-in.
        giveaway (bool): Runs the giveaway.
        cases (bool): Opens the cases.
        wait_after (int): Number of seconds to wait before closing the browser.
        accounts (list): Specify which accounts to process. If empty, all accounts will be processed.
        webhook_url (str): Discord webhook URL to send logs to.
        chromium_path (str): Path to the browser binary.
        chromedriver_path (str): Path to the Chromedriver.
    """
    # Run tasks for multiple accounts with given arguments
    if run_multiple(parse_config(**args)):
        prsuccess("All done!")

if __name__ == "__main__":
    main()

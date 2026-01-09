import time
import random
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="AutoDailies")
    parser.add_argument("-H", "--headless", action="store_true", help="Starts the browser in headless mode.")
    parser.add_argument("-c", "--checkin", action="store_true", help="Runs the daily check-in.")
    parser.add_argument("-g", "--giveaway", action="store_true", help="Runs the giveaway.")
    parser.add_argument("-cs", "--cases", action="store_true", help="Open cases.")
    parser.add_argument("-w", "--wait-after", type=int, default=0, help="Number of seconds to wait before closing the browser.")
    parser.add_argument("--accounts", nargs='*', help="Specify which accounts to process. If empty, all accounts will be processed.")
    parser.add_argument("--webhook_url", type=str, default=None, help="Discord webhook URL to send logs to.")
    return parser.parse_args()

def random_sleep(amount: float = 2.0, r: float = 0.5):
    time.sleep(max(0.0, amount + random.uniform(-r, r)))
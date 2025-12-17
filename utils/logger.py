import requests
from colorama import Fore, Style
from config import WEBHOOK_URL

def _send_webhook(msg, webhook_url=None):
    # Get webhook url
    if not webhook_url:
        webhook_url = WEBHOOK_URL
    # Discord webhook
    requests.post(webhook_url, json={"content": msg})

def _print_log(msg, color = Fore.CYAN, type = "info", webhook=False):
    # Print log
    print(f"{color}[{type.upper()}]{Style.RESET_ALL} {msg}")

    # Optionally send webhook
    if webhook:
        _send_webhook(msg)

def prinfo(msg, webhook=False): _print_log(msg, webhook=webhook)
def prsuccess(msg, webhook=False): _print_log(msg, color = Fore.GREEN, type = "success", webhook=webhook)
def prwarn(msg, webhook=False): _print_log(msg, color = Fore.YELLOW, type = "warning", webhook=webhook)
def prerror(msg, webhook=False): _print_log(msg, color = Fore.RED, type = "error", webhook=webhook)

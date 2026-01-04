import requests
import config
from colorama import Fore, Style

def _send_webhook(msg=None, embeds=None, webhook_url=None):
    # Get webhook url
    if not webhook_url:
        webhook_url = config.WEBHOOK_URL

    # Skip if webhook url is empty
    if not (webhook_url.strip()):
        return
    
    # Discord webhook
    payload = {}
    if msg:
        payload["content"] = msg
    if embeds:
        payload["embeds"] = embeds
    if config.WEBHOOK_PROFILE_NAME:
        payload["username"] = config.WEBHOOK_PROFILE_NAME
    if config.WEBHOOK_PROFILE_AVATAR:
        payload["avatar_url"] = config.WEBHOOK_PROFILE_AVATAR
    
    # Send webhook
    r = requests.post(webhook_url, json=payload, timeout=5)

    if not r.ok:
        prerror(f"Failed to send webhook: {r.status_code} {r.text}")

def _print_log(msg, color = Fore.CYAN, type = "info", webhook=False):
    # Print log
    print(f"{color}[{type.upper()}]{Style.RESET_ALL} {msg}")

    # Optionally send webhook
    if webhook:
        _send_webhook(msg)

def prwebhook(
    msg=None, 
    title=None, 
    color=None, 
    description=None, 
    fields=None, 
    webhook_url=None
    ):
    _send_webhook(msg, embeds=[
        {
            "title": title, 
            "color": color if color else 2818303, 
            "description": description, 
            "fields": fields
        }
    ], webhook_url=webhook_url)

def prinfo(msg, webhook=False): _print_log(msg, webhook=webhook)
def prsuccess(msg, webhook=False): _print_log(msg, color = Fore.GREEN, type = "success", webhook=webhook)
def prwarn(msg, webhook=False): _print_log(msg, color = Fore.YELLOW, type = "warning", webhook=webhook)
def prerror(msg, webhook=False): _print_log(msg, color = Fore.RED, type = "error", webhook=webhook)

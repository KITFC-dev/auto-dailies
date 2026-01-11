import requests
from src.config import Config
from colorama import Fore, Style

def _send_webhook(msg=None, embeds=None):
    # Skip if webhook url is empty
    if not (Config.webhook_url.strip()):
        return
    
    # Discord webhook
    payload = {}
    if msg:
        payload["content"] = msg
    if embeds:
        payload["embeds"] = embeds
    if Config.webhook_name:
        payload["username"] = Config.webhook_name
    if Config.webhook_avatar:
        payload["avatar_url"] = Config.webhook_avatar

    # Send webhook
    r = requests.post(Config.webhook_url, json=payload, timeout=5)

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
    fields=None
):
    _send_webhook(msg, embeds=[
        {
            "title": title, 
            "color": color if color else 2818303, 
            "description": description, 
            "fields": fields
        }
    ])

def prinfo(msg): _print_log(msg)
def prsuccess(msg): _print_log(msg, color = Fore.GREEN, type = "success")
def prwarn(msg): _print_log(msg, color = Fore.YELLOW, type = "warning")
def prerror(msg): _print_log(msg, color = Fore.RED, type = "error")

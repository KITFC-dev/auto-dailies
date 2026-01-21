import requests
from src.config import CONFIG
from colorama import Fore, Style

def _send_webhook(msg=None, embeds=None):
    # Skip if webhook url is empty
    if not (CONFIG.webhook_url.strip()):
        return
    
    # Discord webhook
    payload = {}
    if msg:
        payload["content"] = msg
    if embeds:
        payload["embeds"] = embeds
    if CONFIG.webhook_name:
        payload["username"] = CONFIG.webhook_name
    if CONFIG.webhook_avatar:
        payload["avatar_url"] = CONFIG.webhook_avatar

    # Send webhook
    r = requests.post(CONFIG.webhook_url, json=payload, timeout=5)

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
def prdebug(msg): _print_log(msg, color = Fore.BLUE, type = "debug") if CONFIG.debug else None

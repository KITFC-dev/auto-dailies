import requests
from colorama import Fore, Style
from src.config import CONFIG

def diff_text(label: str, init_val: int, curr_val: int) -> str:
    """Generates a diff stylized text from id. """
    if init_val < curr_val:
        diff = '+'
    elif init_val > curr_val:
        diff = '-'
    else:
        diff = ' '

    return f"{diff} {label.title()}: {init_val} -> {curr_val}\n"

def _print_log(msg, color = Fore.CYAN, type = "info"):
    print(f"{color}[{type.upper()}]{Style.RESET_ALL} {msg}")

def build_summary(results: list) -> dict:
    return {
        "title": "AutoDailies tasks completed!",
        "color": 2818303,
        "description": (
            f"Accounts Done: `{len([r for r in results if r.success])}`\n"
            f"Accounts Failed: `{len([r for r in results if not r.success])}`\n\n"

            f"Earned Coins: `{sum(i.p.balance.coins - i.ip.balance.coins for i in results if i.success)}`\n"
            f"Earned Gold: `{sum(i.p.balance.gold - i.ip.balance.gold for i in results if i.success)}`\n"

            f"All Coins: `{sum(i.all_coins for i in results if i.success)}`\n"
            f"All Gold: `{sum(i.all_gold for i in results if i.success)}`\n\n"

            f"Reached Gold Target: {', '.join([i.p.username for i in results if i.has_reached_target_gold]) or 'None'}"
        )
    }

def build_accounts_summary(results: list) -> dict:
    fields = []
    accounts = {
        "title": "Accounts Summary",
        "color": 2818303,
        "fields": fields
    }

    # Construct accounts summary
    for r in results:
        value = ""
        value += "```diff\n"
        if r.checkin:
            value += (
                f"Streak: {r.checkin.streak} | "
                f"M: {r.checkin.monthly_bonus * 100}% | "
                f"P: {r.checkin.payments_bonus * 100}%\n"
                f"{'Day was skipped! | ' if r.checkin.skipped_day else ''}"
                f"{'(failed)' if not r.checkin.success else ''}"
            )
        if r.cases:
            value += (
                f"Cases opened: "
                f"{r.cases.opened_cases}/{len(r.cases.available_cases)} "
                f"({r.cases.ignored_cases} ignored)\n"
                f"{'(failed)' if not r.cases.success else ''}"
            )
        if r.giveaway:
            value += (
                f"Giveaways joined: "
                f"{len(r.giveaway.joined)}/{len(r.giveaway.giveaways)}\n"
                f"{'(failed)' if not r.giveaway.success else ''}"
            )
        value += (
            f"All Coins: {r.all_coins} | All Gold: {r.all_gold}\n"
            "Inventory value:\n"
            f"{diff_text('coins', r.ip.inventory_meta.all_coins, r.p.inventory_meta.all_coins)}"
            f"{diff_text('gold', r.ip.inventory_meta.all_gold, r.p.inventory_meta.all_gold)}"
            "Balance:\n"
            f"{diff_text('coins', r.ip.balance.coins, r.p.balance.coins)}"
            f"{diff_text('gold', r.ip.balance.gold, r.p.balance.gold)}"
        )
        value += "```\n"

        fields.append({
            "name": f"{r.p.username} ({r.p.id})",
            "value": value,
            "inline": False,
        })

    return accounts

def build_notification(results: list):
    notification = {}
    notification['summary'] = build_summary(results)
    notification['accounts'] = build_accounts_summary(results)
    return notification

def send_discord(notification: dict):
    payload = {}
    payload["embeds"] = [notification['summary'], notification['accounts']]
    if CONFIG.webhook_name:
        payload["username"] = CONFIG.webhook_name
    if CONFIG.webhook_avatar:
        payload["avatar_url"] = CONFIG.webhook_avatar

    r = requests.post(CONFIG.webhook_url, json=payload, timeout=5)
    if not r.ok:
        prerror(f"Failed to send webhook: {r.status_code} {r.text}")

def send_notifications(results: list):
    notification = build_notification(results)
    if CONFIG.webhook_url:
        send_discord(notification)

def prinfo(msg): _print_log(msg)
def prsuccess(msg): _print_log(msg, color = Fore.GREEN, type = "success")
def prwarn(msg): _print_log(msg, color = Fore.YELLOW, type = "warning")
def prerror(msg): _print_log(msg, color = Fore.RED, type = "error")
def prdebug(msg): _print_log(msg, color = Fore.BLUE, type = "debug") if CONFIG.debug else None

import requests
import re

from colorama import Fore, Style
from src.config import CONFIG

def _print_log(msg, color = Fore.CYAN, type = "info"):
    print(f"{color}[{type.upper()}]{Style.RESET_ALL} {msg}")

def prinfo(msg): _print_log(msg)
def prsuccess(msg): _print_log(msg, color = Fore.GREEN, type = "success")
def prwarn(msg): _print_log(msg, color = Fore.YELLOW, type = "warning")
def prerror(msg): _print_log(msg, color = Fore.RED, type = "error")
def prdebug(msg): _print_log(msg, color = Fore.BLUE, type = "debug") if CONFIG.debug else None

class Notifications:
    def __init__(self, results: list):
        self.results = results

        self.summary = self._build_summary()
        self.accounts_summary = self._build_accounts_summary()

    def send_all(self):
        if CONFIG.webhook_url:
            self._send_discord()
        if CONFIG.telegram_token and CONFIG.telegram_chat_id:
            self._send_telegram()

    def _send_discord(self):
        fields = self.accounts_summary["fields"]
        chunks = [
            fields[i:i + 25]
            for i in range(0, len(fields), 25)
        ]

        for i, chunk in enumerate(chunks):
            payload = {}
            accounts = {**self.accounts_summary, "fields": chunk}
            if i == 0:
                payload["embeds"] = [self.summary, accounts]
            else:
                payload["embeds"] = [accounts]

            if CONFIG.webhook_name:
                payload["username"] = CONFIG.webhook_name
            if CONFIG.webhook_avatar:
                payload["avatar_url"] = CONFIG.webhook_avatar

            r = requests.post(CONFIG.webhook_url, json=payload, timeout=5)
            if not r.ok:
                prerror(f"Failed to send Discord webhook: {r.status_code} {r.text}")

    def _send_telegram(self):
        fields = self.accounts_summary["fields"]
        chunks = [
            fields[i:i + 10]
            for i in range(0, len(fields), 10)
        ]

        for i, chunk in enumerate(chunks):
            data = {}
            data["chat_id"] = CONFIG.telegram_chat_id
            accounts = self.embed2text({"title": "", "description": "", "fields": chunk})
            if i == 0:
                data["text"] = (
                    f"{self.embed2text(self.summary)}\n\n" +
                    f"{accounts}"
                )
            else:
                data["text"] = accounts
            
            data["parse_mode"] = "MarkdownV2"

            r = requests.post(
                f"https://api.telegram.org/bot{CONFIG.telegram_token}/sendMessage",
                data=data,
                timeout=5
            )
            if not r.ok:
                prerror(f"Failed to send Telegram message: {r.status_code} {r.text}")

    def _build_summary(self) -> dict:
        results = self.results
        d = f"Accounts Done: `{len([r for r in results if r.success])}/{len(results)}`\n"

        if any(r for r in results if not r.success):
            d += "Failed Accounts:"
            for r in results:
                if not r.success and r.reason is not None:
                    d += f"\n{r.reason}"
            d += "\n\n"
        d += (
            f"Earned Coins: `{sum(i.p.balance.coins - i.ip.balance.coins for i in results if i.success)}`\n"
            f"Earned Gold: `{sum(i.p.balance.gold - i.ip.balance.gold for i in results if i.success)}`\n"
            f"All Coins: `{sum(i.all_coins for i in results if i.success)}`\n"
            f"All Gold: `{sum(i.all_gold for i in results if i.success)}`\n\n"
        )
        if any(i for i in results if i.has_reached_target_gold):
            d += (
                f"Reached target for gold: {', '.join([i.p.username for i in results if i.has_reached_target_gold])}"
            )

        return {
            "title": "AutoDailies tasks completed!",
            "color": 2818303,
            "description": d,
        }

    def _build_accounts_summary(self) -> dict:
        results = self.results
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
            value += (
                f"Coins: {r.all_coins} | Gold: {r.all_gold}\n"
            )
            if r.checkin:
                value += (
                    f"Streak: {r.checkin.streak} "
                    f"| M: {r.checkin.monthly_bonus * 100}% "
                    f"| P: {r.checkin.payments_bonus * 100}% "
                    f"{'| Day was skipped! ' if r.checkin.skipped_day else ' '}"
                    f"{'(failed)' if not r.checkin.success else ''}"
                    f"\n"
                )
            if r.cases:
                value += (
                    f"Cases opened: "
                    f"{r.cases.opened_cases}/{len(r.cases.available_cases)} "
                    f"({r.cases.ignored_cases} ignored) "
                    f"{'(failed)' if not r.cases.success else ''}"
                    f"\n"
                )
            if r.giveaway:
                value += (
                    f"Giveaways joined: "
                    f"{len(r.giveaway.joined)}/{len(r.giveaway.giveaways)} "
                    f"{'(failed)' if not r.giveaway.success else ''}"
                    f"\n"
                )
            if len(r.p.inventory_meta.sold_items) > 0:
                value += (
                    f"Sold items ({len(r.p.inventory_meta.sold_items)}): {', '.join(r.p.inventory_meta.sold_items)} "
                    f"\n"
                )
            value += (
                "Inventory value:\n"
                f"{self._diff_text('coins', r.ip.inventory_meta.all_coins, r.p.inventory_meta.all_coins)}"
                f"{self._diff_text('gold', r.ip.inventory_meta.all_gold, r.p.inventory_meta.all_gold)}"
                "Balance:\n"
                f"{self._diff_text('coins', r.ip.balance.coins, r.p.balance.coins)}"
                f"{self._diff_text('gold', r.ip.balance.gold, r.p.balance.gold)}"
                f"{self._diff_text('rice', r.ip.rice, r.p.rice)}"
            )
            value += "```\n"

            fields.append({
                "name": f"{r.p.username} ({r.p.id})",
                "value": value,
                "inline": False,
            })

        return accounts

    def _diff_text(self, label: str, init_val: int, curr_val: int) -> str:
        """Generates a diff stylized text. """
        if init_val is not None and curr_val is not None:
            if init_val < curr_val:
                diff = '+'
                change = f"{init_val} -> {curr_val}"
            elif init_val > curr_val:
                diff = '-'
                change = f"{init_val} -> {curr_val}"
            else:
                diff = ' '
                change = f"{curr_val}"

            return f"{diff} {label.title()}: {change}\n"

        return ""

    def _md(self, text: str) -> str:
        """Escapes markdown characters in text. """
        parts = re.split(r"(```.*?```|`.*?`)", text, flags=re.DOTALL)
        escaped = [
            # Skip code blocks
            part if part.startswith("```") or part.startswith("`") else re.sub(r'([_*\[\]()~>#+\-=|{}.!])', r'\\\1', part)
            for part in parts
        ]
        return "".join(escaped)

    def embed2text(self, embed: dict) -> str:
        """Convert discord embed to markdown text for telegram. """
        text = (
            f"*{self._md(embed.get('title', ''))}*\n"
            f"{self._md(embed.get('description', ''))}"
        )

        # Convert fields
        for field in embed.get('fields', []):
            text += (
                f"*{self._md(field['name'])}*\n"
                f"{self._md(field['value'])}"
            )
        
        return text

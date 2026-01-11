import os
import tomllib
import argparse

class Config:
    def __init__(self, config_path: str = "config.toml"):
        args = self.parse_args()
        raw = self.load_toml(args.config_path or config_path)

        flags = raw.get("flags", {})
        self.headless = args.headless or flags.get("headless", False)
        self.checkin = args.checkin or flags.get("checkin", False)
        self.giveaway = args.giveaway or flags.get("giveaway", False)
        self.cases = args.cases or flags.get("cases", False)

        general = raw.get("general", {})
        self.wait_timeout = general.get("wait_timeout", 2)
        self.wait_after = args.wait_after if args.wait_after is not None else general.get("wait_timeout", 2)
        self.giveaway_price_threshold = general.get("giveaway_price_threshold", 0)
        self.case_price_threshold = general.get("case_price_threshold", 0)

        paths = raw.get("paths", {})
        self.chromium_path = args.chromium_path or os.path.abspath(paths.get("chromium_path", ""))
        self.chromedriver_path = args.chromedriver_path or os.path.abspath(paths.get("chromedriver_path", ""))
        self.accounts_dir = paths.get("accounts_file", "accounts")
        self.accounts = self.load_accounts()

        discord = raw.get("discord", {})
        self.webhook_url = args.webhook_url or discord.get("webhook_url", "")
        self.webhook_name = discord.get("profile_name", "")
        self.webhook_avatar = discord.get("profile_avatar", "")

        # For new pkl files
        self.new_account = args.new_account
        if self.new_account:
            self.accounts[self.new_account] = f"{self.accounts_dir}/{self.new_account}"

        self.validate_paths()

    def load_toml(self, user_config: str) -> dict:
        # Check if config file exists
        if not os.path.exists(user_config):
            raise FileNotFoundError(f"Config file not found: {user_config}")

        # Read config file
        with open(os.path.abspath(user_config), "rb") as f:
            return tomllib.load(f)

    def load_accounts(self) -> dict[str, str]:
        return {
            name: f"{self.accounts_dir}/{name}"
            for name in os.listdir("accounts")
            if name.endswith(".pkl")
        }

    def validate_paths(self):
        if not os.path.exists(self.chromium_path):
            raise FileNotFoundError(f"Chromium binary not found: {self.chromium_path}")

        if not os.path.exists(self.chromedriver_path):
            raise FileNotFoundError(f"Chromedriver not found: {self.chromedriver_path}")

    def parse_args(self) -> argparse.Namespace:
        """ Parse config options for AutoDailies. """
        parser = argparse.ArgumentParser(description="AutoDailies")

        # Flags
        parser.add_argument("-H", "--headless", action="store_true", help="Starts the browser in headless mode.")
        parser.add_argument("-c", "--checkin", action="store_true", help="Runs the daily check-in.")
        parser.add_argument("-g", "--giveaway", action="store_true", help="Runs the giveaway.")
        parser.add_argument("-cs", "--cases", action="store_true", help="Opens the cases.")

        # General
        parser.add_argument("-w", "--wait-after", type=int, help="Number of seconds to wait before closing the browser.")

        # Discord
        parser.add_argument("--webhook_url", type=str, help="Discord webhook URL to send logs to.")

        # Paths
        parser.add_argument("--chromium_path", type=str, help="Path to the browser binary.")
        parser.add_argument("--chromedriver_path", type=str, help="Path to the Chromedriver.")
        parser.add_argument("--config_path", type=str, help="Path to the config file.")
        
        # For new pkl files
        parser.add_argument("--new_account", type=str, help="Name of the new account's pkl file with extension (e.g. 'name.pkl').")

        return parser.parse_args()

CONFIG: Config = Config()

# URLs for pages on the website
BASE_URL: str = "https://genshindrop.io"
CHECKIN_URL: str = f"{BASE_URL}/checkin"
GIVEAWAY_URL: str = f"{BASE_URL}/give"
PROFILE_URL: str = f"{BASE_URL}/profile"

# HTML elements
ELEMENTS = {
    # Checkin
    "daily_checkin_button": 'checkin-day-today-label-check',
    
    # Giveaway
    "giveaway_box": 'panel give-box col-12 --genshin',
    "giveaway_free_label": 'give-free',
    "giveaway_paid_label": 'give-pay',
    "giveaway_price": 'give-pay_price__value',
    "giveaway_join_button": 'btn btn-gen btn-md w-100',

    # Common
    "button_confirm": 'swal-button swal-button--confirm',

    # Balance
    "balance_label": 'user_mor_value',
    "coins_label": 'user_coin_value',

    # Cases
    "case_box": "index-cat-container",
    "case": "index-case",
    "case_image": "index-case_cover",
    "case_name": "index-case_name",
    "case_price": "index-case_price",

    "case_requirements": "give-requirements-list",
    "case_requirement": "give-requirements-list_item__text",
    "case_coin_price_id": "чайник",

    "case_card_list": "box-page-loot-cards",
    "case_card": "box-page-loot-cards-card",

    # Profile info
    "profile_panel_box": 'profile-account-panel',
    "name": "mainUsernameValue",

    "profile_data_box": 'profile-user-data',
    "id": "mr-1",
    "avatar": "profile-avatar",
    "is_verified": "profile-verified_icon true"
}

# Cases to ignore when opening cases
IGNORE_CASES = [
    "druzeskii-keis",
    "nescatnaya-paimon",
    "bednaya-mona",
    "korobka-vezuncika",
    "vse-ili-nicego",
    "damaznaya-udaca",
    "korobka-inadzumy",
    "dar-arxontov",
    "pokrovitelstvo-dilyuka"
]
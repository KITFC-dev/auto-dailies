import os

# URLs for pages on the website
BASE_URL: str = "https://genshindrop.io"
CHECKIN_URL: str = f"{BASE_URL}/checkin"
GIVEAWAY_URL: str = f"{BASE_URL}/give"
PROFILE_URL: str = f"{BASE_URL}/profile"

# Paths for browser binary and chromedriver
CHROMIUM_PATH: str = "res/chromium/chrome"
CHROMEDRIVER_PATH: str = "res/chromedriver"

# Settings
# Amount of time to wait for the elements to load
WAIT_TIMEOUT: int = 2
# Price threshold for joining giveaways, if threshold is 1, 
# it will join all giveaways with price 1 or less.
GIVEAWAY_PRICE_THRESHOLD: int = 0
# Price threshold for opening cases, same logic as in giveaways
# using 1 as threshold because weekly case usually costs 1 coin.
CASE_PRICE_THRESHOLD: int = 1

# Discord Webhook Settings
# URL to send logs to
webhook_url: str = ""
# Profile name and avatar for webhook messages
WEBHOOK_PROFILE_NAME: str = ""
WEBHOOK_PROFILE_AVATAR: str = ""


# Paths for account pickle files with cookies
ACCOUNTS = {
    name: f"accounts/{name}"
    for name in os.listdir("accounts")
}

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
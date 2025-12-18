import os

# URLs for pages on the website
BASE_URL = "https://genshindrop.io"
CHECKIN_URL = f"{BASE_URL}/checkin"
GIVEAWAY_URL = f"{BASE_URL}/give"
PROFILE_URL = f"{BASE_URL}/profile"

# Paths for browser binary and chromedriver
CHROMIUM_PATH = "res/chromium/chrome.exe"
CHROMEDRIVER_PATH = "res/chromedriver.exe"

# Settings
# Price threshold for joining giveaways, if threshold is 1, 
# it will join all giveaways with price 1 or less.
PRICE_THRESHOLD = 0
# Discord webhook url to send logs to
# this one is not working btw, just an example
WEBHOOK_URL = "https://discord.com/api/webhooks/1450977245433827330/Jj_iswT_Vv2ZQw9-pg1rLaRpwbY8ZWwbCNeQOZsjZ5LAZICBcAVUBgCfhNtINvf72AOg"

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

    # Profile info
    "profile_panel_box": 'profile-account-panel',
    "name": "mainUsernameValue",

    "profile_data_box": 'profile-user-data',
    "id": "mr-1",
    "avatar": "profile-avatar",
    "is_verified": "profile-verified_icon true"

}

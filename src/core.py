from src.browser import create_driver, load_cookies, save_cookies
from src.logger import prinfo, prsuccess, prerror, prwebhook
from src.actions.checkin import run_daily_checkin
from src.actions.giveaway import run_giveaway
from src.actions.case import get_cases, open_case
from src.actions.state import run_get_balance, run_get_profile
from src.common import random_sleep, diff_text
from src.config import CONFIG
from src.constants import BASE_URL

def run_once(cookie_file):
    """Logs in to the website using the given cookie file and runs given actions. """
    driver = create_driver()
    driver.get(BASE_URL)

    res = {}

    # Load cookies to browser
    if cookie_file.split("/")[-1] != CONFIG.new_account:
        if not load_cookies(driver, cookie_file):
            prerror(f"No cookie file: {cookie_file}")
            return False
    else:
        prinfo(f"New account: {cookie_file}, waiting 90 seconds for user to log in...")
        random_sleep(90, 0)
        save_cookies(driver, cookie_file)

    driver.refresh()

    # Verify if login was successful
    balance = run_get_balance(driver)
    if balance is None:
        prerror(f"Failed to get balance, the login may have failed. Skipping {cookie_file}")
        driver.quit()
        return False
    
    # Save initial state
    res["initial"] = {}
    res["initial"]["coins"] = balance.coins
    res["initial"]["gold"] = balance.gold
    res["initial"]["profile"] = run_get_profile(driver)

    # Run actions
    if CONFIG.checkin:
        run_daily_checkin(driver)
    if CONFIG.giveaway:
        run_giveaway(driver)
    if CONFIG.cases:
        available_cases = get_cases(driver)
        res["available_cases"] = len(available_cases)
        res["opened_cases"] = 0
        res["ignored_cases"] = 0
        for case in available_cases:
            # Skip ignored cases
            if not case.is_ignored:
                if open_case(driver, case.link):
                    prsuccess(f"Opened case: {case.name}")
                    res["opened_cases"] += 1
                    random_sleep(7)
            else:
                res["ignored_cases"] += 1

    # Build result
    balance = run_get_balance(driver)
    if balance:
        res["coins"] = balance.coins
        res["gold"] = balance.gold
    res["profile"] = run_get_profile(driver)

    # Wait before closing
    if CONFIG.wait_after > 0:
        prinfo(f"Waiting {CONFIG.wait_after} seconds before closing the browser...")
        random_sleep(CONFIG.wait_after, 0)

    # Cleanup
    save_cookies(driver, cookie_file)
    driver.quit()

    return res

def run():
    """
    Runs the main script
    """
    # Variables
    done_accounts = []
    failed_accounts = []
    account_results = []

    # Iterate over all accounts
    for name, cookie_file in CONFIG.accounts.items():
        if (name not in CONFIG.accounts if CONFIG.accounts else False):
            continue
        prinfo(f"Processing account: {name}")
        res = run_once(cookie_file)
        if res:
            done_accounts.append(name)
            account_results.append(res)
            prsuccess(f"Account {name} done")
        else:
            failed_accounts.append(name)
            prerror(f"Account {name} failed")

    # Send summary webhook
    prwebhook(
        title="Tasks completed!",
        description=(
            f"Accounts Done: {len(done_accounts)}\n"
            f"Accounts Failed: {len(failed_accounts)}\n\n"
            f"Earned Coins: {sum(i.get('coins', 0) - i['initial'].get('coins', 0) for i in account_results)}\n"
            f"Earned Gold: {sum(i.get('gold', 0) - i['initial'].get('gold', 0) for i in account_results)}"
        ),
        color=2818303,
        fields=[
            {
                "name": f"{res['profile'].username} ({res['profile'].id})",
                "value": (
                    f"```diff\n"

                    f"Inventory value: {res['initial']['profile'].inventory_meta.all_coins} "
                    f"-> {res['profile'].inventory_meta.all_coins} Coins, "
                    f"{res['initial']['profile'].inventory_meta.all_gold} "
                    f"-> {res['profile'].inventory_meta.all_gold} Gold\n"

                    f"{diff_text('coins', res)}"
                    f"{diff_text('gold', res)}"

                    f"Cases opened: {res.get('opened_cases', 0)}/{res.get('available_cases', 0)} ({res.get('ignored_cases', 0)} ignored)"

                    f"```\n"
                ),
                "inline": False,
            }
            for res in account_results
        ],
    )

    prsuccess("All Done!")
    return True

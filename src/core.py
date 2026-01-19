from src.browser import create_driver, load_cookies, save_cookies
from src.logger import prinfo, prsuccess, prerror, prwebhook
from src.actions.checkin import run_daily_checkin
from src.actions.giveaway import run_giveaway
from src.actions.case import get_cases, open_case
from src.actions.state import run_get_profile
from src.models import RunResult
from src.common import random_sleep, diff_text
from src.config import CONFIG
from src.constants import BASE_URL

def run_once(cookie_file) -> RunResult:
    """Logs in to the website using the given cookie file and runs given actions. """
    driver = create_driver()
    if driver.current_url != BASE_URL:
        driver.get(BASE_URL)

    # Load cookies to browser
    if cookie_file.split("/")[-1] != CONFIG.new_account:
        if not load_cookies(driver, cookie_file):
            driver.quit()
            return RunResult.fail(f"No cookie file: {cookie_file}")
    else:
        prinfo(f"New account: {cookie_file}, waiting 90 seconds for user to log in...")
        random_sleep(90, 0)
        save_cookies(driver, cookie_file)

    driver.refresh()

    # Verify if login was successful
    init_profile = run_get_profile(driver)
    if init_profile is None or init_profile.id == '':
        driver.quit()
        return RunResult.fail("Failed to get profile information")

    # Run actions
    if CONFIG.checkin:
        run_daily_checkin(driver)
    if CONFIG.giveaway:
        run_giveaway(driver)
    available_cases_len = 0
    opened_cases = 0
    ignored_cases = 0
    if CONFIG.cases:
        available_cases = get_cases(driver)
        available_cases_len = len(available_cases)
        for case in available_cases:
            # Skip ignored cases
            if not case.is_ignored:
                if open_case(driver, case.link):
                    prsuccess(f"Opened case: {case.name}")
                    opened_cases += 1
                    random_sleep(7)
            else:
                ignored_cases += 1

    curr_profile = run_get_profile(driver)
    if curr_profile is None or curr_profile.id == '':
        prerror(f"Failed to get profile information. Skipping {cookie_file}")
        driver.quit()
        return RunResult.fail("Failed to get profile information")

    # Wait before closing
    if CONFIG.wait_after > 0:
        prinfo(f"Waiting {CONFIG.wait_after} seconds before closing the browser...")
        random_sleep(CONFIG.wait_after, 0)

    # Cleanup
    save_cookies(driver, cookie_file)
    driver.quit()

    return RunResult(
        success=True,
        ip=init_profile,
        p=curr_profile,
        available_cases_len=available_cases_len,
        opened_cases=opened_cases,
        ignored_cases=ignored_cases,
    )

def run():
    """
    Runs the main script
    """
    # Variables
    done_accounts = []
    failed_accounts = []
    account_results: list[RunResult] = []

    # Iterate over all accounts
    for name, cookie_file in CONFIG.accounts.items():
        prinfo(f"Processing account: {name}")
        res = run_once(cookie_file)
        if res.success:
            done_accounts.append(name)
            account_results.append(res)
            prsuccess(f"Account {res.p.username} done")
        else:
            failed_accounts.append(name)
            prerror(f"Account {name} failed")

    # Send summary webhook
    prwebhook(
        title="Tasks completed!",
        description=(
            f"Accounts Done: {len(done_accounts)}\n"
            f"Accounts Failed: {', '.join(failed_accounts) if failed_accounts else 0}\n\n"
            f"Earned Coins: {sum(i.p.balance.coins - i.ip.balance.coins for i in account_results)}\n"
            f"Earned Gold: {sum(i.p.balance.gold - i.ip.balance.gold for i in account_results)}"
        ),
        color=2818303,
        fields=[
            {
                "name": f"{r.p.username} ({r.p.id})",
                "value": (
                    f"```diff\n"
                    f"Inventory value:\n"
                    f"{diff_text('coins', r.ip.inventory_meta.all_coins, r.p.inventory_meta.all_coins)}"
                    f"{diff_text('gold', r.ip.inventory_meta.all_gold, r.p.inventory_meta.all_gold)}"

                    f"Balance:\n"
                    f"{diff_text('coins', r.ip.balance.coins, r.p.balance.coins)}"
                    f"{diff_text('gold', r.ip.balance.gold, r.p.balance.gold)}"

                    f"Cases opened: {r.opened_cases}/{r.available_cases_len} ({r.ignored_cases} ignored)"
                    f"```\n"
                ),
                "inline": False,
            }
            for r in account_results
        ],
    )

    prsuccess("All Done!")
    return True

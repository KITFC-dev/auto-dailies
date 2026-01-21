from src.browser import create_driver, load_cookies, save_cookies
from src.logger import prinfo, prsuccess, prerror, prwebhook
from src.actions.checkin import run_daily_checkin
from src.actions.giveaway import run_giveaway
from src.actions.case import run_cases
from src.actions.profile import run_get_profile
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
        checkin = run_daily_checkin(driver)
        prinfo(f"Check-in result: {checkin.success}, Streak: {checkin.streak}, Monthly bonus: {checkin.monthly_bonus}, Payments bonus: {checkin.payments_bonus}, Skipped day: {checkin.skipped_day}, Earned: {checkin.earned}, Currency type: {checkin.currency_type}")
    if CONFIG.giveaway:
        run_giveaway(driver)
    if CONFIG.cases:
        cases = run_cases(driver)

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
        checkin=checkin if CONFIG.checkin else None,
        cases=cases if CONFIG.cases else None,
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
                    "```diff\n"
                    + (f"Streak: {r.checkin.streak} | M Bonus: {r.checkin.monthly_bonus * 100}% | P Bonus: {r.checkin.payments_bonus * 100}%\n" if r.checkin else "")
                    + (f"Cases opened: {r.cases.opened_cases}/{len(r.cases.available_cases)} ({r.cases.ignored_cases} ignored)\n" if r.cases else "")
                    + "Inventory value:\n"
                    + f"{diff_text('coins', r.ip.inventory_meta.all_coins, r.p.inventory_meta.all_coins)}"
                    + f"{diff_text('gold', r.ip.inventory_meta.all_gold, r.p.inventory_meta.all_gold)}"

                    + "Balance:\n"
                    + f"{diff_text('coins', r.ip.balance.coins, r.p.balance.coins)}"
                    + f"{diff_text('gold', r.ip.balance.gold, r.p.balance.gold)}"
                    + "```\n"
                ),
                "inline": False,
            }
            for r in account_results
        ],
    )

    prsuccess("All Done!")
    return True

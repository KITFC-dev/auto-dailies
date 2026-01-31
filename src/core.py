from src.browser import create_driver, load_cookies, save_cookies
from src.logger import prinfo, Notifications
from src.actions.checkin import run_daily_checkin
from src.actions.giveaway import run_giveaway
from src.actions.case import run_cases
from src.actions.profile import run_profile
from src.models import RunResult
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL

def run_once(cookie_file) -> RunResult:
    """Run specified actions for given pickle file. """
    driver = create_driver()
    if driver.current_url != BASE_URL:
        driver.get(BASE_URL)

    # Inject cookies into browser
    if cookie_file.split("/")[-1] != CONFIG.new_account:
        if not load_cookies(driver, cookie_file):
            driver.quit()
            return RunResult(False, f"No cookie file: {cookie_file}")
    else:
        prinfo(f"New account: {cookie_file}, waiting 90 seconds for user to log in...")
        random_sleep(90, 0)
        save_cookies(driver, cookie_file)
    driver.refresh()

    # Verify if login was successful
    init_profile = run_profile(driver, initial=True)
    if init_profile is None or init_profile.id == '':
        driver.quit()
        return RunResult(False, "Failed to get profile information")

    # Run actions
    if CONFIG.checkin:
        checkin = run_daily_checkin(driver)
    if CONFIG.giveaway:
        giveaway = run_giveaway(driver)
    if CONFIG.cases:
        cases = run_cases(driver)

    # Get profile information after actions
    curr_profile = run_profile(driver)
    if curr_profile is None or curr_profile.id == '':
        driver.quit()
        return RunResult(False, "Failed to get profile information")

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
        giveaway=giveaway if CONFIG.giveaway else None,
        cases=cases if CONFIG.cases else None,
    )

def run():
    results: list[RunResult] = []

    # Iterate over all accounts
    for file in CONFIG.accounts.values():
        prinfo(f"Processing cookie file: {file}")
        results.append(run_once(file))

    Notifications(results).send_all()

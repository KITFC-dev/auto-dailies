from selenium.webdriver.support.ui import WebDriverWait

from src.logger import prsuccess, prwarn
from src.common import get_swal, parse_num, click_el, handle_exceptions, \
    wait_for, find, parse_currency
from src.config import CONFIG
from src.constants import CHECKIN_URL, CheckinSelectors, Condition
from src.models import CheckinResult

@handle_exceptions(default=CheckinResult(success=False, reason="Failed to check in"))
def run_daily_checkin(driver) -> CheckinResult:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != CHECKIN_URL:
        driver.get(CHECKIN_URL)

    # Click checkin button
    button = wait_for(Condition.CLICKABLE, wait, CheckinSelectors.BUTTON)
    title = None
    checked_in = False
    if button:
        click_el(driver, button)
        prsuccess("Daily check-in button clicked")
        swal = get_swal(driver)
        if swal:
            checked_in = True
            swal.click_confirm()
            title = swal.title
    else:
        prwarn("No daily check-in button detected. Seems like you already checked in today")

    # Parse data
    streak = parse_num(find(driver, CheckinSelectors.STREAK))
    monthly_bonus = parse_num(find(driver, CheckinSelectors.MONTHLY_BONUS), is_percent=True)
    payments_bonus = parse_num(find(driver, CheckinSelectors.PAYMENTS_BONUS), is_percent=True)
    skipped_day = not bool(find(driver, CheckinSelectors.SKIP_AVAILABLE))

    # Earned and currency type from swal
    earned = parse_num(title)
    currency_type = parse_currency(title)

    return CheckinResult(
        success=checked_in,
        streak=streak if streak else 0,
        monthly_bonus=monthly_bonus if monthly_bonus else 0.0,
        payments_bonus=payments_bonus if payments_bonus else 0.0,
        skipped_day=skipped_day,
        earned=earned if earned else 0,
        currency_type=currency_type,
    )

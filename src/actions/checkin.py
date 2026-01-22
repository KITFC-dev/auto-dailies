from selenium.webdriver.support.ui import WebDriverWait

from src.locators import wait_for, find
from src.logger import prsuccess, prwarn, prerror
from src.common import random_sleep, get_swal, parse_num
from src.config import CONFIG
from src.constants import CHECKIN_URL, CheckinSelectors, Condition, CurrencyType
from src.models import CheckinResult

def run_daily_checkin(driver) -> CheckinResult:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != CHECKIN_URL:
        driver.get(CHECKIN_URL)

    try:
        button = wait_for(Condition.CLICKABLE, wait, CheckinSelectors.BUTTON)
        title = None
        checked_in = False
        if button:
            button.click()
            prsuccess("Daily check-in button clicked")
            random_sleep(0.5)
            swal = get_swal(driver)
            if swal:
                checked_in = True
                random_sleep(0.5)
                swal.click_confirm()
                title = swal.title
        else:
            prwarn("No daily check-in button detected. Seems like you already checked in today")

        streak_el = find(driver, CheckinSelectors.STREAK)
        monthly_bonus_el = find(driver, CheckinSelectors.MONTHLY_BONUS)
        payments_bonus_el = find(driver, CheckinSelectors.PAYMENTS_BONUS)
        skipped_day_el = find(driver, CheckinSelectors.SKIPPED_DAY_FALSE)

        # Earned and currency type from swal
        earned = 0
        currency_type = CurrencyType.UNKNOWN
        if title:
            earned = parse_num(title)
            if 'чайник' in title.lower():
                currency_type = CurrencyType.COIN
            elif 'мор' in title.lower():
                currency_type = CurrencyType.GOLD
        
        # Skipped day
        skipped_day = False
        if not skipped_day_el:
            skipped_day_el = find(driver, CheckinSelectors.SKIPPED_DAY_TRUE)
            if skipped_day_el:
                skipped_day = True

        return CheckinResult(
            success=checked_in,
            streak=parse_num(streak_el),
            monthly_bonus=parse_num(monthly_bonus_el, is_percent=True),
            payments_bonus=parse_num(payments_bonus_el, is_percent=True),
            skipped_day=skipped_day,
            earned=earned,
            currency_type=currency_type,
        )
    except Exception as e:
        prerror(f"Error while checking in daily: {e}")

    return CheckinResult(success=False, reason="Check-in failed due to exception")

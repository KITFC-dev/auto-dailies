import re

from selenium.webdriver.support.ui import WebDriverWait

from src.locators import wait_for, find
from src.logger import prsuccess, prwarn, prerror
from src.common import random_sleep, get_swal
from src.config import CONFIG
from src.constants import CHECKIN_URL, CheckinSelectors, Condition
from src.models import CheckinResult

def run_daily_checkin(driver) -> CheckinResult:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != CHECKIN_URL:
        driver.get(CHECKIN_URL)

    try:
        button = wait_for(Condition.CLICKABLE, wait, CheckinSelectors.BUTTON)
        if button:
            button.click()
            prsuccess("Daily check-in button clicked")
            checked_in = True
            random_sleep(0.5)
            get_swal(driver).click_confirm()
        else:
            prwarn("No daily check-in button detected. Seems like you already checked in today")
            checked_in = False
        streak_el = find(driver, CheckinSelectors.STREAK)
        monthly_bonus_el = find(driver, CheckinSelectors.MONTHLY_BONUS)
        payments_bonus_el = find(driver, CheckinSelectors.PAYMENTS_BONUS)
        skipped_day_el = find(driver, CheckinSelectors.SKIPPED_DAY_FALSE)
        # Streak
        streak = 0
        if streak_el:
            num = re.search(r'\d+', streak_el.text.strip())
            if num:
                streak = int(num.group())
        # Monthly bonus
        monthly_bonus = 0
        if monthly_bonus_el:
            num = re.search(r'\d+', monthly_bonus_el.text.strip())
            if num:
                monthly_bonus = float(num.group()) / 100
        # Payments bonus
        payments_bonus = 0
        if payments_bonus_el:
            num = re.search(r'\d+', payments_bonus_el.text.strip())
            if num:
                payments_bonus = float(num.group()) / 100
        # Skipped day
        skipped_day = False
        if not skipped_day_el:
            skipped_day_el = find(driver, CheckinSelectors.SKIPPED_DAY_TRUE)
            if skipped_day_el:
                skipped_day = True

        return CheckinResult(
            success=checked_in,
            streak=streak,
            monthly_bonus=monthly_bonus,
            payments_bonus=payments_bonus,
            skipped_day=skipped_day,
        )
    except Exception as e:
        prerror(f"Error while checking in daily: {e}")

    return CheckinResult(success=False, reason="Check-in failed due to exception")

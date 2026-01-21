import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from typing import overload, Literal

from src.locators import wait_for, find
from src.logger import prsuccess, prwarn, prerror
from src.common import random_sleep, get_swal
from src.config import CONFIG
from src.constants import CHECKIN_URL, CheckinSelectors, Condition, CurrencyType
from src.models import CheckinResult

def _extract_number(text: str) -> int:
    num = re.search(r'\d+', text)
    if num:
        return int(num.group())
    return 0

@overload
def _extract_value(el: WebElement | None, is_percent: Literal[True]) -> float: ...
@overload
def _extract_value(el: WebElement | None, is_percent: Literal[False] = False) -> int: ...
def _extract_value(el: WebElement | None, is_percent: bool = False) -> int | float:
    res = _extract_number(el.text.strip()) if el else 0
    if is_percent:
        res = float(res) / 100
    return res

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
            earned = _extract_number(title.strip())
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
            streak=_extract_value(streak_el),
            monthly_bonus=_extract_value(monthly_bonus_el, is_percent=True),
            payments_bonus=_extract_value(payments_bonus_el, is_percent=True),
            skipped_day=skipped_day,
            earned=earned,
            currency_type=currency_type,
        )
    except Exception as e:
        prerror(f"Error while checking in daily: {e}")

    return CheckinResult(success=False, reason="Check-in failed due to exception")

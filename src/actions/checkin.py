from selenium.webdriver.support.ui import WebDriverWait

from src.locators import wait_for
from src.logger import prsuccess, prwarn, prerror
from src.common import random_sleep
from src.config import CONFIG
from src.constants import CHECKIN_URL, CheckinSelectors, Condition

def run_daily_checkin(driver):
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(CHECKIN_URL)

    try:
        # Find and click checkin button
        button = wait_for(Condition.CLICKABLE, wait, CheckinSelectors.BUTTON)
        if button:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            random_sleep(0.3)
            button.click()
            prsuccess("Daily check-in button clicked")
        else:
            prwarn("No daily check-in button detected. Seems like you already checked in today")
            return True
    except Exception as e:
        prerror(f"Error while checking in daily: {e}")
        random_sleep(1)

    return False

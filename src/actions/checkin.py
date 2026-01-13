from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.logger import prsuccess, prwarn
from src.common import random_sleep
from src.config import CONFIG
from src.constants import CHECKIN_URL, CheckinSelectors

def run_daily_checkin(driver):
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(CHECKIN_URL)

    try:
        # Find and click checkin button
        button = driver.find_element(CheckinSelectors.BUTTON)
        wait.until(EC.presence_of_element_located(button))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        random_sleep(0.3)
        button.click()
        prsuccess("Daily check-in button clicked")
    except Exception:
        prwarn("No daily check-in button detected. Seems like you already checked in today")
        random_sleep(1)
        return False

    return True

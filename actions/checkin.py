import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import prsuccess, prwarn
from config import ELEMENTS, CHECKIN_URL

def run_daily_checkin(driver):
    wait = WebDriverWait(driver, 2)
    driver.get(CHECKIN_URL)

    try:
        # Find and click checkin button
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS["daily_checkin_button"])))
        button = driver.find_element(By.CLASS_NAME, ELEMENTS["daily_checkin_button"])
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.3)
        button.click()
        prsuccess("Daily check-in button clicked")
    except Exception:
        prwarn("No daily check-in button detected")
        return False

    return True

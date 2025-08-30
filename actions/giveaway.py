import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import prsuccess, prwarn, prinfo
from config import ELEMENTS, GIVEAWAY_URL

def run_giveaway(driver):
    """Checks out all giveaways on the giveaways main page """
    wait = WebDriverWait(driver, 5)
    driver.get(GIVEAWAY_URL)

    # Get all giveaways links
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "give-box__link")))

        link_elements = driver.find_elements(By.CLASS_NAME, "give-box__link")
        giveaway_hrefs = [element.get_attribute("href") for element in link_elements][:3]
    except Exception:
        prwarn("No giveaway box detected")
        return False

    # Check out giveaways
    for giveaway_href in giveaway_hrefs:
        if giveaway_href:
            prinfo(f"Checking out: {giveaway_href}")
            driver.get(giveaway_href)
            time.sleep(1)
            click_giveaway_join_button(driver)
        else:
            prwarn("No giveaway link found inside the box")
            return False

def click_giveaway_join_button(driver):
    try:
        join_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Участвовать')]"))
        )
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", join_button)
        
        # Check if giveaway is free
        try:
            price_element = driver.find_element(By.CLASS_NAME, ELEMENTS["giveaway_price"])
            price_text = price_element.text.strip()
            if price_text not in ["0", "Бесплатно", "Free"]:
                prwarn(f"Giveaway is PAID (Price: {price_text})")
                return False
        except Exception:
            prwarn("Could not determine giveaway price")
        
        # Click join button
        try:
            join_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", join_button)

        prsuccess("Giveaway join button clicked")
        time.sleep(0.5)
    except Exception:
        prwarn("No giveaway join button detected. Seems like you already joined this giveaway")
        return False

    return True
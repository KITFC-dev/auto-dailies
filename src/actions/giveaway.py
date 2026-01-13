from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.logger import prsuccess, prwarn, prinfo
from src.common import random_sleep
from src.config import CONFIG
from src.constants import GIVEAWAY_URL, GiveawaySelectors

def run_giveaway(driver):
    """Checks out all giveaways on the giveaways main page """
    wait = WebDriverWait(driver, CONFIG.wait_timeout+1)
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
    for i, giveaway_href in enumerate(giveaway_hrefs):
        if giveaway_href:
            prinfo(f"Checking out: giveaway #{i+1} {giveaway_href}")
            driver.get(giveaway_href)
            random_sleep(1)
            # Delay between giveaways if it was clicked
            if click_giveaway_join_button(driver):
                random_sleep(5)
        else:
            prwarn("No giveaway link found inside the box")
            return False

def click_giveaway_join_button(driver):
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    try:
        join_button = WebDriverWait(driver, CONFIG.wait_timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Участвовать')]"))
        )
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", join_button)
        
        # Check giveaway's price
        try:
            price_element = wait.until(
                EC.presence_of_element_located(GiveawaySelectors.PRICE)
            )
            price_text = price_element.text.strip()
            if price_text not in ["0", "Бесплатно", "Free"]:                
                # Check if price is above threshold
                try:
                    price_value = float(price_text)
                    if price_value > CONFIG.giveaway_price_threshold:
                        prwarn(f"Giveaway price ({price_value}) is above {CONFIG.giveaway_price_threshold}. Skipping.")
                        return False
                except ValueError:
                    prwarn(f"Value of PRICE_THRESHOLD is not a number: '{price_text}'. Skipping.")
                    return False
        except Exception:
            prwarn("Could not determine giveaway price")
        
        # Click join button
        try:
            join_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", join_button)

        prsuccess("Giveaway join button clicked")
        random_sleep(0.5)
    except TimeoutException:
        prwarn("No giveaway join button detected. Seems like you already joined this giveaway")
        return False

    return True

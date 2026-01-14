from selenium.webdriver.support.ui import WebDriverWait

from src.locators import wait_for, find
from src.logger import prsuccess, prwarn, prinfo, prerror
from src.common import random_sleep
from src.config import CONFIG
from src.constants import GIVEAWAY_URL, GiveawaySelectors, Condition

def run_giveaway(driver):
    """Checks out all giveaways on the giveaways main page """
    wait = WebDriverWait(driver, CONFIG.wait_timeout+1)
    driver.get(GIVEAWAY_URL)

    try:
        # Wait for at least one giveaway to load, then get all giveaways
        wait_for(Condition.VISIBLE, wait, GiveawaySelectors.GIVEAWAY)
        giveaways = find(driver, GiveawaySelectors.GIVEAWAY, multiple=True)
        hrefs = []

        # Get all links to giveaways
        for giveaway in giveaways:
            link = find(giveaway, GiveawaySelectors.LINK)
            if link:
                hrefs.append(link.get_attribute("href"))
    
    except Exception as e:
        prerror(f"Error while getting giveaway links: {e}")
        return False

    # Join all giveaways
    for href in hrefs:
        prinfo(f"Checking out giveaway: {href}")
        random_sleep(1)
        if click_giveaway_join_button(driver, href):
            random_sleep(5)

    return True

def click_giveaway_join_button(driver, href):
    driver.get(href)
    wait = WebDriverWait(driver, CONFIG.wait_timeout)

    try:
        # Check if join button is present
        join_button = wait_for(Condition.CLICKABLE, wait, GiveawaySelectors.JOIN_BUTTON)
        if not join_button:
            prwarn("No giveaway join button detected. Seems like you already joined this giveaway")
            return False
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", join_button)
        
        # Check giveaway's price
        try:
            price_element = wait_for(Condition.PRESENCE, wait, GiveawaySelectors.PRICE)
            if price_element:
                price_text = price_element.text.strip()
                
                # Check if price is not free
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
            if join_button:
                join_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", join_button)

        prsuccess("Giveaway join button clicked")
        random_sleep(0.5)
    except Exception as e:
        prerror(f"Error while joining giveaway: {e}")
        return False

    return True

from selenium.webdriver.support.ui import WebDriverWait

from src.locators import wait_for, find
from src.config import CONFIG
from src.models import GiveawayResult
from src.logger import prsuccess, prwarn, prinfo, prerror
from src.common import random_sleep, get_swal, scroll_into
from src.constants import GIVEAWAY_URL, GiveawaySelectors, Condition

def run_giveaway(driver) -> GiveawayResult:
    """Checks out all giveaways on the giveaways main page. """
    wait = WebDriverWait(driver, CONFIG.wait_timeout+1)
    if driver.current_url != GIVEAWAY_URL:
        driver.get(GIVEAWAY_URL)

    try:
        # Wait for at least one giveaway to load, then get all giveaways
        wait_for(Condition.VISIBLE, wait, GiveawaySelectors.GIVEAWAY)
        giveaways = find(driver, GiveawaySelectors.GIVEAWAY, multiple=True)
        links = []

        # Get all links to giveaways
        for giveaway in giveaways:
            link = find(giveaway, GiveawaySelectors.LINK)
            if link:
                links.append(link.get_attribute("href"))
    
    except Exception as e:
        prerror(f"Error while getting giveaway links: {e}")
        return GiveawayResult(success=False, reason=str(e))

    # Join all giveaways
    joined = []
    for link in links:
        prinfo(f"Checking out giveaway: {link}")
        random_sleep(1)
        if click_giveaway_join_button(driver, link):
            joined.append(link)
            random_sleep(5)

    return GiveawayResult(
        success=True,
        giveaways=links,
        joined=joined
    )

def click_giveaway_join_button(driver, href) -> bool:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != href:
        driver.get(href)

    try:
        join_button = wait_for(Condition.CLICKABLE, wait, GiveawaySelectors.JOIN_BUTTON)
        if not join_button:
            prwarn("No giveaway join button detected. Seems like you already joined this giveaway")
            return False
        
        scroll_into(driver, join_button)
        
        # Check giveaway's price
        try:
            price_element = wait_for(Condition.PRESENCE, wait, GiveawaySelectors.PRICE)
            if price_element:
                price_text = price_element.text.strip()
                
                # Check if price is not free
                if price_text not in ["0", "Бесплатно", "Free"]:                
                    # Check if price is above threshold
                    price_value = int(price_text)
                    if price_value > CONFIG.giveaway_price_threshold:
                        prwarn(f"Giveaway price ({price_value}) is above {CONFIG.giveaway_price_threshold}. Skipping.")
                        return False
        except Exception:
            prwarn("Could not determine giveaway price")

        join_button.click()

        swal = get_swal(driver)
        if swal.title or swal.text:
            prsuccess("Giveaway join button clicked")
            random_sleep(0.5)
    except Exception as e:
        prerror(f"Error while joining giveaway: {e}")
        return False

    return True

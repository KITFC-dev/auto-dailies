from selenium.webdriver.support.ui import WebDriverWait

from src.config import CONFIG
from src.models import GiveawayResult
from src.logger import prsuccess, prwarn, prinfo, prdebug
from src.constants import GIVEAWAY_URL, GiveawaySelectors, Condition
from src.common import random_sleep, get_swal, parse_num, \
    handle_exceptions, click_el, wait_for, find

@handle_exceptions(default=GiveawayResult(success=False, reason="Failed to join giveaways"))
def run_giveaway(driver) -> GiveawayResult:
    """Checks out all giveaways on the giveaways main page. """
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != GIVEAWAY_URL:
        driver.get(GIVEAWAY_URL)

    # Wait for at least one giveaway to load, then get all giveaways
    wait_for(Condition.VISIBLE, wait, GiveawaySelectors.GIVEAWAY)
    giveaways = find(driver, GiveawaySelectors.GIVEAWAY, multiple=True)
    links = []
    for giveaway in giveaways:
        link = find(giveaway, GiveawaySelectors.LINK)
        if link:
            links.append(link.get_attribute("href"))

    # Join all giveaways
    joined = []
    for link in links:
        prinfo(f"Checking out giveaway: {link}")
        random_sleep(1)
        if join_giveaway(driver, link):
            joined.append(link)
            random_sleep(5)

    data = GiveawayResult(
        success=True,
        giveaways=links,
        joined=joined
    )
    prdebug(f"Giveaway result: {data}")
    return data

def join_giveaway(driver, href) -> bool:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    if driver.current_url != href:
        driver.get(href)

    # Wait for join button
    join_button = wait_for(Condition.CLICKABLE, wait, GiveawaySelectors.JOIN_BUTTON)
    if not join_button:
        prwarn("No giveaway join button detected. Seems like you already joined this giveaway")
        return False
        
    # Check giveaway's price
    price_element = wait_for(Condition.PRESENCE, wait, GiveawaySelectors.PRICE)
    if price_element:
        price = parse_num(price_element)
        if price:
            if price > CONFIG.giveaway_price_threshold:
                prwarn(f"Giveaway price ({price}) is above {CONFIG.giveaway_price_threshold}. Skipping.")
                return False
    else:
        prwarn(f"No giveaway price detected in {href}. Skipping.")
        return False

    # Join giveaway
    click_el(driver, join_button)
    swal = get_swal(driver)
    if swal.title or swal.text:
        prsuccess("Giveaway join button clicked")
        random_sleep(0.5)

    return True

import re
import random

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import wait_for, find
from src.logger import prinfo, prwarn
from src.common import random_sleep
from src.config import CONFIG
from src.constants import BASE_URL, CaseSelectors, Condition

def get_cases(driver):
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(BASE_URL)

    try:
        # Get cases box's elements in a container
        container = wait_for(Condition.PRESENCE, wait, CaseSelectors.BOX)
        cases = find(container, CaseSelectors.CASE, multiple=True)

        # Parse the data
        for case in cases:
            res = {}
            res["link"] = case.get_attribute("href")
            img = find(case, CaseSelectors.IMAGE)
            if img: 
                res["image"] = img.get_attribute("src")
            name = find(case, CaseSelectors.NAME)
            if name: 
                res["name"] = name.text
            price = find(case, CaseSelectors.PRICE)
            if price: 
                res["price"] = price.text

        return res
    except TimeoutException:
        prwarn("Couldn't find cases box element.")

    return []

def open_case(driver, case_link, card_idx=None):
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(case_link)

    try:
        # Wait until case cards are present
        wait.until(EC.presence_of_element_located(CaseSelectors.CARD_LIST))
        random_sleep(1)
        
        # Extract requirements for the case, this is needed
        # to check if the price is above the threshold.
        # NOTE: use find_elements to avoid exceptions. If not present,
        # we open the case anyway (there's no requirements).
        coin_price = None
        req_containers = driver.find_elements(*CaseSelectors.REQUIREMENTS)
        if req_containers:
            # Pick the first container with reqs
            req_container = req_containers[0]

            # Find all elements that have requirement text
            req_texts = req_container.find_elements(*CaseSelectors.REQUIREMENT)
            for req_text in req_texts:
                text = req_text.text.strip()
                # Check if the text contains coin price text which is 'чайник'
                if 'чайник' in text.lower():
                    # Extract numbers using regex
                    match = re.search(r'\d+', text)
                    if match:
                        case_price = int(match.group())

                        # Check if the price is above the threshold
                        if case_price > CONFIG.case_price_threshold:
                            prinfo(f"Case price ({case_price}) is higher than threshold ({CONFIG.case_price_threshold}), skipping...")
                            return False

        if coin_price is None:
            prinfo("No coin requirement found, opening the case anyway...")

        # Pick the card, but wait 3 seconds for the animation to finish
        random_sleep(3)
        cards = driver.find_elements(*CaseSelectors.CARD_LIST)
        if cards:
            card_el = cards[0]

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_el)

            # Find available cards
            available_cards = card_el.find_elements(*CaseSelectors.CARD)

            # Pick random card or the one specified
            if card_idx:
                picked_card = available_cards[card_idx]
            else:
                picked_card = random.choice(available_cards)

            # Click the card
            driver.execute_script("arguments[0].scrollIntoView(true);", picked_card)
            picked_card.click()

            return True
    except TimeoutException:
        prwarn(f"Couldn't find the case with link {case_link}.")

    return False

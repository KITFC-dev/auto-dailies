import time
import re
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import prinfo, prwarn
from config import ELEMENTS, BASE_URL, WAIT_TIMEOUT, CASE_PRICE_THRESHOLD

def get_cases(driver):
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    driver.get(BASE_URL)

    try:
        # Wait until cases box is present
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS["case_box"])))

        # Get cases box's elements
        cases_elements = container.find_elements(By.CLASS_NAME, ELEMENTS["case"])
        cases_data = []

        # Parse the data
        for case in cases_elements:
            link = case.get_attribute("href")
            img = case.find_element(By.CLASS_NAME, ELEMENTS["case_image"]).get_attribute("src")
            name = case.find_element(By.CLASS_NAME, ELEMENTS["case_name"]).text
            price = case.find_element(By.CLASS_NAME, ELEMENTS["case_price"]).text

            cases_data.append({
                "name": name,
                "price": price,
                "link": link,
                "image": img
            })

        return cases_data
    except Exception:
        prwarn("Couldn't find cases box element.")

    return []

def open_case(driver, case_link, card_idx=None):
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    driver.get(case_link)

    try:
        # Wait until case cards are present
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS["case_card_list"])))
        time.sleep(1)
        
        # Extract requirements for the case, this is needed
        # to check if the price is above the threshold.
        # NOTE: use find_elements to avoid exceptions. If not present,
        # we open the case anyway (there's no requirements).
        coin_price = None
        req_containers = driver.find_elements(By.CLASS_NAME, ELEMENTS["case_requirements"])
        if req_containers:
            # Pick the first container with reqs
            req_container = req_containers[0]

            # Find all elements that have requirement text
            req_texts = req_container.find_elements(By.CLASS_NAME, ELEMENTS["case_requirement"])
            for req_text in req_texts:
                text = req_text.text.strip()
                # Check if the text contains coin price
                if ELEMENTS['case_coin_price_id'].lower() in text.lower():
                    print(f"Coin price found: {text}")
                    # Extract numbers using regex
                    match = re.search(r'\d+', text)
                    if match:
                        case_price = int(match.group())
                        print(f"Case price found: {case_price}")

                        if case_price > CASE_PRICE_THRESHOLD:
                            prinfo(f"Case price ({case_price}) is higher than threshold ({CASE_PRICE_THRESHOLD}), skipping...")
                            return False

        if coin_price is None:
            prinfo("No coin/tea requirement found; opening case anyway.")

        # Pick the card, but wait 3 seconds for the animation to finish
        time.sleep(3)
        cards = driver.find_elements(By.CLASS_NAME, ELEMENTS["case_card_list"])
        if cards:
            card_el = cards[0]

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_el)

            # Find available cards
            available_cards = card_el.find_elements(By.CLASS_NAME, ELEMENTS["case_card"])

            # Pick random card or the one specified
            if card_idx:
                picked_card = available_cards[card_idx]
            else:
                picked_card = random.choice(available_cards)

            # Click the card
            driver.execute_script("arguments[0].scrollIntoView(true);", picked_card)
            picked_card.click()

            prinfo(f"Opened case {case_link}")
            return True
    except Exception:
        prwarn(f"Couldn't find the case with link {case_link}.")

    return False

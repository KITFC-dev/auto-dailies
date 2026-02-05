from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait

from src.common import handle_exceptions, wait_for, click_el, \
    switch_newtab, random_sleep, tab_exists, parse_text
from src.logger import prsuccess
from src.constants import LoginSelectors, CommonSelectors, Condition
from src.config import CONFIG
from src.constants import BASE_URL, PROFILE_URL

def get_secretcode(driver) -> str | None:
    """Get user secret code for verification in Telegram bot. """
    if driver.current_url != PROFILE_URL:
        driver.get(PROFILE_URL)

    driver.execute_script('$("#MySecretCode").modal("show");')
    random_sleep(2)
    return parse_text(
        wait_for(
            Condition.PRESENCE, 
            WebDriverWait(driver, CONFIG.wait_timeout), 
            LoginSelectors.SECRET_CODE
        )
    )

@handle_exceptions(default=False)
def run_login_tg(driver) -> bool:
    wait = WebDriverWait(driver, CONFIG.wait_timeout)
    driver.get(CONFIG.referral_url or BASE_URL)
    origin_tab = driver.current_window_handle
    
    # Click login
    button = wait_for(Condition.CLICKABLE, wait, LoginSelectors.LOGIN_BUTTON)
    if button:
        click_el(driver, button)

        # Pick telegram login
        tg_button = wait_for(Condition.CLICKABLE, wait, LoginSelectors.TG_LOGIN_BUTTON)
        if tg_button:
            click_el(driver, tg_button)
            
            # Switch to tab and iframe and click login
            tg_tab = switch_newtab(driver)
            tg_iframe = wait_for(Condition.PRESENCE, wait, CommonSelectors.IFRAME)
            if tg_iframe:
                driver.switch_to.frame(tg_iframe)
                click_el(driver, wait_for(Condition.CLICKABLE, wait, CommonSelectors.BUTTON))
                
                # Switch to telegram OAuth window and enter phone number
                oauth_tab = switch_newtab(driver)
                phone_input = wait_for(Condition.CLICKABLE, wait, LoginSelectors.TG_PHONE_INPUT)
                if phone_input:
                    # Clear country code
                    for i in range(4):
                        random_sleep(0.5)
                        phone_input.send_keys(Keys.BACKSPACE)
                    
                    # Enter phone number
                    phone_input.send_keys(str(CONFIG.new_account))
                    random_sleep(0.5)
                    phone_input.send_keys(Keys.ENTER)
                    
                    # Wait for confirmation from user and click confirm
                    while tab_exists(driver, oauth_tab):
                        try:
                            accept_btn = wait_for(Condition.CLICKABLE, wait, LoginSelectors.ACCEPT_BUTTON)
                            if accept_btn:
                                click_el(driver, accept_btn)
                                break
                        except Exception:
                            pass
                        random_sleep(0.5)
                    
                    # Switch back to tg login window to complete login
                    driver.switch_to.window(tg_tab)
                    button = wait_for(Condition.CLICKABLE, wait, CommonSelectors.BUTTON)
                    click_el(driver, button)
                    driver.close()
    
                    # Switch to original tab
                    driver.switch_to.window(origin_tab)
                    driver.refresh()
                    
                    prsuccess(f"Login successful, secret code: {get_secretcode(driver)}")
                    return True
    
    return False

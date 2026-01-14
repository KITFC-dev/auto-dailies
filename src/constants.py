from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functools import partial
from enum import Enum

__all__ = [
    "BASE_URL",
    "CHECKIN_URL",
    "GIVEAWAY_URL",
    "PROFILE_URL",
    "CommonSelectors",
    "CheckinSelectors",
    "GiveawaySelectors",
    "CaseSelectors",
    "StateSelectors",
    "Condition"
]

# Cases to ignore when opening cases
IGNORE_CASES = [
    "druzeskii-keis",
    "nescatnaya-paimon",
    "bednaya-mona",
    "korobka-vezuncika",
    "vse-ili-nicego",
    "damaznaya-udaca",
    "korobka-inadzumy",
    "dar-arxontov",
    "pokrovitelstvo-dilyuka"
]

BASE_URL: str = "https://genshindrop.io"
CHECKIN_URL: str = f"{BASE_URL}/checkin"
GIVEAWAY_URL: str = f"{BASE_URL}/give"
PROFILE_URL: str = f"{BASE_URL}/profile"

S = tuple[str, str]

class SelEnum(tuple, Enum):
    """Base class for selector enums"""
    @property
    def by(self) -> str: return self._value_[0]

    @property
    def val(self) -> str: return self._value_[1]

    def __new__(cls, value: S):
        obj = tuple.__new__(cls, value)
        obj._value_ = value
        return obj

    def __str__(self):
        return f"{self.value[0]}={self.value[1]}"

class CommonSelectors(SelEnum):
    """Selectors for common elements"""
    CONFIRM_BUTTON: S = (By.CLASS_NAME, 'swal-button swal-button--confirm')

class CheckinSelectors(SelEnum):
    """Selectors for check in page"""
    BUTTON = (By.CLASS_NAME, 'checkin-day-today-label-check')

class GiveawaySelectors(SelEnum):
    """Selectors for giveaway page"""
    LINKS: S = (By.CLASS_NAME, 'give-box__link')
    BOX: S = (By.CLASS_NAME, 'panel give-box col-12 --genshin')
    FREE_LABEL: S = (By.CLASS_NAME, 'give-free')
    PAID_LABEL: S = (By.CLASS_NAME, 'give-pay')
    PRICE: S = (By.CLASS_NAME, 'give-pay_price__value')
    JOIN_BUTTON: S = (By.CLASS_NAME, 'btn btn-gen btn-md w-100')

class CaseSelectors(SelEnum):
    """Selectors for cases"""
    BOX = (By.CLASS_NAME, 'index-cat-container')
    CASE = (By.CLASS_NAME, 'index-case')
    IMAGE = (By.CLASS_NAME, 'index-case_cover')
    NAME = (By.CLASS_NAME, 'index-case_name')
    PRICE = (By.CLASS_NAME, 'index-case_price')
    
    REQUIREMENTS = (By.CLASS_NAME, 'give-requirements-list')
    REQUIREMENT = (By.CLASS_NAME, 'give-requirements-list_item__text')
    
    CARD_LIST = (By.CLASS_NAME, 'box-page-loot-cards')
    CARD = (By.CLASS_NAME, 'box-page-loot-cards-card')

class StateSelectors(SelEnum):
    """Selectors for state information"""
    BALANCE = (By.CSS_SELECTOR, "span[data-key='user_mor_value']")
    COINS = (By.CSS_SELECTOR, "span[data-key='user_coin_value']")

    class Profile(SelEnum):
        """Profile page selectors"""
        PANEL_BOX: S = (By.CLASS_NAME, 'profile-account-panel')
        NAME: S = (By.CLASS_NAME, 'mainUsernameValue')
        
        DATA_BOX: S = (By.CLASS_NAME, 'profile-user-data')
        ID: S = (By.CLASS_NAME, 'mr-1')
        AVATAR: S = (By.CLASS_NAME, 'profile-avatar')
        IS_VERIFIED: S = (By.CLASS_NAME, 'profile-verified_icon true')

class Condition(Enum):
    PRESENCE = partial(EC.presence_of_element_located)
    CLICKABLE = partial(EC.element_to_be_clickable)
    VISIBLE = partial(EC.visibility_of_element_located)

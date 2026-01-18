from dataclasses import dataclass, field

from src.constants import CurrencyType

@dataclass(slots=True)
class Case:
    link: str
    is_ignored: bool
    image: str | None = None
    name: str | None = None
    price: str | None = None

@dataclass(slots=True)
class Balance:
    gold: int = 0
    coins: int = 0

@dataclass(slots=True)
class InventoryItem:
    image: str | None = None
    name: str | None = None
    price: int | None = None
    currency_type: CurrencyType = CurrencyType.UNKNOWN

@dataclass(slots=True)
class InventoryMeta:
    all_coins: int = 0
    all_gold: int = 0

@dataclass(slots=True)
class Profile:
    id: str
    avatar_url: str | None = None
    username: str | None = None
    rice: int | None = None
    is_verified: bool | None = None

    balance: Balance = field(default_factory=Balance)

    inventory: list[InventoryItem] = field(default_factory=list)

    @property
    def inventory_meta(self) -> InventoryMeta:
        coins = sum(i.price or 0 for i in self.inventory if i.currency_type is CurrencyType.COIN)
        gold = sum(i.price or 0 for i in self.inventory if i.currency_type is CurrencyType.GOLD)
        return InventoryMeta(coins, gold)

@dataclass
class RunResult:
    success: bool

    # Initial Profile
    ip: Profile = field(default_factory=lambda: Profile(id=''))
    # Profile
    p: Profile = field(default_factory=lambda: Profile(id=''))

    available_cases_len: int = 0
    opened_cases: int = 0
    ignored_cases: int = 0

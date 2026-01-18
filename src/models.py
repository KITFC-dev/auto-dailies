from dataclasses import dataclass, field
from typing import List

from src.constants import CurrencyType

@dataclass(slots=True)
class Case:
    link: str
    is_ignored: bool
    image: str | None = None
    name: str | None = None
    price: str | int | None = None

@dataclass(slots=True)
class Balance:
    balance: int
    coins: int

@dataclass(slots=True)
class InventoryItem:
    image: str | None = None
    name: str | None = None
    price: int | None = None
    currency_type: CurrencyType = CurrencyType.UNKNOWN

@dataclass(slots=True)
class InventoryMeta:
    all_coins: int = 0
    all_balance: int = 0

@dataclass(slots=True)
class Profile:
    id: str
    avatar_url: str | None = None
    username: str | None = None
    rice: int | None = None
    is_verified: bool | None = None

    inventory: List[InventoryItem] = field(default_factory=list)

    @property
    def inventory_meta(self) -> InventoryMeta:
        coins = sum(i.price or 0 for i in self.inventory if i.currency_type is CurrencyType.COIN)
        balance = sum(i.price or 0 for i in self.inventory if i.currency_type is CurrencyType.GOLD)
        return InventoryMeta(coins, balance)

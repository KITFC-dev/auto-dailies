from dataclasses import dataclass
from typing import List, Literal

@dataclass(slots=True)
class Case:
    link: str
    is_ignored: bool
    image: str | None = None
    name: str | None = None
    price: str | int | None = None

@dataclass
class Balance:
    balance: int
    coins: int

@dataclass
class InventoryItem:
    image: str | None = None
    name: str | None = None
    price: int = 0
    currency_type: Literal["coin", "mor", "unknown"] = "unknown"

@dataclass
class InventoryMeta:
    all_coins: int = 0
    all_balance: int = 0

@dataclass
class Profile:
    id: str
    avatar_url: str | None = None
    username: str | None = None
    rice: int | None = None
    is_verified: bool | None = None

    inventory: List[InventoryItem] | None = None
    inventory_meta: InventoryMeta | None = None

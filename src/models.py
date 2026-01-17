from dataclasses import dataclass

@dataclass(slots=True)
class Case:
    link: str
    is_ignored: bool
    image: str | None = None
    name: str | None = None
    price: str | int | None = None

from dataclasses import dataclass


@dataclass
class MarketOrder:
    price: float
    volume_remain: int

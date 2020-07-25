from dataclasses import dataclass


@dataclass
class MarketOrder:
    type_id: int
    order_type: str
    price: float
    volume_remain: int

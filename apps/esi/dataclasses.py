from dataclasses import dataclass


@dataclass
class MarketOrder:
    price: float
    volume_remain: int

    @property
    def total(self):
        return self.price * self.volume_remain

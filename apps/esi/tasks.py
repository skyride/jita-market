from collections import defaultdict
from typing import Dict, List

from jita.celery import app
from apps.sde.models import Region
from .api import get_region_orders, OrderType 
from .dataclasses import MarketOrder


@app.task
def update_region_prices(region_id: int):
    """
    Fetch and update pricing data for the region from ESI.
    """
    region: Region = Region.objects.get(id=region_id)

    # Fetch all pricing data from a region
    print(f"Fetching prices for {region.name}")
    orders: Dict[int, Dict[str, List[MarketOrder]]] = (
        defaultdict(lambda: defaultdict(list)))

    i = 1
    while True:
        response = get_region_orders(region_id, page=i).json()
        for order in response:
            order_type = OrderType.BUY if order['is_buy_order'] else OrderType.SELL
            orders[order['type_id']][order_type].append(MarketOrder(
                price=order['price'],
                volume_remain=order['volume_remain']))

        if i % 10 == 0:
            print(f"  Fetched page {i}")

        if len(response) < 1000:
            break
        i += 1

    
from collections import defaultdict
from typing import Dict, List
from operator import attrgetter

from django.db import transaction
from psqlextra.query import ConflictAction
from psqlextra.util import postgres_manager

from jita.celery import app
from apps.sde.models import Region, Type
from apps.pricing.models import RegionPrice
from .api import get_region_orders, OrderType 
from .dataclasses import MarketOrder


@app.task
@transaction.atomic
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

    # Iterate through types and upsert region pricing data
    print("Upserting region pricing data")
    price_objects: List[RegionPrice] = []
    for type_ in Type.objects.filter(market_group__isnull=False):
        # Buy
        buy: List[MarketOrder] = sorted(
            orders[type_.id][OrderType.BUY],
            key=attrgetter("price"),
            reverse=True)
        if len(buy) > 0:
            buy_volume = sum([order.volume_remain for order in buy])

            # Find the 95th percentile prices
            # We do this by calculating the index of the specific within an order
            # which will represent the 95th percentile, then iterating over the
            # orders until we find the one containing it.
            percentile_index = buy_volume * 0.05
            for order in buy:
                if order.volume_remain > percentile_index:
                    percentile_buy = order.price
                    break
                else:
                    percentile_index -= order.volume_remain
        else:
            buy_volume, percentile_buy = 0, 0

        sell: List[MarketOrder] = sorted(
            orders[type_.id][OrderType.SELL],
            key=attrgetter("price"))
        sell_volume = sum([order.volume_remain for order in sell])

        if len(sell) > 0:
            # Find the 95th percentile prices using the same method as buy
            percentile_index = sell_volume * 0.05
            for order in sell:
                if order.volume_remain > percentile_index:
                    percentile_sell = order.price
                    break
                else:
                    percentile_index -= order.volume_remain
        else:
            sell_volume, percentile_sell = 0, 0

        price_objects.append(RegionPrice(
            region=region,
            type=type_,
            max_buy=max([order.price for order in buy], default=0),
            max_sell=max([order.price for order in sell], default=0),
            min_buy=min([order.price for order in buy], default=0),
            min_sell=min([order.price for order in sell], default=0),
            average_buy=(
                sum([order.total for order in buy])
                / (sum([order.volume_remain for order in buy]) or 1.0)),
            average_sell=(
                sum([order.total for order in sell])
                / (sum([order.volume_remain for order in sell]) or 1.0)),
            percentile_buy=percentile_buy,
            percentile_sell=percentile_sell,
            buy_volume=buy_volume,
            sell_volume=sell_volume))
    
    # Clear database and repopulate with new objects
    RegionPrice.objects.filter(region=region).delete()
    RegionPrice.objects.bulk_create(price_objects)


@app.task
def schedule_region_price_updates(kspace_only: bool = True):
    """
    Schedules a price update task for every region.
    By default will only schedule kspace regions.
    """
    regions = Region.objects
    if kspace_only:
        # Filter to only k-space regions
        regions = regions.filter(id__lt=11000001)

    for region in regions.all():
        update_region_prices.delay(region_id=region.id)

    print(f"Scheduled price update tasks for {regions.count()} regions")

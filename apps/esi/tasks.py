from jita.celery import app

from apps.sde.models import Region
from .api import get_region_orders


@app.task
def update_region_prices(region_id: int):
    """
    Fetch and update pricing data for the region from ESI.
    """
    region: Region = Region.objects.get(id=region_id)

    # Fetch all pricing data from a region
    print(f"Fetching prices for {region.name}")
    i = 1
    prices = []
    while True:
        response = get_region_orders(region_id, page=i).json()
        prices.extend(response)

        if i % 10 == 0:
            print(f"  Fetched page {i}")

        if len(response) < 1000:
            break
        i += 1

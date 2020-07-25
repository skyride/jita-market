from jita.celery import app

from .api import get_region_orders


@app.task
def update_region_prices(region_id: int):
    """
    Fetch and update pricing data for the region from ESI.
    """
    i = 1
    prices = []
    while True:
        response = get_region_orders(region_id, page=i).json()
        prices.extend(response)
        print(i, len(response), len(prices))

        if len(response) < 1000:
            break
        i += 1

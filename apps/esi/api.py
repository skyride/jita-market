from typing import Optional

import requests

from .exceptions import ESIException


BASE_URL = "https://esi.evetech.net"


class OrderType:
    """
    A simple mapping of order types.
    """
    BUY = "buy"
    SELL = "sell"
    ALL = "all"


def get_region_orders(region_id: int,
                      order_type: Optional[str] = OrderType.ALL,
                      page: Optional[int] = 1,
                      type_id: Optional[int] = None) -> requests.Response:
    """
    Fetch a set of region orders from ESI.
    """
    params = {
        "order_type": order_type,
        "page": page}

    if type_id is not None:
        params['type_id'] = type_id
    
    response = requests.get(f"{BASE_URL}/latest/markets/{region_id}/orders/",
        params=params)
    return _process_response(response)


def _process_response(response: requests.Response) -> requests.Response:
    """
    Handle the response.
    """
    if response.status_code < 200 or response.status_code > 299:
        raise ESIException("%s returned http status code %s" % (
            response.url, response.status_code))

    return response

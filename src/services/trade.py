"""Trade service to get user's private account information and orders."""
from krakenex import API, connection

from models.asset import Asset
from models.order import Order


def krakenex_conn(func):
    """Decorate for kraken api calls."""
    def wrapper(*args, **kargs):
        """Login befor call apis."""
        conn = connection.Connection()
        client = API(conn=conn)
        client.load_key('secret/secret.txt')
        return func(client, *args, **kargs)
    return wrapper


def get_time(key):
    """Get timestamp for orders."""
    def get_key_time(order):
        """Open time for opened orders and closed time for others."""
        return order.get(key)
    return get_key_time


@krakenex_conn
def get_account_info(client):
    """Get user's balance info."""
    assets = []
    total = 0
    response = client.query_private('Balance', {})
    balance = response.get('result')
    if not balance:
        from app import sentry
        sentry.captureMessage(response.get('error'))
        return None, None

    # TODO:
    # Collect all paris used in balance and query them once together.
    pair_list = [asset + 'ZUSD' for asset in balance.keys() if asset[0] == 'X']
    response = client.query_public('Ticker', {'pair': ','.join(pair_list)})
    pair_price = response.get('result')
    for asset in balance.keys():
        if asset[0] == 'X':
            pair_name = asset + 'ZUSD'
            new_asset = Asset(asset, float(balance.get(asset)), float(
                pair_price.get(pair_name).get('c')[0])).to_dict()
        else:
            new_asset = Asset(asset, amount=float(balance.get(
                asset)), total=float(balance.get(asset))).to_dict()
        assets.append(new_asset)
        total += new_asset.get('total')
    return assets, total


@krakenex_conn
def get_orders(client, order_type):
    """Get user's orders info."""
    if order_type == 'open':
        endpoint, sort_key = 'OpenOrders', get_time('opened')
    else:
        endpoint, sort_key = 'ClosedOrders', get_time('closed')
    orders = []
    response = client.query_private(endpoint)
    order_list = response.get('result').get(order_type)
    for order_index, order in order_list.items():
        orders.append(Order(order_index, order).to_dict())
    return sorted(orders, key=sort_key, reverse=True)

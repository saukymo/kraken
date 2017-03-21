from math import floor
import moment
from krakenex import API, connection
from models.asset import Asset

def krakenex_conn(func):
	def wrapper():
		conn = connection.Connection()
		client = API(conn=conn)
		client.load_key('secret.txt')
		return func(client)
	return wrapper

@krakenex_conn
def get_account_info(client):
	assets = []
	total = 0
	balance = client.query_private('Balance', {}).get('result')
	for asset in balance.keys():
		if asset[0] == 'X':
			pair_name = asset + 'ZUSD'
			response = client.query_public('Ticker', {'pair': pair_name})
			price = response.get('result')
			new_asset = Asset(asset, float(balance.get(asset)), float(price.get(pair_name).get('c')[0])).to_dict()
		else:
			new_asset = Asset(asset, amount=float(balance.get(asset)), total=float(balance.get(asset))).to_dict()
		assets.append(new_asset)
		total += new_asset.get('total')
	return assets, total

@krakenex_conn
def get_open_order(client):
	open_orders = []
	open_order = client.query_private('OpenOrders').get('result').get('open')
	for order_index, order in open_order.items():
		descr = order.get('descr')
		pair = descr.get('pair')
		new_order = {
				'order_id': order_index.split('-')[0],
				'order_type': descr .get('type') + '/' + descr.get('ordertype'),
				'pair': pair[:3] + '/' + pair[3:],
				'price': descr.get('price'),
				'fee': order.get('fee'),
				'volumn': order.get('vol'),
				'cost': order.get('cost'),
				'status': order.get('status'),
				'opened': moment.unix(float(order.get('opentm')), utc=True).timezone("Asia/Shanghai").format("YYYY-M-D H:m:s")
			}
		open_orders.append(new_order)
	return sorted(open_orders, key=lambda order: order.get('closed'), reverse=True)

@krakenex_conn
def get_closed_order(client):
	closed_orders = []
	closed_order = client.query_private('ClosedOrders').get('result').get('closed')
	for order_index, order in closed_order.items():
		descr = order.get('descr')
		pair = descr.get('pair')
		new_order = {
				'order_id': order_index.split('-')[0],
				'order_type': descr .get('type') + '/' + descr.get('ordertype'),
				'pair': pair[:3] + '/' + pair[3:],
				'price': order.get('price'),
				'fee': order.get('fee'),
				'volumn': order.get('vol_exec'),
				'cost': order.get('cost'),
				'status': order.get('status'),
				'closed': moment.unix(float(order.get('closetm')), utc=True).timezone("Asia/Shanghai").format("YYYY-M-D H:m:s")
			}
		closed_orders.append(new_order)
	return sorted(closed_orders, key=lambda order: order.get('closed'), reverse=True)
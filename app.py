from flask import Flask, jsonify, render_template, g
from krakenex import API, connection
import sqlite3



from services.trade import get_account_info, get_closed_order, get_open_order

DATABASE= 'database.db'


app = Flask(__name__)
conn = connection.Connection()
client = API(conn=conn)
client.load_key('secret.txt')



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
	return "OK!"

@app.route("/account")
def get_account():
	assets, total = get_account_info()
	opened_orders = get_open_order()
	closed_orders = get_closed_order()
	return render_template('account.html', assets=assets, total=total, opened_orders=opened_orders, closed_orders=closed_orders)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
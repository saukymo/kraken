"""Web interface for Kraken account info."""
from flask import Flask, render_template
from flask_apscheduler import APScheduler

from services.database import DatabaseService
from services.trade import get_account_info, get_orders
from services.cronjob import CronjobService
from configs.config import Config

DATABASE = 'database.db'
app = Flask(__name__)

cronjob_service = CronjobService()
cron_job = cronjob_service.get_daily_balance

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
database_service = DatabaseService()
database_service.init_db()


@app.route("/")
def get_account():
    """Return account page."""
    assets, total = get_account_info()
    opened_orders = get_orders('open')
    closed_orders = get_orders('closed')
    return render_template(
        'account.html',
        assets=assets,
        total=total,
        opened_orders=opened_orders,
        closed_orders=closed_orders
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

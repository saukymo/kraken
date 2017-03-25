"""Web interface for Kraken account info."""
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from raven.contrib.flask import Sentry


from services.database import DatabaseService
from services.trade import get_account_info, get_orders
from services.cronjob import CronjobService
from configs.config import Config

DSN = """https://810a6bc6fd8546529ae6104d26096f2b:7178284"""\
    """885294fc6864015bd93ed4c60@sentry.io/151873"""
app = Flask(__name__)
sentry = Sentry(app, dsn=DSN)

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

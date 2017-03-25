"""Cronjob service for all cronjob using Apschedule."""
from services.trade import get_account_info
from services.database import DatabaseService, Balance


class CronjobService:
    """Class for cronjob service."""

    def __init__(self):
        """Create service object."""
        self.database_service = DatabaseService()

    def get_daily_balance(self):
        """Get balance every day."""
        from app import sentry

        db = self.database_service.get_db()
        db.connect()
        try:
            assets, total = get_account_info()
            Balance.create(total=total)
        except Exception as e:
            sentry.captureMessage(e)
        finally:
            db.close()

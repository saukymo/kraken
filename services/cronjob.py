"""Cronjob service for all cronjob using Apschedule."""
from services.trade import get_account_info
from services.database import DatabaseService, Balance
from playhouse.shortcuts import model_to_dict
# from app import get_db


class CronjobService:
    """Class for cronjob service."""

    def __init__(self):
        """Create service object."""
        self.database_service = DatabaseService()

    def get_daily_balance(self):
        """Get balance every day."""
        assets, total = get_account_info()
        db = self.database_service.get_db()
        db.connect()
        balance = Balance.create(total=total)
        print(model_to_dict(balance))
        db.close()

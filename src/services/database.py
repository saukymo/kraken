"""Database service using peewee."""
from peewee import DecimalField, DateTimeField, Model
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime


DATABASE = SqliteExtDatabase('database.db')


class DatabaseService:
    """Service for database."""

    def __init__(self):
        """Create service object."""
        self.db = DATABASE

    def get_db(self):
        """Return database connect."""
        return self.db

    def init_db(self):
        """Create database."""
        self.db.connect()
        self.db.create_tables([Balance], True)
        self.db.close()


class BaseModel(Model):
    """Base model for other models."""

    class Meta:
        """Base database connection."""

        database = DATABASE


class Balance(BaseModel):
    """Balance model."""

    total = DecimalField()
    created_date = DateTimeField(unique=True, default=datetime.datetime.now)

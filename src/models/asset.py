"""Class for model Asset."""


class Asset:
    """Class for Asset model."""

    def __init__(self, asset, amount=None, price=None, total=None):
        """Construct function for Asset."""
        self.asset = asset[1:]
        self.amount = amount
        self.price = price
        if amount and price:
            self.total = amount * price
        else:
            self.total = total

    def to_dict(self):
        """Dict output."""
        return {
            'asset': self.asset,
            'amount': self._format(self.amount),
            'price': self._format(self.price),
            'total': self._format(self.total),
        }

    @staticmethod
    def _format(val):
        """String format. Keep 4 digital and '---' if None."""
        if val:
            return round(val, 4)
        else:
            return '---'

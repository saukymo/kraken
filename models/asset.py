class Asset:

    def __init__(self, asset, amount=None, price=None, total=None):
        self.asset = asset[1:]
        self.amount = amount
        self.price = price
        if amount and price:
            self.total = amount * price
        else:
            self.total = total

    def to_dict(self):
        return {
            'asset': self.asset,
            'amount': self._format(self.amount),
            'price': self._format(self.price),
            'total': self._format(self.total),
        }

    @staticmethod
    def _format(val):
        if val:
            return round(val, 4)
        else:
            return '---'

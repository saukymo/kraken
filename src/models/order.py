"""Orders model."""
import moment


class Order:
    """Class of opened or closed orders in kraken."""

    def __init__(self, idx, obj):
        """
        Construct function for orders.

        @Param idx: order id.
        @Param obj: order info obj.
        """
        self.idx = idx
        self.obj = obj
        self.is_open = obj.get('status') == 'open'

    def to_dict(self):
        """Formated infomations in dict."""
        descr = self.obj.get('descr')
        pair = descr.get('pair')
        order_dict = {
            'order_id': self.idx.split('-')[0],
            'order_type': descr.get('type') + '/' + descr.get('ordertype'),
            'pair': pair[:3] + '/' + pair[3:],
            'price': self.get_price(),
            'fee': self.obj.get('fee'),
            'volume': self.obj.get('vol'),
            'cost': self.obj.get('cost'),
            'status': self.obj.get('status'),
        }
        if self.is_open:
            order_dict['opened'] = self.time_format(self.obj.get('opentm'))
        else:
            order_dict['closed'] = self.time_format(self.obj.get('closetm'))

        return order_dict

    @staticmethod
    def time_format(timestamp, timezone="Asia/Shanghai"):
        """Turn timestamp to local time formated string."""
        return moment \
            .unix(float(timestamp), utc=True) \
            .timezone(timezone) \
            .format("YYYY-M-D H:m:s")

    def get_price(self):
        """Open orders return expect price and others return exec price."""
        if self.is_open:
            return self.obj.get('descr').get('price')
        else:
            return self.obj.get('price')

    def get_volume(self):
        """Open orders return expect volume and others return exec volume."""
        if self.is_open:
            return self.obj.get('vol')
        else:
            return self.obj.get('vol_exec')

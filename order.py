import datetime

class Order:
    def __init__(self, id, ticker, type, quantity, price, classification, start, end, open=True, duration = 'N/A', pl = 'N/A', plpc='N/A'):
        self.id = id
        self.ticker = ticker
        self.type = type
        self.quantity = quantity
        self.price = price
        self.classification = classification
        self.start = datetime.now()
        self.open = open
        self.end = end
        self.duration = duration
        self.pl = pl
        self.plpc = plpc

    def close_order(self, end, pl, plpc):
        self.open = False
        self.end = end
        self.duration = self.end - self.start
        self.pl = pl
        self.plpc = plpc

    def __repr__(self):
        return f"id: {self.id},\nticker: {self.ticker},\ntype:{self.type},\nquantity:{self.quantity},\nprice:{self.price},\nprice:{self.classification},\nprice:{self.end},\nprice:{self.pl},\nprice:{self.plpc})"

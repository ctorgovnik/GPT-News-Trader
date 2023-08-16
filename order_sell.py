class OrderSell:
    def __init__(self, id, ticker, type, quantity, price, pl, pl_pct):
        self.id = id
        self.ticker = ticker
        self.type = type
        self.quantity = quantity
        self.price = price
        self.pl = pl
        self.pl_pct = pl_pct

    def __repr__(self):
        return f"id: {self.id},\nticker: {self.ticker},\ntype:{self.type},\nquantity:{self.quantity},\nprice:{self.price})"


class OrderBuy:
    def __init__(self, id, ticker, type, quantity, price, classification):
        self.id = id
        self.ticker = ticker
        self.type = type
        self.quantity = quantity
        self.price = price
        self.classification = classification

    def __repr__(self):
        return f"id: {self.id},\nticker: {self.ticker},\ntype:{self.type},\nquantity:{self.quantity},\nprice:{self.price})"


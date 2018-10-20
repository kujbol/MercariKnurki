class Transaction:

    def __init__(self, seller, buyer, price: float, fraud: bool):
        self.seller = seller
        self.buyer = buyer
        self.price = price
        self.fraud = fraud

    def __reversed__(self):
        return Transaction(
            self.buyer,
            self.seller,
            self.price,
            self.fraud
        )

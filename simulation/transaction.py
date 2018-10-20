class Transaction:
    def __init__(self, buyer, seller):
        self.buyer = buyer
        self.seller = seller

    def to_csv(self):
        result = {
            'buyer': str(self.buyer),
            'seller': str(self.seller),
            'value': 100,
            'was_fraud': None,
            'buyer_rating': None,
            'seller_rating': None,
        }

        assert len(result) == len(self.fields())
        return result

    @classmethod
    def fields(cls):
        return ['buyer', 'seller', 'value', 'was_fraud', 'buyer_rating', 'seller_rating']

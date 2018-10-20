from simulation.clients import User


class Transaction:
    def __init__(self, buyer: User, seller: User, value: float):
        self.buyer = buyer
        self.seller = seller
        self.value = value

    def to_csv(self):
        result = {
            'buyer': str(self.buyer.id),
            'seller': str(self.seller.id),
            'value': self.value,
            'was_fraud': self.seller.fraud,
            'buyer_rating': None,
            'seller_rating': None,
        }

        assert len(result) == len(self.fields())
        return result

    @classmethod
    def fields(cls):
        return ['buyer', 'seller', 'value', 'was_fraud', 'buyer_rating', 'seller_rating']

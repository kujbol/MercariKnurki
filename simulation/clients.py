import uuid
import random
import numpy as np


class User:
    def __init__(self, sell, buy, fraud):
        self.id = uuid.uuid4()

        self.sell = sell
        self.buy = buy
        self.fraud = fraud


class UserType:
    def __init__(self, sell_volume, buy_volume, fraud_probability=1e-3, mistake_probability=0.00001, volume_difference=0.4):
        self.sell_volume = sell_volume
        self.buy_volume = buy_volume
        self.volume_difference = volume_difference

        self.fraud_probability = fraud_probability
        self.mistake_probability = mistake_probability

    def generate_user(self):
        return User(
            buy=random.normalvariate(self.buy_volume, self.volume_difference),
            sell=random.normalvariate(self.sell_volume, self.volume_difference),
            fraud=np.random.binomial(1, self.fraud_probability, 1)[0]
        )


big_seller = UserType(
    sell_volume=1000,
    buy_volume=0,
    mistake_probability=0.0001,  # Higher chance of mistake probability
)

small_seller = UserType(
    sell_volume=50,
    buy_volume=5,
)

individual_buyer = UserType(
    sell_volume=10,
    buy_volume=10,
    volume_difference=1
)



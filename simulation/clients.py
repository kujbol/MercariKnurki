import uuid
import random


class User:
    def __init__(self, sell, buy,):
        self.id = uuid.uuid4()

        self.sell = sell
        self.buy = buy


class UserType:
    def __init__(self, sell_volume, buy_volume, fraud_propaility=0, mistake_propability=0.00001, volume_difference=0.4):
        self.sell_volume = sell_volume
        self.buy_volume = buy_volume
        self.volume_difference = volume_difference
        self.fraud_propability = fraud_propaility
        self.mistake_propability = mistake_propability

    def generate_user(self):
        return User(
            buy=self.buy_volume * random.uniform(1 - self.volume_difference, 1 + self.volume_difference),
            sell=self.sell_volume * random.uniform(1 - self.volume_difference, 1 + self.volume_difference),
        )


big_seller = UserType(
    sell_volume=1000,
    buy_volume=0,
    mistake_propability=0.0001,  # Higher chance of mistake probability
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



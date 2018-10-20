import random
import csv

from simulation.clients import big_seller, small_seller, individual_buyer, UserType
from simulation.transaction import Transaction

user_types_mapping = {
    big_seller: 1,
    small_seller: 10,
    individual_buyer: 100,
}


class Simulation:
    def __init__(self, user_types_mapping):
        self.user_types = user_types_mapping
        self.buyers = []
        self.sellers = []

    def run(self):
        self.generate_world()

        with open('transactions.csv', 'w') as trans:
            output = csv.DictWriter(trans, fieldnames=Transaction.fields())
            self.generate_transactions(output)

    def generate_world(self):
        for user_type, amount in self.user_types.items():
            for _ in range(amount):
                user = user_type.generate_user()
                if user.buy:
                    self.buyers.append(user)
                if user.sell:
                    self.sellers.append(user)

        random.shuffle(self.sellers)
        random.shuffle(self.buyers)

    def generate_transactions(self, output):
        error_count = 0

        while self.buyers and self.sellers:
            buyer = random.choice(self.buyers)
            seller = random.choice(self.sellers)

            if buyer.id == seller.id:
                error_count += 1
                continue

            transaction = self.generate_transaction(buyer=buyer, seller=seller)
            self.save_transaction(transaction.to_csv(), output)

            if buyer.buy <= 0:
                self.buyers.remove(buyer)
            if seller.sell <= 0:
                self.sellers.remove(seller)

    def generate_transaction(self, seller, buyer):
        seller.sell -= 1
        buyer.buy -= 1

        return Transaction(buyer.id, seller.id)

    def save_transaction(self, transaction, output):
        output.writerow(transaction)


Simulation(user_types_mapping).run()

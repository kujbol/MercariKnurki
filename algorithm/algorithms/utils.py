from algorithm.model.transaction import Transaction


class NormalizedUid:
    def __init__(self):
        self.uid_dict = {}
        self.reversed_uid_dict = {}

    def __call__(self, uid, *args, **kwargs):
        if uid not in self.uid_dict.keys():
            self.reversed_uid_dict[len(self.uid_dict)] = uid
            self.uid_dict[uid] = len(self.uid_dict)
        return self.uid_dict[uid]

    def reversed(self):
        return lambda x: self.reversed_uid_dict[x]

    def __len__(self):
        return len(self.uid_dict)


def process_transactions(transactions):
    get_uid = NormalizedUid()
    return [Transaction(
        get_uid(transaction.seller),
        get_uid(transaction.buyer),
        transaction.price,
        transaction.fraud
    ) for transaction in transactions], get_uid, get_uid.reversed()

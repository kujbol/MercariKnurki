from typing import List, Dict, Any, NamedTuple
from algorithm.algorithms.utils import process_transactions
from algorithm.model.transaction import Transaction


class PageRankTuple(NamedTuple):
    symmetric: float
    asymmetric: float
    asymmetric_reversed: float
    split_seller: float
    split_buyer: float


def _calc_rank(transactions, iterations=1000, dump_factor=0.0, symmetric=False):
    transactions, get_uid, reversed_get_uid = process_transactions(transactions)

    if symmetric:
        transactions += [
            Transaction(transaction.buyer, transaction.seller, transaction.price, transaction.fraud)
            for transaction in transactions
        ]

    users = len(get_uid)
    values = [1.0/users]*users
    total_cost = [0.0]*users

    for transaction in transactions:
        total_cost[transaction.seller] += transaction.price

    for _ in range(iterations):
        tmp_val = [0.0]*users
        for transaction in transactions:
            tmp_val[transaction.buyer] += (values[transaction.seller] * transaction.price) / total_cost[transaction.seller]
        values = [
            old_val * dump_factor + new_val * (1-dump_factor)
            for old_val, new_val in zip(values, tmp_val)
        ]

    return {
        reversed_get_uid(key): values[key]
        for key in range(len(values))
    }


def run_pagerank(transactions: List[Transaction]) -> Dict[Any, PageRankTuple]:
    uids = {t.seller for t in transactions} | {t.buyer for t in transactions}
    symmetric_pagerank = _calc_rank(transactions, symmetric=True)
    asymmetric_pagerank = _calc_rank(transactions, symmetric=False)
    asymmetric_pagerank_reversed = _calc_rank([reversed(t) for t in transactions], symmetric=False)
    splitted_pagerank = _calc_rank([
        Transaction(
            "{}_s".format(t.seller),
            "{}_b".format(t.buyer),
            t.price,
            t.fraud
        )
        for t in transactions], symmetric=True)
    return {
        uid: PageRankTuple(
            symmetric_pagerank[uid],
            asymmetric_pagerank[uid],
            asymmetric_pagerank_reversed[uid],
            splitted_pagerank.get("{}_s".format(uid), 0.0),
            splitted_pagerank.get("{}_b".format(uid), 0.0),
        )
        for uid in uids
    }


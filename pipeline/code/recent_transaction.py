from model.model import Transaction
from typing import List
from service.base_service import BaseService

class RecentTransaction(BaseService):
    def __init__(self):
        super(RecentTransaction, self).__init__()
        self.list_transaction: List[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.list_transaction.append(transaction)

    def get_top_recent_transaction(self, top_k: int = 5):
        return self.list_transaction[::-1][:top_k]
    
    def get_transaction(self):
        return self.list_transaction
    

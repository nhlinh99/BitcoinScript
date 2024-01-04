from pipeline.code.p2pkh import P2PKH_Address
from pipeline.code.multisig_p2sh import Multisig_Address
from pipeline.code.recent_transaction import RecentTransaction
from service.base_service import BaseService
from model.model import *


class TransactionPipeline(BaseService):
    def __init__(self):
        super(TransactionPipeline, self).__init__()

        self.p2pkh_address = P2PKH_Address()
        self.multisig_address = Multisig_Address()
        self.recent_transaction = RecentTransaction()

    def send_transaction_p2pkh(self, transaction: Transaction):
        private_key = transaction.address_input.private_key
        address_output = transaction.address_output.address
        amount = transaction.amount
        fee = transaction.fee

        tx_in = self.p2pkh_address.create_txin(private_key)
        balance = sum([item["value"] for item in tx_in])
        remaining = balance-amount-fee
        tx_out = self.p2pkh_address.create_txout(address_output, amount=amount, balance=balance)
        tx_out += self.p2pkh_address.create_txout(self.p2pkh_address.get_address(private_key), amount=remaining, balance=balance)
        tx = self.p2pkh_address.create_transaction(tx_in, tx_out, private_key)
        # transaction_id = self.p2pkh_address.broadcast_tx(tx)
        transaction_id = "ahihihi"
        if transaction_id:
            transaction.transaction_id = transaction_id
            transaction.timestamp = self.get_timezone()
            transaction.address_input.balance = remaining
            self.recent_transaction.add_transaction(transaction)

        return transaction
    
    def send_transaction_multisig(self, transaction: MultisigTransaction):
        private_keys = [info.private_key for info in transaction.address_input.list_address]
        address_output = transaction.address_output.address
        amount = transaction.amount
        fee = transaction.fee
        num_signs = 2
        
        redeem_script = self.multisig_address.get_redeem_script(private_keys, num_signs)

        tx_in = self.multisig_address.create_txin(redeem_script)
        balance = sum([item["value"] for item in tx_in])
        remaining = balance-amount-fee
        tx_out = self.multisig_address.create_txout(address_output, amount=amount, balance=balance)
        tx_out += self.multisig_address.create_txout(self.multisig_address.get_address(redeem_script), amount=remaining, balance=balance)
        tx = self.multisig_address.create_transaction(tx_in, tx_out, private_keys)
        # transaction_id = self.multisig_address.broadcast_tx(tx)
        transaction_id = "ahihihi"
        if transaction_id:
            transaction.transaction_id = transaction_id
            transaction.timestamp = self.get_timezone()
            self.recent_transaction.add_transaction(transaction)

        return transaction
    
    def get_all_transaction(self):
        return self.recent_transaction.get_transaction()
    
    def get_top_transaction(self):
        return self.recent_transaction.get_top_recent_transaction()
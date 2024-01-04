from cryptos import *
from cryptos.electrumx_client.types import ElectrumXUnspentResponse
from service.base_service import BaseService


class P2PKH_Address(BaseService):
    def __init__(self):
        super(P2PKH_Address, self).__init__()
        self.bitcoin = Bitcoin(testnet=True)

    def create_txin(self, private_key: str) -> ElectrumXUnspentResponse:
        address = self.get_address(private_key)
        txin = self.bitcoin.unspent(address)
        return txin
    
    def create_txout(self, address: str, amount: int, balance: int, fee: int = 750) -> List[dict]:
        amount_send_valid = min(amount, balance - fee)
        return [{'value': amount_send_valid, 'address': address}]
    
    def create_transaction(self, tx_in: ElectrumXUnspentResponse, tx_out, private_key) -> Tx:
        tx = self.bitcoin.mktx(tx_in, tx_out)
        tx = self.bitcoin.sign(tx, 0, private_key)
        return tx
    
    def broadcast_tx(self, tx: Tx) -> str:
        tx_serialize = serialize(tx)
        return self.bitcoin.pushtx(tx_serialize)

    def get_address(self, private_key: str) -> str:
        return self.bitcoin.privtop2pkh(private_key)
    
    def get_balance(self, address_id: str) -> int:
        address_info = self.bitcoin.unspent(address_id)
        balance = sum([item["value"] for item in address_info])
        return balance


if __name__ == "__main__":
    p2pkh_address = P2PKH_Address()

    private_key = "cS2Bz7tdXKsFBKiFLGhNFVMrnZVxpFR96GShmtfcc95NdXARLTAZ"
    address_output = "2MvukeKaPBWwfHJBAZ72P7nm45HKPG91Wg3"
    amount = 8000
    fee = 750
    
    tx_in = p2pkh_address.create_txin(private_key)
    balance = sum([item["value"] for item in tx_in])
    tx_out = p2pkh_address.create_txout(address_output, amount=amount, balance=balance)
    tx_out += p2pkh_address.create_txout(p2pkh_address.get_address(private_key), amount=balance-amount-fee, balance=balance)
    tx = p2pkh_address.create_transaction(tx_in, tx_out, private_key)
    result = p2pkh_address.broadcast_tx(tx)
    print(result)
    if result:
        print("TRANSACTION SUCCESS")
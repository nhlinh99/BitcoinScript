from cryptos import *
from cryptos.electrumx_client.types import ElectrumXUnspentResponse
from service.base_service import BaseService


class Multisig_Address(BaseService):
    def __init__(self):
        super(Multisig_Address, self).__init__()
        self.bitcoin = Bitcoin(testnet=True)

    def create_txin(self, private_key: str) -> ElectrumXUnspentResponse:
        address = self.get_address(private_key)
        txin = self.bitcoin.unspent(address)
        return txin
    
    def create_txout(self, address: str, amount: int, balance: int, fee: int = 750) -> List[dict]:
        amount_send_valid = min(amount, balance - fee)
        return [{'value': amount_send_valid, 'address': address}]
    
    def create_transaction(self, tx_in: ElectrumXUnspentResponse, tx_out, redeem_script:str, private_keys: List[str]) -> Tx:
        tx = self.bitcoin.mktx(tx_in, tx_out)
        list_sign = []
        for key in private_keys:
            list_sign.append(self.bitcoin.multisign(tx, 0, redeem_script, key))

        tx = apply_multisignatures(tx, 0, redeem_script, list_sign)
        return tx
    
    def broadcast_tx(self, tx: Tx):
        tx_serialize = serialize(tx)
        return self.bitcoin.pushtx(tx_serialize)

    def get_address(self, redeem_script: str) -> str:
        return self.bitcoin.p2sh_scriptaddr(redeem_script)
    
    def get_pubkey(self, private_key: str) -> str:
        return self.bitcoin.privtopub(private_key)

    def get_redeem_script(self, list_private_keys: List[str], num_sign: int):
        list_pub_keys = [self.bitcoin.privtopub(key) for key in list_private_keys]
        return mk_multisig_script(list_pub_keys, num_sign)

if __name__ == "__main__":
    multisig_address = Multisig_Address()

    private_keys = ["sample_key_1",
                "sample_key_2"]
    address_output = "sample_address_output"
    num_signs = 2
    amount = 8000
    fee = 750
    
    redeem_script = multisig_address.get_redeem_script(private_keys, num_signs)

    tx_in = multisig_address.create_txin(redeem_script)
    balance = sum([item["value"] for item in tx_in])
    tx_out = multisig_address.create_txout(address_output, amount=amount, balance=balance)
    tx_out += multisig_address.create_txout(multisig_address.get_address(redeem_script), amount=balance-amount-fee, balance=balance)
    tx = multisig_address.create_transaction(tx_in, tx_out, redeem_script, private_keys)
    result = multisig_address.broadcast_tx(tx)
    print(result)
    if result:
        print("TRANSACTION SUCCESS")
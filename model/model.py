from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Address(BaseModel):
    private_key: Optional[str]
    public_key: Optional[str]
    address: Optional[str]

class MultisigAddress(BaseModel):
    list_address: List[Address]
    redeem_script: Optional[str]
    p2sh_address: Optional[str]

class Transaction(BaseModel):
    transaction_id: Optional[str]
    timestamp: Optional[str]
    address_input: Address
    address_output: Address
    amount: int
    fee: Optional[int] = 500
    
class MultisigTransaction(Transaction):
    address_input: MultisigAddress


class InputTransaction(BaseModel):
    private_key: str
    address_output: str
    amount: int

class InputMultisigTransaction(BaseModel):
    private_key: List[str]
    address_output: str
    amount: int
    num_sign: int
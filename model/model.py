from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Address(BaseModel):
    private_key: Optional[str]
    public_key: Optional[str] = Field(..., exclude=True)
    address: Optional[str]
    balance: Optional[int] = Field(0, exclude=True)

class MultisigAddress(BaseModel):
    list_address: List[Address]
    redeem_script: Optional[str] = Field(..., exclude=True)
    p2sh_address: Optional[str] = Field(..., exclude=True)

class Transaction(BaseModel):
    transaction_id: Optional[str] = Field(..., exclude=True)
    transaction_type: str = Field(
        default="p2pkh", title="p2pkh | multisig", max_length=20
    )
    timestamp: Optional[str]
    address_input: Address
    address_output: Address
    amount: int
    fee: Optional[int] = 750
    
class MultisigTransaction(Transaction):
    address_input: MultisigAddress
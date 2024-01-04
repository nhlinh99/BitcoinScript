import uvicorn
from fastapi import FastAPI, Body
from typing_extensions import Annotated
from model.model import *

from pipeline.transaction import TransactionPipeline


app = FastAPI()
pipeline = TransactionPipeline()

@app.post("/send_p2pkh")
async def send_p2pkh(transaction: Annotated[Transaction, Body(embed=True)]):
   result = pipeline.send_transaction_p2pkh(transaction)
   return result

@app.post("/send_multisig")
async def send_multisig(transaction: Annotated[MultisigTransaction, Body(embed=True)]):
   result = pipeline.send_transaction_multisig(transaction)
   return result

@app.get("/get_all_transaction")
async def get_all_transaction():
   result = pipeline.get_all_transaction()
   return result


if __name__ == "__main__":
   uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
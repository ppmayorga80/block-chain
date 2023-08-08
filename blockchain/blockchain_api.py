import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from blockchain import BlockChain, Block, Transaction

bitcoin = BlockChain()
bitcoin.create_genesis_block()
node_address = str(uuid.uuid1()).replace('-', '').upper()

app = FastAPI()


class TransactionArg(BaseModel):
    amount: int
    sender: str
    recipient: str


@app.get("/blockchain")
def blockchain():
    return bitcoin.to_json()


@app.post("/transaction")
def transaction(data: TransactionArg):
    next_block_index = bitcoin.create_new_transaction(
        Transaction(
            amount=data.amount,
            sender=data.sender,
            recipient=data.recipient
        )
    )
    message = f"Transaction will be added to block {next_block_index}"
    return message


@app.get("/mine")
def mine():
    last_block: Block = bitcoin.get_last_block()
    prev_hash = last_block.hash_str
    pending_transactions = bitcoin.pending_transactions
    nonce, hash_str = bitcoin.proof_of_work(prev_hash=prev_hash, transactions=pending_transactions)

    # create a reward
    bitcoin.create_new_transaction(
        Transaction(
            amount=1250,
            sender="00",
            recipient=node_address
        )
    )

    new_block = bitcoin.create_new_block(nonce=nonce,
                                         cur_hash=hash_str,
                                         prev_hash=prev_hash)
    return new_block

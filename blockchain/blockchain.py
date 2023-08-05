import json
from dataclasses import dataclass, asdict, field
from datetime import datetime

import pytz


@dataclass
class Transaction:
    """Transaction information to save in every block"""
    amount: int
    sender: str
    recipient: str


@dataclass
class Block:
    """Block class to build the chain"""
    index: int
    timestamp: float
    transactions: list[Transaction]
    nonce: int
    hash: str
    prev_hash: str


@dataclass
class BlockChain:
    """This is the main blockchain class"""
    chain: list[Block] = field(default_factory=list)
    pending_transactions: list[Transaction] = field(default_factory=list)

    def to_json(self):
        """returns the json representation of current object"""
        x = asdict(self)
        x_str = json.dumps(x, indent=3)
        return x_str

    def create_new_block(self, nonce: int, cur_hash: str, prev_hash: str) -> Block:
        """ 1. Create a new block,
            2. insert pending transactions to the new block, and
            3. insert the new block to the chain
        :param nonce: the validation number
        :param cur_hash: current hash
        :param prev_hash: previous hash
        :return: the new block
        """

        # 1. creating the new block and add pending transaction to it
        new_block = Block(
            index=len(self.chain) + 1,
            timestamp=datetime.now(pytz.utc).timestamp(),
            transactions=self.pending_transactions,
            nonce=nonce,
            hash=cur_hash,
            prev_hash=prev_hash
        )
        # 2. add new block to the chain
        self.chain.append(new_block)
        # 3. emptying pending transaction
        self.pending_transactions = []

        return new_block

    def get_last_block(self) -> Block or None:
        """get last block"""
        return self.chain[-1] if self.chain else None

    def create_new_transaction(self, amount: int, sender: str, recipient: str) -> int:
        """create a new transaction and add it to the pending transaction list
        :param amount: the amount to be set
        :param sender: the sender id
        :param recipient: the recipient id
        :return: and id of the next block
        """
        new_transaction = Transaction(
            amount=amount,
            sender=sender,
            recipient=recipient
        )
        self.pending_transactions.append(new_transaction)
        last_block = self.get_last_block()
        return last_block.index + 1


if __name__ == '__main__':
    bitcoin = BlockChain()
    bitcoin.create_new_block(123, 'abc', '')
    bitcoin.create_new_transaction(66, 'ABC', 'CDE')
    print(bitcoin.to_json())
    print("----------------")

    bitcoin.create_new_block(123, 'abc', '')
    print(bitcoin.to_json())
    print("================")

    bitcoin.create_new_transaction(77, 'XYZ1', 'CDE1')
    bitcoin.create_new_transaction(88, 'XYZ2', 'CDE2')
    bitcoin.create_new_transaction(99, 'XYZ2', 'CDE3')
    bitcoin.create_new_block(123, 'abc', '')
    print(bitcoin.to_json())

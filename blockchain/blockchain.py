import hashlib
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from itertools import count

import jsons
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
    hash_str: str
    prev_hash: str


@dataclass
class BlockChain:
    """This is the main blockchain class"""
    chain: list[Block] = field(default_factory=list)
    pending_transactions: list[Transaction] = field(default_factory=list)

    def to_json_string(self):
        """returns the json representation of current object"""
        x = asdict(self)
        x_str = json.dumps(x, indent=3)
        return x_str

    def to_json(self):
        """returns the json representation of current object"""
        x = asdict(self)
        return x

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
            hash_str=cur_hash,
            prev_hash=prev_hash
        )
        # 2. add new block to the chain
        self.chain.append(new_block)
        # 3. emptying pending transaction
        self.pending_transactions = []

        return new_block

    def create_genesis_block(self):
        """Create the block at the beginning of the chain"""
        return self.create_new_block(
            nonce=100, cur_hash="0000", prev_hash="00"
        )

    def get_last_block(self) -> Block or None:
        """get last block"""
        return self.chain[-1] if self.chain else None

    def create_new_transaction(self, transaction: Transaction) -> int:
        """create a new transaction and add it to the pending transaction list
        :param transaction: the transaction information
        :return: and id of the next block
        """
        self.pending_transactions.append(transaction)
        last_block = self.get_last_block()
        return last_block.index + 1

    @classmethod
    def hash_block(cls, nonce: int, prev_hash: str, transactions: list[Transaction]) -> str:
        """hash the given block
        :param nonce: the nonce value to be used
        :param prev_hash: previous hash i.e. the hash_str of previous block
        :param transactions: the block to be hashed
        :return: the hashed string
        """
        transactions_str = jsons.dumps(transactions)
        data_str = f"{prev_hash}{nonce}{transactions_str}"
        hashed_data_str = hashlib.sha256(data_str.encode('UTF8')).hexdigest()
        return hashed_data_str.upper()

    @classmethod
    def _validate_hash(cls, hash_str: str) -> bool:
        """Validate the hash string with a given logic:
        option a: the hash string starts with 4 zeros in a row
        option b: the hash string contains the first 4 prime numbers
                  in that position for example '2' at position 2 and
                  '5' at position 5.
        :param hash_str: the hash string to be validated
        :return: true if validation was successful or false otherwise
        """
        pos = [2, 3, 5, 7]
        flag = all(hash_str[k] == f"{k}" for k in pos)
        return flag

    @classmethod
    def proof_of_work(cls, prev_hash, transactions: list[Transaction]) -> tuple[int, str]:
        """compute a valid nonce and return it with the hash string
        brute force method: try with all values for nonce starting
        at zero until find a valid hash string
        :param prev_hash: the hash string of previous block
        :param transactions: the block to be used as a proof of work
        """
        valid_nonce = -1
        valid_hash_str = ""
        for nonce in count():
            hash_str = cls.hash_block(
                nonce=nonce,
                prev_hash=prev_hash,
                transactions=transactions
            )
            if cls._validate_hash(hash_str=hash_str):
                valid_nonce = nonce
                valid_hash_str = hash_str
                break
        return valid_nonce, valid_hash_str

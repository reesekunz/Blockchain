import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        # have to make up previous hash and proof cause there is no previous hash and proof when initiated
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            "index": len(self.chain) + 1,
            # dont need self.proof since being passed as an argument (same with previous_hash)
            "proof": proof,
            "timestamp": time(),  # from time module import
            # list of all the transactions we want to be included in history
            "transactions": self.current_transactions,
            "previous_hash": previous_hash

        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block, sort_keys=True)
        string_in_bytes = block_string.encode()

        # TODO: Hash this string using sha256
        hash_object = hashlib.sha256(string_in_bytes)
        hash_string = hash_object.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format. Can now be used in future blocks.
        return hash_string

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Simple Proof of Work Algorithm
        Stringify the block and look for a proof.
        Loop through possibilities, checking each one against `valid_proof`
        in an effort to find a number that is a valid proof
        :return: A valid proof for the provided block
        """
        # stringify block
        block_string = json.dumps(block, sort_keys=True)
        proof = 0
        # increment proof until self.valid_proof returns True
        while self.valid_proof(block_string, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f'{block_string}{proof}'.encode(
        )  # encode turns string into bytes
        guess_hash = hashlib.sha256(guess).hexdigest()
        # check if first 3 values start with 000
        print(guess_hash, "guess_hash")
        return guess_hash[:3] == '000'
        # if guess_hash[:3] == '000':
        #     return True
        # else:
        #     return False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# [{genesis block}, {hashOfGenisis, proof}, {hash_of_last_block, proof_of_last_block}, {hash_of_last_block, proof_of_last_block} ]
@app.route('/mine', methods=['GET'])
def mine():
    # grab last block in chain
    block = blockchain.last_block
    # Run the proof of work algorithm to get the next proof. Look for some # that results in a pattern in our hash. That # is our proof.
    proof = blockchain.proof_of_work(block)
    # hash the new block
    block_hash = blockchain.hash(block)
    # Forge the new Block by adding it to the chain with the proof
    new_block = blockchain.new_block(proof, block_hash)

    response = {

        "message": "Hey I found a proof! And forged a new block",
        "index": new_block['index'],
        "transactions": new_block['transactions'],
        "proof": new_block['proof'],
        'previous_hash': block_hash
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        "chain": blockchain.chain,
        "chain_length": len(blockchain.chain)
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
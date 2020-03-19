# same file as blockchain.py from basic_block_gp just copied over
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

    def new_transaction(self, sender, receiver, amount):
        new_transaction = {
            "timestamp": time(),
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }
        # new transaction goes into the next block
        self.current_transactions.append(new_transaction)
        # return index of block that will hold this transaction
        future_index = self.last_block['index'] + 1
        return future_index

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
        # return guess_hash[:6] == '000000'
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
# TODO - Modify the `mine` endpoint to instead receive and validate or reject a new proof sent by a client.
#   - It should accept a POST
#       - Note that `request` and `requests` both exist in this project
#     - Check that 'proof', and 'id' are present
#       - return a 400 error using `jsonify(response)` with a 'message'
# - Return a message indicating success or failure. Remember, a valid proof should fail for all senders except the first.

# miner: gets last block
# miner: runs proof_of_work
# miner: posts their proof
# from there, we need to check it to see if its a valid proof

# first person to submit valid proof wins. This is b/c the valid proof forges a new block, meaning the chain has moved on. The second miner will be comparing it to a previous block, but that wont be the previous block anymore

# [{genesis block}, {hashOfGenisis, proof}, {hash_of_last_block, proof_of_last_block}, {hash_of_last_block, proof_of_last_block} ]
@app.route('/mine', methods=['POST'])
def mine():
    # pull data out of request
    data = request.get_json()
    # check that proof and id are present
    required = ['proof', 'id']
    # if not present. send back error message and 400
    if not all(x in data for x in required):
        response = {"message": "Missing values"}
        return jsonify(response), 400

    # if proof and id are present - make sure its valid
    submitted_proof = data['proof']
    miner_id = data['id']
    block_string = json.dumps(blockchain.last_block, sort_keys=True)
    is_valid_proof = blockchain.valid_proof(block_string, submitted_proof)
    if is_valid_proof:
        # now that we know its a valid proof, we can make a new block
        previous_hash = blockchain.hash(blockchain.last_block)
        new_block = blockchain.new_block(submitted_proof, previous_hash)
        blockchain.new_transaction(sender='0', receiver=miner_id, amount=1)
        response = {
            "message": "New Block Forged"

        }
    # submitted proof is not a valid proof
    else:
        response = {
            "message": "Submitted proof is not a valid proof, or block has changed (chain may have moved on). Try again."
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


@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        # "last_block": blockchain.chain[-1]
        "last_block": blockchain.last_block
    }
    return jsonify(response), 200

# this is NOT secure!
# now someone can send a new transaction to someone else
@app.route('/transactions/new', methods=["POST"])
def new_transaction():
    data = request.get_json()
    required = ['sender', 'receiver', 'amount']
    if not all(x in data for x in required):
        response = {"message": "Missing values."}
        return jsonify(response), 400

    index = blockchain.new_transaction(
        sender=data["sender"], receiver=data["receiver"], amount=data["amount"])
    response = {"message": f"Your transaction will be in block {index} "}

    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

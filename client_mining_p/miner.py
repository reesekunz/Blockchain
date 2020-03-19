import hashlib
import requests

import sys
import json

# Run server in one terminal and miner in other terminal.


def proof_of_work(block):
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
    while valid_proof(block_string, proof) is False:
        proof += 1

        return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
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
    # check if first 6 values start with 0
    # print(guess_hash, "guess_hash")
    return guess_hash[:6] == '000000'

# Grab last block. Use that last block to look for our proof of work and send that proof of work into our server (and hope we are the first one.


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    coins_mined = 0
    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # last_block = data.get('last_block') SAME AS
        last_block = data['last_block']
        print("starting to look for a proof of work")
        new_proof = proof_of_work(last_block)
        print(f'Proof found: {new_proof}')

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data['message'] == "New Block Forged":
            coins_mined += 1
            print(f'We mined a coin! Coins mined: {coins_mined}')

        else:
            print(data['message'])

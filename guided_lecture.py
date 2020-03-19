hash("key")  # - -> integer
hash("i like turtles")  # --> bc139de

hashlib.sha256({index, timestamp, transactions: [], proof})  # -->

chain = [
    {index, timestamp, transactions: [], proof},
    # previousHash = hash of ^
    {index, timestamp, transactions: [{sender: tim, amount: 10, recipient: sam}], proof, previousHash},
    # previousHash = hash of ^. If this hash above is changed, it will result in a different hash and you can tell that the history has been changed.
    {index, timestamp, transactions: [], proof, previousHash},
]

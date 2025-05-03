import hashlib
import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f"{self.sender} -> {self.recipient}: {self.amount}"

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions  # List of Transaction objects
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_str = ''.join(str(tx) for tx in self.transactions)
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{tx_str}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, '0', [Transaction("None", "Genesis", 0)])

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False

            if current.previous_hash != previous.hash:
                print(f"Invalid previous hash at block {i}")
                return False

        return True






#Usage
tx1 = Transaction("Alice", "Bob", 50)
tx2 = Transaction("Bob", "Charlie", 25)
tx3 = Transaction("Charlie", "Dave", 10)

bc = Blockchain()
bc.add_block(Block(1, '', [tx1]))
bc.add_block(Block(2, '', [tx2, tx3]))

for block in bc.chain:
    print(f"\nBlock {block.index}")
    print("Hash:", block.hash)
    print("Previous Hash:", block.previous_hash)
    print("Transactions:", block.transactions)
    print("Nonce:", block.nonce)
    print("Timestamp:", block.timestamp)

print("\nIs blockchain valid?", bc.is_chain_valid())

import time
import hashlib
import json
import datetime


class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data  # Can include type: 'game' | 'reward' | etc.
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.data)}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), {"type": "genesis", "message": "Genesis Block"})

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(
            index=prev_block.index + 1,
            previous_hash=prev_block.hash,
            timestamp=time.time(),
            data=data
        )
        self.chain.append(new_block)
        return new_block

    def reward_player(self, player_address, amount=5):
        """Creates a reward block for the player with Chroma Denarii"""
        reward_data = {
            "type": "reward",
            "to": player_address,
            "amount": amount,
            "currency": "Chroma Denarii"
        }
        return self.add_block(reward_data)

    def get_chain(self):
        return [block.__dict__ for block in self.chain]


# Test logic (optional)
if __name__ == "__main__":
    bc = Blockchain()
    bc.add_block({"type": "game", "message": "First color guess"})
    bc.reward_player("player123")

    for block in bc.get_chain():
        print(json.dumps(block, indent=2))

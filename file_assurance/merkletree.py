import os
import json
from datetime import datetime
from Crypto.Hash import keccak
from hashfiles import hashes

# Function to hash data using Keccak256
def hash_data(data):
    hash_obj = keccak.new(digest_bits=256)
    hash_obj.update(data.encode('utf-8'))
    return hash_obj.hexdigest()

# Function to build a Merkle tree from a list of hashes
def build_merkle_tree(hashes):
    # Initialize the tree structure with the leaves
    tree = [hashes[:]]  # Copy the list to avoid modifying the original list
    level = hashes
    
    # Iteratively build the tree
    while len(level) > 1:
        # If the number of hashes at this level is odd, append a hash of '0'
        if len(level) % 2 == 1:
            level.append(hash_data('0'))
        
        # Create the next level
        new_level = []
        for i in range(0, len(level), 2):
            new_hash = hash_data(level[i] + level[i + 1])
            new_level.append(new_hash)
        
        # Add the new level to the tree and prepare for next iteration
        tree.append(new_level)
        level = new_level
    
    # The tree is built from bottom to top, so we reverse it to have the root at the top
    return tree[::-1]

# Build the Merkle tree and store the entire tree structure
merkle_tree = build_merkle_tree(hashes)

# Save the root hash, the first element of the first list in the tree
root_hash = merkle_tree[0][0]
# print(root_hash)

# Get the current timestamp and format it as YYYYMMDD_HHMMSS
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Construct the filename with the timestamp
tree_filename = f'hashes/merkle_tree_{timestamp}.json'

# Ensure the 'hashes' directory exists
os.makedirs('hashes', exist_ok=True)

# Save the Merkle tree to a JSON file
with open(tree_filename, 'w') as json_file:
    json.dump({
        'merkle_tree': merkle_tree,
        'leaf_hashes': hashes
    }, json_file, indent=4)

print(f"Merkle tree complete. Results saved to {tree_filename}")
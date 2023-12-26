import os
import json
from Crypto.Hash import keccak
from datetime import datetime

# Function to hash a file using Keccak256
def hash_file(file_path, chunk_size=8192):
    hash_obj = keccak.new(digest_bits=256)
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

# Get the directory of the script and the 'files' folder
script_dir = os.path.dirname(os.path.realpath(__file__))
files_dir = os.path.join(script_dir, 'files')

# List to store the filesnames and hashes
files_hashes = []

# List to store the hashes
hashes = []

# Iterate over each file in the 'files' directory
for filename in os.listdir(files_dir):
    file_path = os.path.join(files_dir, filename)
    
    # Ensure it's a file and not a directory
    if os.path.isfile(file_path):
        # Hash the file
        file_hash = hash_file(file_path)
        # Append the result to the two lists
        files_hashes.append({'filename': filename, 'hash': file_hash})
        hashes.append(file_hash)

# Get the current timestamp and format it as YYYYMMDD_HHMMSS
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Construct the filename with the timestamp
jsonl_filename = f'hashes/hashes_{timestamp}.jsonl'

# Write the hashes to a JSONL file with the timestamped filename
with open(jsonl_filename, 'w') as jsonl_file:
    for entry in files_hashes:
        jsonl_file.write(json.dumps(entry) + '\n')

print(f"Hashing complete. Results saved to {jsonl_filename}")
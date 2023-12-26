import requests
import json
import os

def bitcoin_rpc(method, params=[], wallet=None):
    url = f"http://127.0.0.1:8332/wallet/{wallet}" if wallet else "http://127.0.0.1:8332/" # Change to your RPC port
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    # This line will need to be changed to your RPC username and password in your bitcoin.conf file
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=('rpcuser', 'rpcpassword'))
    return response.json()

# Prompt the user for wallet names
wallet1_name = input("Enter the name for wallet1: ")
wallet2_name = input("Enter the name for wallet2: ")

# Create wallets
wallet1_creation = bitcoin_rpc("createwallet", [wallet1_name])
wallet2_creation = bitcoin_rpc("createwallet", [wallet2_name])

# Get new Taproot addresses
wallet1_address = bitcoin_rpc("getnewaddress", ["", "bech32m"], wallet1_name)
wallet2_address = bitcoin_rpc("getnewaddress", ["", "bech32m"], wallet2_name)

# Ensure the output directory exists
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

# Save output to JSONL file in the outputs directory
output_file_path = os.path.join(output_dir, "wallets.jsonl")
with open(output_file_path, "w") as file:
    wallet1_data = {
        "creation_result": wallet1_creation,
        "taproot_address": wallet1_address["result"]
    }
    wallet2_data = {
        "creation_result": wallet2_creation,
        "taproot_address": wallet2_address["result"]
    }
    
    file.write(json.dumps(wallet1_data) + "\n")
    file.write(json.dumps(wallet2_data) + "\n")

print(f"Wallet information saved to {output_file_path}")
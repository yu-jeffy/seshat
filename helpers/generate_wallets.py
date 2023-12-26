import requests
import json
import os

def bitcoin_rpc(method, params=[], wallet=None, rpc_port="8332", rpc_username="rpcuser", rpc_password="rpcpassword"):
    url = f"http://127.0.0.1:{rpc_port}/wallet/{wallet}" if wallet else f"http://127.0.0.1:{rpc_port}/"
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(rpc_username, rpc_password))
    return response.json()

def generate_wallet(rpc_port, rpc_username, rpc_password):
    wallet_name = input("Enter the name for the new wallet: ")

    # Create wallet
    wallet_creation = bitcoin_rpc("createwallet", [wallet_name], rpc_port=rpc_port, rpc_username=rpc_username, rpc_password=rpc_password)

    # Get new Taproot address
    wallet_address = bitcoin_rpc("getnewaddress", ["", "bech32m"], wallet_name, rpc_port=rpc_port, rpc_username=rpc_username, rpc_password=rpc_password)

    # Ensure the output directory exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Save output to JSONL file in the outputs directory
    output_file_path = os.path.join(output_dir, "wallets.jsonl")
    with open(output_file_path, "a") as file:  # Use "a" mode to append to the file
        wallet_data = {
            "wallet_name": wallet_name,
            "creation_result": wallet_creation,
            "taproot_address": wallet_address["result"]
        }
        file.write(json.dumps(wallet_data) + "\n")

    print(f"Wallet '{wallet_name}' information saved to {output_file_path}")
    return wallet_name, wallet_address["result"]
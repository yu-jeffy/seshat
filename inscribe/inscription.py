import requests
import json
import os

def bitcoin_rpc(method, params=[], wallet=None):
    url = f"http://127.0.0.1:8332/wallet/{wallet}" if wallet else "http://127.0.0.1:8332/"
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=('rpcuser', 'rpcpassword'))
    return response.json()

def create_and_sign_tx(address, inscription_data_hex):
    # Fetch UTXOs from wallet1
    utxos = bitcoin_rpc("listunspent", [1, 9999999, [], True], "wallet1")["result"]
    if not utxos:
        print("No UTXOs found in wallet1. Make sure it's funded.")
        return

    selected_utxo = utxos[0]  # Select the first UTXO
    txid = selected_utxo["txid"]
    vout = selected_utxo["vout"]
    amount = selected_utxo["amount"]

    # Create a raw transaction with OP_RETURN output
    raw_tx_response = bitcoin_rpc("createrawtransaction", [
        [{"txid": txid, "vout": vout}],
        [{address: amount - 0.00001000}, {"data": inscription_data_hex}]
    ], "wallet1")
    raw_tx_hex = raw_tx_response["result"]
    if not raw_tx_hex:
        print("Failed to create raw transaction. Response:", raw_tx_response)
        return

    # Sign the transaction
    signed_tx_response = bitcoin_rpc("signrawtransactionwithwallet", [raw_tx_hex], "wallet1")

    # Check if the signing was successful
    if not signed_tx_response["result"]:
        print("Failed to sign the transaction. Response:", signed_tx_response)
        return None

    return signed_tx_response["result"]["hex"]

# User input for inscription text
inscription_text = input("Enter the text you want to inscribe (max 80 bytes): ")
inscription_data = inscription_text.encode('utf-8')
if len(inscription_data) > 80:
    print("Error: Inscription text exceeds the 80-byte limit.")
    exit()

# Convert inscription data to hex
inscription_data_hex = inscription_data.hex()

# Replace with the address from wallet2
wallet2_address = "bcrt1ps3grgld76pek00d8y0tfdmrhv78jvwy2pxphccv9s30jaruwqxsslw80rh"

signed_tx_hex = create_and_sign_tx(wallet2_address, inscription_data_hex)
print("Signed Transaction Hex:", signed_tx_hex)

def broadcast_transaction(signed_tx_hex):
    broadcast_response = bitcoin_rpc("sendrawtransaction", [signed_tx_hex])
    if broadcast_response.get("error"):
        print("Failed to broadcast the transaction. Response:", broadcast_response)
        return None
    return broadcast_response["result"]

# Broadcast the signed transaction to the network
txid = broadcast_transaction(signed_tx_hex)
if txid:
    print("Transaction successfully broadcasted. TXID:", txid)
else:
    print("Transaction failed to broadcast.")

# Ensure the output directory exists
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

# Save output to JSONL file in the outputs directory
output_file_path = os.path.join(output_dir, "txs.jsonl")
if txid:
    with open(output_file_path, "a") as file:
        data = {
            "tx_type": "inscription",
            "signed_tx_hex": signed_tx_hex,
            "txid": txid
        }
        file.write(json.dumps(data) + "\n")
    print(f"Transaction information saved to {output_file_path}")
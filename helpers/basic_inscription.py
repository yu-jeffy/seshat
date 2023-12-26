import requests
import json

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

def select_utxo(utxos):
    print("\nAvailable UTXOs:")
    for i, utxo in enumerate(utxos, 1):
        print(f"{i}. TXID: {utxo['txid']}, Vout: {utxo['vout']}, Amount: {utxo['amount']} BTC")
    while True:
        choice = input("Select a UTXO by number (or 'exit' to cancel): ")
        if choice.lower() == 'exit':
            return None
        try:
            choice = int(choice)
            if choice < 1 or choice > len(utxos):
                raise ValueError
            return utxos[choice - 1]
        except ValueError:
            print("Invalid choice. Please enter a number from the list.")

def calculate_tx_fee(raw_tx_hex, fee_rate_satoshi_per_byte):
    # Get the size of the transaction
    decoded_tx = bitcoin_rpc("decoderawtransaction", [raw_tx_hex])
    tx_size = len(raw_tx_hex) / 2  # Hex string has 2 characters per byte
    # Calculate the fee
    return tx_size * fee_rate_satoshi_per_byte

def create_inscription(wallet1, wallet2_address, amount, inscription_data_hex, rpc_port, rpc_username, rpc_password):
    # Fetch UTXOs from wallet1
    utxos = bitcoin_rpc("listunspent", [1, 9999999, [], True], wallet1, rpc_port, rpc_username, rpc_password)["result"]
    if not utxos:
        print("No UTXOs found in wallet1. Make sure it's funded.")
        return

    # Let the user select a UTXO
    selected_utxo = select_utxo(utxos)
    if not selected_utxo:
        print("UTXO selection cancelled.")
        return

    txid = selected_utxo["txid"]
    vout = selected_utxo["vout"]
    utxo_amount = selected_utxo["amount"]

    # Create a raw transaction with OP_RETURN output
    raw_tx_response = bitcoin_rpc("createrawtransaction", [
        [{"txid": txid, "vout": vout}],
        [{wallet2_address: amount}, {"data": inscription_data_hex}]
    ], wallet1, rpc_port, rpc_username, rpc_password)
    raw_tx_hex = raw_tx_response["result"]
    if not raw_tx_hex:
        print("Failed to create raw transaction. Response:", raw_tx_response)
        return

    # Check if the selected UTXO can cover the amount
    if utxo_amount < amount:
        print("Selected UTXO does not have enough funds to cover the amount.")
        return

    # Sign the transaction
    signed_tx_response = bitcoin_rpc("signrawtransactionwithwallet", [raw_tx_hex], wallet1, rpc_port, rpc_username, rpc_password)

    # Check if the signing was successful
    if not signed_tx_response["result"]:
        print("Failed to sign the transaction. Response:", signed_tx_response)
        return None

    signed_tx_hex = signed_tx_response["result"]["hex"]
    print("Signed Transaction Hex:", signed_tx_hex)

    # Broadcast the signed transaction to the network
    txid = broadcast_transaction(signed_tx_hex, wallet1, rpc_port, rpc_username, rpc_password)
    if txid:
        print("Transaction successfully broadcasted. TXID:", txid)
    else:
        print("Transaction failed to broadcast.")
    return txid

def broadcast_transaction(signed_tx_hex, wallet, rpc_port, rpc_username, rpc_password):
    broadcast_response = bitcoin_rpc("sendrawtransaction", [signed_tx_hex, 0], wallet, rpc_port, rpc_username, rpc_password)
    if broadcast_response.get("error"):
        print("Failed to broadcast the transaction. Response:", broadcast_response)
        return None
    return broadcast_response["result"]
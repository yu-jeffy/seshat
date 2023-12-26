import requests
import json

def bitcoin_rpc(method, params=[], rpc_port=None, rpc_username=None, rpc_password=None):
    url = f"http://127.0.0.1:{rpc_port}/"
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(rpc_username, rpc_password))
    return response.json()

def get_transaction(txid, rpc_port, rpc_username, rpc_password):
    raw_tx = bitcoin_rpc("getrawtransaction", [txid, True], rpc_port, rpc_username, rpc_password)  # Set verbose to True to get decoded transaction
    return raw_tx.get('result')

def extract_inscription(decoded_tx):
    for vout in decoded_tx['vout']:
        if 'scriptPubKey' in vout and 'asm' in vout['scriptPubKey']:
            asm = vout['scriptPubKey']['asm']
            if asm.startswith('OP_RETURN'):
                hex_data = asm.split(' ')[1]
                try:
                    inscription = bytes.fromhex(hex_data).decode('utf-8')
                    return inscription
                except ValueError:
                    print("Inscription is not valid UTF-8 data.")
                    return None
    return None

def view_inscription(txid, rpc_port, rpc_username, rpc_password):
    # Fetch the transaction and decode it
    decoded_tx = get_transaction(txid, rpc_port, rpc_username, rpc_password)
    if decoded_tx:
        print()
        print("Raw transaction:")
        print(json.dumps(decoded_tx, indent=2))  # Print the entire transaction information
        inscription = extract_inscription(decoded_tx)
        print()
        if inscription:
            print("Inscription:", inscription)
        else:
            print("No inscription found in the transaction.")
    else:
        print("Transaction not found.")
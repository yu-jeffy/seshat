import requests
import json

def bitcoin_rpc(method, params=[]):
    url = "http://127.0.0.1:8332/" # Change to your RPC port
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

def get_transaction(txid):
    raw_tx = bitcoin_rpc("getrawtransaction", [txid, True])  # Set verbose to True to get decoded transaction
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

# User input for transaction ID
txid = input("Enter the transaction ID: ")

# Fetch the transaction and decode it
decoded_tx = get_transaction(txid)
if decoded_tx:
    inscription = extract_inscription(decoded_tx)
    if inscription:
        print("Inscription:", inscription)
    else:
        print("No inscription found in the transaction.")
else:
    print("Transaction not found.")
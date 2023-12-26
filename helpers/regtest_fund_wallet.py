import requests
import json

# Update the signature of bitcoin_rpc to accept RPC credentials
def bitcoin_rpc(method, params=[], rpc_port="18443", rpc_username="rpcuser", rpc_password="rpcpassword"):
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

# Update the signature of fund_address to accept RPC credentials
def fund_address(address, rpc_port, rpc_username, rpc_password, num_blocks=100):
    result = bitcoin_rpc("generatetoaddress", [num_blocks, address], rpc_port=rpc_port, rpc_username=rpc_username, rpc_password=rpc_password)
    if result.get('error'):
        print("Error:", result['error'])
    else:
        print(f"Mined {num_blocks} blocks. Rewards sent to {address}")
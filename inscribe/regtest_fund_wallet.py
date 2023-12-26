import requests
import json

def bitcoin_rpc(method, params=[]):
    url = "http://127.0.0.1:8332/"  # Change to your RPC port
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

def fund_address(address, num_blocks=100):
    """
    Mine blocks to the specified address.
    :param address: Taproot address to fund.
    :param num_blocks: Number of blocks to mine.
    """
    result = bitcoin_rpc("generatetoaddress", [num_blocks, address])
    if result.get('error'):
        print("Error:", result['error'])
    else:
        print(f"Mined {num_blocks} blocks. Rewards sent to {address}")

# Replace with your Taproot address
taproot_address = "bcrt1pugy2kwefar6nhthnw3n4wwm0dk6pft7l7gntk5458tlc5nrs89fqarwmgn"
fund_address(taproot_address)




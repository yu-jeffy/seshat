import requests
import json

def bitcoin_rpc(method, params=[], rpc_port="8332", rpc_username="rpcuser", rpc_password="rpcpassword"):
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

def list_wallets(rpc_port, rpc_username, rpc_password):
    response = bitcoin_rpc("listwallets", rpc_port=rpc_port, rpc_username=rpc_username, rpc_password=rpc_password)
    return response.get('result', [])

def get_taproot_address(wallet_name, rpc_port, rpc_username, rpc_password):
    response = bitcoin_rpc("getnewaddress", ["", "bech32m"], wallet=wallet_name, rpc_port=rpc_port, rpc_username=rpc_username, rpc_password=rpc_password)
    return response.get('result')
    
def load_wallets(rpc_port, rpc_username, rpc_password):
    wallets = list_wallets(rpc_port, rpc_username, rpc_password)
    
    if not wallets:
        print("No wallets available. Please create a new wallet first.")
        return None, None
    
    print("\nAvailable wallets:")
    for i, wallet in enumerate(wallets, 1):
        print(f"{i}. {wallet}")

    wallet_indices = []
    for wallet_number in ["first", "second"]:
        while True:
            choice = input(f"Select the {wallet_number} wallet by number (or 'exit' to cancel): ")
            if choice.lower() == 'exit':
                return None, None
            try:
                choice = int(choice)
                if choice < 1 or choice > len(wallets):
                    raise ValueError
                if choice in wallet_indices:
                    print("This wallet is already selected. Please choose a different one.")
                    continue
                wallet_indices.append(choice)
                break
            except ValueError:
                print("Invalid choice. Please enter a number from the list.")

    wallet1 = {'name': wallets[wallet_indices[0] - 1], 'taproot_address': get_taproot_address(wallets[wallet_indices[0] - 1], rpc_port, rpc_username, rpc_password)}
    wallet2 = {'name': wallets[wallet_indices[1] - 1], 'taproot_address': get_taproot_address(wallets[wallet_indices[1] - 1], rpc_port, rpc_username, rpc_password)} if len(wallets) > 1 else None


    if not wallet2:
        print("Another wallet is needed for a second wallet.")
    
    return wallet1, wallet2
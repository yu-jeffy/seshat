import requests
import json
import sys
from helpers.generate_wallets import generate_wallet
from helpers.load_wallets import load_wallets

# Global variables to keep track of RPC information and wallet details
rpc_port = None
rpc_username = None
rpc_password = None
wallet1 = {'name': None, 'taproot_address': None}
wallet2 = {'name': None, 'taproot_address': None}


ascii_art = """
────██──██─────
███████████▄───
──███████████▄─
──███────▀████─
──███──────███─
──███────▄███▀─
──█████████▀───
──███████████▄─
──███─────▀████
──███───────███
──███─────▄████
──████████████─
████████████▀──
────██──██─────
"""

def welcome_message():
    print()
    print(ascii_art)
    print()
    print("Welcome to Seshat, Bitcoin Inscription Tool")
    print()

def bitcoin_rpc(method, params=[]):
    url = f"http://127.0.0.1:{rpc_port}/"
    headers = {'content-type': 'application/json'}
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 0,
    }
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(rpc_username, rpc_password))
        response.raise_for_status()  # Will raise HTTPError for HTTP error codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the Bitcoin node: {e}")
        return None

def get_rpc_credentials():
    global rpc_port, rpc_username, rpc_password
    while True:
        rpc_port = input("Enter your Bitcoin Core RPC port: ")
        rpc_username = input("Enter your Bitcoin Core RPC username: ")
        rpc_password = input("Enter your Bitcoin Core RPC password: ")

        # Test the connection with the provided RPC credentials
        test_response = bitcoin_rpc("getblockchaininfo")
        if test_response is not None and not test_response.get('error'):
            print()
            print("Successfully connected to the Bitcoin Core node.")
            print()
            break
        else:
            print()
            print("Failed to connect with the provided RPC credentials. Please try again.")
            print()

def show_menu():
    options = [
        "Create wallet",
        "Load wallet",
        "Fund wallet (regtest)",
        "Create simple inscription",
        "View simple inscription",
        "Create taproot inscription",
        "View taproot inscription"
    ]
    print("\nOptions Menu:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Exit")

def handle_option_selection():
    while True:
        show_menu()
        try:
            choice = int(input("\nEnter the number of your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if choice == 0:
            print("Exiting the program.")
            sys.exit(0)
        elif choice == 1:
            wallet_name, taproot_address = generate_wallet(rpc_port, rpc_username, rpc_password)
            print()
            print(f"Wallet '{wallet_name}' created with Taproot address: {taproot_address}")
        elif choice == 2:
            wallet1_info, wallet2_info = load_wallets(rpc_port, rpc_username, rpc_password)
            if wallet1_info:
                wallet1['name'] = wallet1_info['name']
                wallet1['taproot_address'] = wallet1_info['taproot_address']
            if wallet2_info:
                wallet2['name'] = wallet2_info['name']
                wallet2['taproot_address'] = wallet2_info['taproot_address']
        elif choice == 3:
            print("Fund wallet (regtest) - under development")
        elif choice == 4:
            print("Create simple inscription - under development")
        elif choice == 5:
            print("View simple inscription - under development")
        elif choice == 6:
            print("Create taproot inscription - under development")
        elif choice == 7:
            print("View taproot inscription - under development")
        else:
            print("Invalid choice. Please try again.")

def main():
    welcome_message()
    get_rpc_credentials()
    handle_option_selection()

if __name__ == "__main__":
    main()
import requests
import json
import sys
from helpers.generate_wallets import generate_wallet
from helpers.load_wallets import load_wallets
from helpers.regtest_fund_wallet import fund_address
from helpers.basic_inscription import create_inscription
from helpers.basic_inscription_view import view_inscription

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

def is_regtest_active():
    blockchain_info = bitcoin_rpc("getblockchaininfo")
    return blockchain_info.get('result', {}).get('chain') == 'regtest'

def fund_wallets():
    if not is_regtest_active():
        print("Regtest is not active. Funding wallets is only available in regtest mode.")
        return
    else:
        print("Regtest is active. Funding wallets...")
    
    if wallet1['name'] is None or wallet2['name'] is None:
        print("Wallets must be loaded before they can be funded.")
        return
    
    # Fund wallet1
    fund_address(wallet1['taproot_address'], rpc_port, rpc_username, rpc_password)
    
    # Fund wallet2 if it's set
    if wallet2['name'] is not None:
        fund_address(wallet2['taproot_address'], rpc_port, rpc_username, rpc_password)

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
            fund_wallets()
        elif choice == 4:
            if not wallet1['name']:
                print("Please load a wallet first.")
            else:
                user_amount = float(input("Enter the transaction amount in BTC: "))
                inscription_text = input("Enter the text you want to inscribe (max 80 bytes): ")
                inscription_data = inscription_text.encode('utf-8')
                if len(inscription_data) > 80:
                    print("Error: Inscription text exceeds the 80-byte limit.")
                else:
                    inscription_data_hex = inscription_data.hex()
                    txid = create_inscription(wallet1['name'], wallet1['taproot_address'], user_amount, inscription_data_hex, rpc_port, rpc_username, rpc_password)
                    if txid:
                        print(f"Transaction ID: {txid}")
        elif choice == 5:
            txid = input("Enter the transaction ID: ")
            view_inscription(txid, rpc_port, rpc_username, rpc_password)
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
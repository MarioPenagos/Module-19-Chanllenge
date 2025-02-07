# Cryptocurrency Wallet
################################################################################

# This file contains the Ethereum transaction functions that you have created throughout this module’s lessons.
# By using import statements, you will integrate this `crypto_wallet.py` Python script
# into the KryptoJobs2Go interface program that is found in the `krypto_jobs.py` file.

################################################################################
# Imports
import os
import requests
from dotenv import load_dotenv

load_dotenv()
from bip44 import Wallet
from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

################################################################################
# Wallet functionality


def generate_account():
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    dotenv_path ='C:/Users/mpena/OneDrive/Documents/Fintech Boot Camp/Week 19/Module-19-Chanllenge/Starter_Code/.env'
    load_dotenv(dotenv_path)
    mnemonic = os.getenv("MNEMONIC")

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    # Convert private key into an Ethereum account
    account = Account.from_key(private)

    return account


def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


from web3.gas_strategies.time_based import medium_gas_price_strategy

def send_transaction(w3, account, to, wage):
    """Send an authorized transaction to the Ganache blockchain."""
    # Set gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert ETH amount to Wei
    value = w3.toWei(wage, "ether")

    # Calculate gas estimate
    gasEstimate = w3.eth.estimateGas(
        {"to": to, "from": account.address, "value": value}
    )

    # Get current gas price
    gasPrice = w3.eth.gas_price

    # Construct a raw transaction
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": gasPrice,  # Set the correct gas price
        "nonce": w3.eth.getTransactionCount(account.address),
    }

    try:
        # Sign the raw transaction with the account's private key
        signed_tx = w3.eth.account.sign_transaction(raw_tx, private_key=account.privateKey)

        # Send the signed transaction
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # Return the transaction hash
        return tx_hash.hex()
    except Exception as e:
        print(f"Error sending transaction: {e}")
        raise


from decouple import config
from cryptography.fernet import Fernet

from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.api import plaid_api

# Fernet encryption
fernet = Fernet(config("FERNET_KEY"))

def encrypt_token(token: str) -> str:
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

def get_plaid_client():
    configuration = Configuration(
        host="https://sandbox.plaid.com",
        api_key={
            "clientId": config("PLAID_CLIENT_ID"),
            "secret": config("PLAID_SECRET"),
        },
    )
    return plaid_api.PlaidApi(ApiClient(configuration))

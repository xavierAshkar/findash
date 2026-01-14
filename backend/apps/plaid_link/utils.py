from decouple import config
from cryptography.fernet import Fernet

from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.api import plaid_api


def get_fernet():
    key = config("FERNET_KEY", default=None)
    if not key:
        raise RuntimeError("FERNET_KEY is not configured")
    return Fernet(key)

def encrypt_token(token: str) -> str:
    return get_fernet().encrypt(token.encode()).decode()

def decrypt_token(token: str) -> str:
    return get_fernet().decrypt(token.encode()).decode()

def get_plaid_client():
    configuration = Configuration(
        host="https://sandbox.plaid.com",
        api_key={
            "clientId": config("PLAID_CLIENT_ID", default=""),
            "secret": config("PLAID_SECRET", default=""),
        },
    )
    return plaid_api.PlaidApi(ApiClient(configuration))

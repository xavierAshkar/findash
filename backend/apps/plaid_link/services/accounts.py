def sync_accounts(plaid_item):
    """
    Fetch accounts from Plaid and upsert them into the Account model.
    """
    from apps.plaid_link.utils import get_plaid_client
    from apps.accounts.models import Account
    client = get_plaid_client()

    # Plaid → internal account type mapping
    PLAID_TYPE_MAP = {
        "checking": Account.CHECKING,
        "savings": Account.SAVINGS,
        "credit card": Account.CREDIT_CARD,
        "credit": Account.CREDIT_CARD,
        "loan": Account.LOAN,
        "brokerage": Account.INVESTMENT,
        "investment": Account.INVESTMENT,
    }

    # Fetch accounts from Plaid
    response = client.accounts_get({
        "access_token": plaid_item.get_access_token()
    })

    for acct in response["accounts"]:
        # Plaid SDK returns enums — convert to strings safely
        plaid_type = acct["type"].value if acct.get("type") else None
        plaid_subtype = acct["subtype"].value if acct.get("subtype") else None

        # Determine internal account type
        account_type = PLAID_TYPE_MAP.get(
            plaid_subtype,
            PLAID_TYPE_MAP.get(plaid_type, Account.CHECKING)
        )

        # Upsert account
        Account.objects.update_or_create(
            user=plaid_item.user,
            external_account_id=acct["account_id"],
            defaults={
                "name": acct["name"],
                "institution_name": plaid_item.institution_name,
                "mask": acct.get("mask"),
                "account_type": account_type,
                "currency_code": acct["balances"]["iso_currency_code"] or "USD",
                "balance_current": acct["balances"]["current"] or 0,
                "balance_available": acct["balances"].get("available"),
                "credit_limit": acct["balances"].get("limit"),
                "plaid_item": plaid_item,
                "data_source": "plaid",
            },
        )

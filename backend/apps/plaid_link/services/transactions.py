from plaid.model.transactions_sync_request import TransactionsSyncRequest
from apps.transactions.services.normalization import normalize_plaid_amount


def sync_transactions(plaid_item):
    from apps.plaid_link.utils import get_plaid_client
    from apps.transactions.models import Transaction
    from apps.accounts.models import Account
    client = get_plaid_client()
    cursor = plaid_item.sync_cursor or ""

    has_more = True

    while has_more:
        request = TransactionsSyncRequest(
            access_token=plaid_item.get_access_token(),
            cursor=cursor,
        )

        response = client.transactions_sync(request).to_dict()

        added = response.get("added", [])
        modified = response.get("modified", [])
        removed = response.get("removed", [])

        for tx in added + modified:
            account = Account.objects.filter(
                user=plaid_item.user,
                external_account_id=tx["account_id"],
            ).first()

            if not account:
                continue

            normalized_amount = normalize_plaid_amount(tx["amount"])

            Transaction.objects.update_or_create(
                external_transaction_id=tx["transaction_id"],
                defaults={
                    "account": account,
                    "description": tx.get("name") or tx.get("merchant_name") or "Transaction",
                    "amount": normalized_amount,  # CHANGED
                    "date": tx["date"],
                    "pending": tx["pending"],
                    "currency_code": tx.get("iso_currency_code") or "USD",
                    "plaid_category_primary": (
                        tx["category"][0] if tx.get("category") else None
                    ),
                    "plaid_category_detailed": tx.get("category_id"),
                },
            )

        for tx in removed:
            Transaction.objects.filter(
                external_transaction_id=tx["transaction_id"]
            ).delete()

        cursor = response["next_cursor"]
        has_more = response["has_more"]

    plaid_item.sync_cursor = cursor
    plaid_item.save()

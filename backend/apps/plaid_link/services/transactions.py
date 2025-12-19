from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_request_options import TransactionsSyncRequestOptions

from apps.plaid_link.utils import get_plaid_client
from apps.transactions.models import Transaction
from apps.accounts.models import Account


def sync_transactions(plaid_item):
    client = get_plaid_client()
    cursor = plaid_item.sync_cursor

    has_more = True

    while has_more:
        request = TransactionsSyncRequest(
            access_token=plaid_item.access_token,
            cursor=cursor,
            options=TransactionsSyncRequestOptions(count=500),
        )

        response = client.transactions_sync(request).to_dict()

        added = response.get("added", [])
        modified = response.get("modified", [])
        removed = response.get("removed", [])

        for tx in added + modified:
            account = Account.objects.filter(
                plaid_account_id=tx["account_id"]
            ).first()

            if not account:
                continue

            Transaction.objects.update_or_create(
                plaid_transaction_id=tx["transaction_id"],
                defaults={
                    "user": plaid_item.user,
                    "account": account,
                    "name": tx["name"],
                    "amount": tx["amount"],
                    "date": tx["date"],
                    "pending": tx["pending"],
                    "plaid_category_primary": (
                        tx["category"][0] if tx.get("category") else None
                    ),
                    "plaid_category_detailed": tx.get("category_id"),
                },
            )

        for tx in removed:
            Transaction.objects.filter(
                plaid_transaction_id=tx["transaction_id"]
            ).delete()

        cursor = response["next_cursor"]
        has_more = response["has_more"]

    plaid_item.sync_cursor = cursor
    plaid_item.save()

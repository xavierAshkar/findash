import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from apps.plaid_link.services.accounts import sync_accounts
from apps.plaid_link.services.transactions import sync_transactions


from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest
)

from apps.plaid_link.models import PlaidItem
from apps.plaid_link.utils import get_plaid_client


@csrf_exempt
@require_POST
@login_required
def exchange_public_token(request):
    body = json.loads(request.body)
    public_token = body.get("public_token")

    if not public_token:
        return JsonResponse({"error": "Missing public_token"}, status=400)

    client = get_plaid_client()

    response = client.item_public_token_exchange(
        ItemPublicTokenExchangeRequest(public_token=public_token)
    )

    item, _ = PlaidItem.objects.get_or_create(
        user=request.user,
        defaults={"item_id": response["item_id"]},
    )

    item.set_access_token(response["access_token"])
    item.item_id = response["item_id"]
    item.save()

    sync_accounts(item)
    sync_transactions(item)

    return JsonResponse({"status": "ok"})

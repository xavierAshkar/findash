from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.plaid_link.models import PlaidItem
from apps.plaid_link.services.transactions import sync_transactions


@require_POST
@login_required
def sync_transactions_view(request):
    item = PlaidItem.objects.filter(user=request.user).first()

    if not item:
        return JsonResponse({"error": "No Plaid item linked"}, status=400)

    sync_transactions(item)
    return JsonResponse({"status": "transactions synced"})

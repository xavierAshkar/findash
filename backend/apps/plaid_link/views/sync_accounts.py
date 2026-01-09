from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from apps.plaid_link.models import PlaidItem


@csrf_exempt
@require_POST
@login_required
def sync_accounts_view(request):
    from apps.plaid_link.services.accounts import sync_accounts  # moved here

    item = PlaidItem.objects.filter(user=request.user).first()
    if not item:
        return JsonResponse({"error": "No Plaid item linked"}, status=400)

    sync_accounts(item)
    return JsonResponse({"status": "accounts synced"})

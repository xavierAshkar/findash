# backend/apps/ui/views/accounts.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.accounts.models import Account

@login_required
def accounts(request):
    accounts_qs = (
        Account.objects
        .filter(user=request.user)
        .order_by("account_type", "name")
    )
    return render(
        request,
        "app/accounts/index.html",
        {"accounts": accounts_qs},
    )

# backend/apps/ui/views/dashboard.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.accounts.models import Account
from apps.transactions.models import Transaction

@login_required
def dashboard(request):
    accounts = (
        Account.objects
        .filter(user=request.user)
        .order_by("account_type", "name")[:5]
    )

    recent_transactions = (
        Transaction.objects
        .select_related("account")
        .filter(account__user=request.user)
        .order_by("-date", "-created_at")[:8]
    )

    return render(
        request,
        "app/dashboard/index.html",
        {
            "accounts": accounts,
            "recent_transactions": recent_transactions,
        },
    )

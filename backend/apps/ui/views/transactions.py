# backend/apps/ui/views/transactions.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.transactions.models import Transaction


@login_required
def transactions(request):
    tx_qs = (
        Transaction.objects
        .select_related("account")
        .filter(account__user=request.user)
        .order_by("-date", "-created_at")[:20]
    )

    return render(
        request,
        "app/transactions/index.html",
        {"transactions": tx_qs},
    )

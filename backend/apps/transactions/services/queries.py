# backend/apps/transactions/services/queries.py
from django.db.models import QuerySet
from apps.transactions.models import Transaction

from decimal import Decimal
from django.db.models import Sum

def get_recent_transactions(*, user, limit: int = 5, exclude_transfers: bool = True) -> QuerySet[Transaction]:
    qs = (
        Transaction.objects
        .filter(account__user=user)
        .select_related("account")
        .order_by("-date", "-created_at")
    )

    if exclude_transfers:
        qs = qs.exclude(category="TRANSFER")

    return qs[:limit]

def get_month_spend_total(*, user, start_date, end_date, include_pending: bool = False) -> Decimal:
    qs = Transaction.objects.filter(
        account__user=user,
        date__gte=start_date,
        date__lte=end_date,
    )

    if not include_pending:
        qs = qs.filter(pending=False)

    # Spending = negative amounts, excluding transfers and debt payments
    qs = qs.filter(amount__lt=0).exclude(category__in=["TRANSFER", "DEBT_PAYMENT"])

    total = qs.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # total is negative (since spending amounts are negative); return positive for display
    return abs(total).quantize(Decimal("0.01"))

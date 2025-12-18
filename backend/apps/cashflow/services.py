from decimal import Decimal
from datetime import date
from calendar import monthrange

from apps.transactions.models import Transaction


def _get_month_bounds(month):
    if month is None:
        today = date.today()
        year, month_num = today.year, today.month
    else:
        year, month_num = month.year, month.month

    start = date(year, month_num, 1)
    end = date(year, month_num, monthrange(year, month_num)[1])
    return start, end


def get_monthly_cashflow(user, month=None):
    start_date, end_date = _get_month_bounds(month)

    transactions = Transaction.objects.filter(
        account__user=user,
        date__gte=start_date,
        date__lte=end_date,
    )

    income = Decimal("0.00")
    expenses = Decimal("0.00")
    by_category = {}

    for tx in transactions:
        # Transfers never affect cash flow
        if tx.transaction_type == Transaction.TRANSFER:
            continue

        # Money in
        if tx.amount > 0:
            income += tx.amount
            continue

        # Money out
        amount = abs(tx.amount)
        expenses += amount

        category = tx.category or "other"
        by_category[category] = by_category.get(category, Decimal("0.00")) + amount

    return {
        "month": start_date.strftime("%Y-%m"),
        "income": income,
        "expenses": expenses,
        "net": income - expenses,
        "by_category": by_category,
    }

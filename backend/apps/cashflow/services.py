# backend/apps/cashflow/services.py
from decimal import Decimal
from datetime import date
from calendar import monthrange
from dateutil.relativedelta import relativedelta

from apps.accounts.models import Account
from apps.transactions.models import Transaction

def _month_start(d: date) -> date:
    return d.replace(day=1)

def _get_month_bounds(month):
    if month is None:
        today = date.today()
        year, month_num = today.year, today.month
    else:
        year, month_num = month.year, month.month

    start = date(year, month_num, 1)
    end = date(year, month_num, monthrange(year, month_num)[1])
    return start, end

# Cashflow counts spending at purchase time; internal transfers and payments are excluded.
def get_monthly_cashflow(user, month=None):
    start_date, end_date = _get_month_bounds(month)

    transactions = Transaction.objects.select_related("account").filter(
        account__user=user,
        date__gte=start_date,
        date__lte=end_date,
    )

    income = Decimal("0.00")
    expenses = Decimal("0.00")
    by_category = {}

    for tx in transactions:
        # Ignore internal moves (MVP): transfers + payments
        if tx.is_transfer or tx.plaid_category_primary in {"Transfer", "Payment"}:
            continue

        # Ignore investments entirely
        if tx.account.account_type == Account.INVESTMENT:
            continue

        if tx.is_income and not tx.account.is_debt:
            income += tx.amount

        elif tx.is_expense:
            amount = abs(tx.amount)
            expenses += amount
            cat = tx.category or "uncategorized"
            by_category[cat] = by_category.get(cat, Decimal("0.00")) + amount

    return {
        "month": start_date.strftime("%Y-%m"),
        "income": income,
        "expenses": expenses,
        "net": income - expenses,
        "by_category": by_category,
    }


def get_monthly_cashflow_comparison(user, month=None):
    """
    Returns:
    {
      current: {...},
      previous: {...},
      delta: {...},
      delta_by_category: {...}
    }
    """
    if month is None:
        current_month = _month_start(date.today())
    else:
        current_month = _month_start(month)

    previous_month = current_month - relativedelta(months=1)

    current = get_monthly_cashflow(user, current_month)
    previous = get_monthly_cashflow(user, previous_month)

    delta = {
        "income": current["income"] - previous["income"],
        "expenses": current["expenses"] - previous["expenses"],
        "net": current["net"] - previous["net"],
    }

    # Category deltas (union of both months)
    delta_by_category = {}

    all_categories = set(current["by_category"]) | set(previous["by_category"])

    for category in all_categories:
        current_val = current["by_category"].get(category, Decimal("0.00"))
        previous_val = previous["by_category"].get(category, Decimal("0.00"))
        delta_by_category[category] = current_val - previous_val

    return {
        "current": current,
        "previous": previous,
        "delta": delta,
        "delta_by_category": delta_by_category,
    }

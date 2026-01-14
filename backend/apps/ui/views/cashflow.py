# backend/apps/ui/views/cashflow.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.cashflow.services import get_monthly_cashflow_comparison

@login_required
def cashflow(request):
    data = get_monthly_cashflow_comparison(request.user)
    return render(
        request,
        "app/cashflow/index.html",
        {"cashflow": data},
    )

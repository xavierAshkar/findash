from django.urls import path
from .views.dashboard import dashboard
from .views.accounts import accounts
from .views.transactions import transactions
from .views.cashflow import cashflow
from .views.goals import goals

app_name = "ui"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("accounts/", accounts, name="accounts"),
    path("transactions/", transactions, name="transactions"),
    path("cashflow/", cashflow, name="cashflow"),
    path("goals/", goals, name="goals"),
]

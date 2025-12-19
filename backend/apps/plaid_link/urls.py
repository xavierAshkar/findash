from django.urls import path
from apps.plaid_link.views.link import create_link_token
from apps.plaid_link.views.exchange import exchange_public_token
from apps.plaid_link.views.test import plaid_test
from apps.plaid_link.views.sync_accounts import sync_accounts_view
from apps.plaid_link.views.sync_transactions import sync_transactions_view

urlpatterns = [
    path("link-token/", create_link_token, name="plaid_link_token"),
    path("exchange/", exchange_public_token, name="plaid_exchange"),
    path("test/", plaid_test),
    path("sync-accounts/", sync_accounts_view),
    path("sync-transactions/", sync_transactions_view),
]

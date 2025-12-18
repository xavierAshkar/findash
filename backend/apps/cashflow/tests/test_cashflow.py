from decimal import Decimal
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.accounts.models import Account
from apps.transactions.models import Transaction
from apps.cashflow.services import (
    get_monthly_cashflow,
    get_monthly_cashflow_comparison,
)

User = get_user_model()


class CashflowTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="password123",
        )

        cls.checking = Account.objects.create(
            user=cls.user,
            name="Checking",
            category="checking",
        )

        cls.credit = Account.objects.create(
            user=cls.user,
            name="Credit Card",
            category="credit_card",
        )

        cls.savings = Account.objects.create(
            user=cls.user,
            name="Savings",
            category="savings",
        )

        # December data
        Transaction.objects.create(
            account=cls.checking,
            amount=Decimal("3000"),
            transaction_type="income",
            category="other",
            date=date(2025, 12, 1),
            description="Paycheck",
        )

        Transaction.objects.create(
            account=cls.checking,
            amount=Decimal("-1200"),
            transaction_type="expense",
            category="rent",
            date=date(2025, 12, 2),
            description="Rent",
        )

        Transaction.objects.create(
            account=cls.credit,
            amount=Decimal("150"),
            transaction_type="expense",
            category="shopping",
            date=date(2025, 12, 5),
            description="Shopping",
        )

        Transaction.objects.create(
            account=cls.credit,
            amount=Decimal("-50"),
            transaction_type="income",
            category="other",
            date=date(2025, 12, 10),
            description="Cashback",
        )

        # November data
        Transaction.objects.create(
            account=cls.checking,
            amount=Decimal("2800"),
            transaction_type="income",
            category="other",
            date=date(2025, 11, 1),
            description="Paycheck",
        )

    def test_get_monthly_cashflow(self):
        result = get_monthly_cashflow(self.user, date(2025, 12, 1))

        self.assertEqual(result["income"], Decimal("3050"))
        self.assertEqual(result["expenses"], Decimal("1350"))
        self.assertEqual(result["net"], Decimal("1700"))

        self.assertEqual(result["by_category"]["rent"], Decimal("1200"))
        self.assertEqual(result["by_category"]["shopping"], Decimal("150"))

    def test_monthly_cashflow_comparison(self):
        result = get_monthly_cashflow_comparison(self.user, date(2025, 12, 1))

        self.assertEqual(result["delta"]["income"], Decimal("250"))
        self.assertEqual(result["delta"]["expenses"], Decimal("1350"))
        self.assertEqual(result["delta"]["net"], Decimal("-1100"))

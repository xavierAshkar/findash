from decimal import Decimal
from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.accounts.models import Account
from apps.transactions.models import Transaction

User = get_user_model()


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
        )

        self.checking = Account.objects.create(
            user=self.user,
            name="Checking",
            account_type=Account.CHECKING,
        )

        self.credit = Account.objects.create(
            user=self.user,
            name="Credit Card",
            account_type=Account.CREDIT_CARD,
        )

    def test_checking_income(self):
        tx = Transaction.objects.create(
            account=self.checking,
            amount=Decimal("2000"),
            date=date.today(),
            description="Paycheck",
        )
        self.assertTrue(tx.is_income)
        self.assertFalse(tx.is_expense)

    def test_checking_expense(self):
        tx = Transaction.objects.create(
            account=self.checking,
            amount=Decimal("-100"),
            date=date.today(),
            description="Groceries",
        )
        self.assertTrue(tx.is_expense)

    def test_credit_purchase(self):
        tx = Transaction.objects.create(
            account=self.credit,
            amount=Decimal("50"),
            date=date.today(),
            description="Shopping",
        )
        self.assertTrue(tx.is_debt_increase)
        self.assertFalse(tx.is_income)

    def test_credit_payment(self):
        tx = Transaction.objects.create(
            account=self.credit,
            amount=Decimal("-200"),
            date=date.today(),
            description="Card Payment",
        )
        self.assertTrue(tx.is_debt_payment)

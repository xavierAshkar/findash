from decimal import Decimal

def normalize_plaid_amount(plaid_amount) -> Decimal:
    """
    Plaid convention: outflow is positive, inflow is negative.
    App convention: inflow positive, outflow negative.
    """
    return -Decimal(str(plaid_amount))

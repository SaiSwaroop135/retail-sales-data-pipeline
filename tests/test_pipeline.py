import sys
from pathlib import Path
from decimal import Decimal

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "src")
)

from extract_sales import validate_sales, transform_sales


def test_valid_sales():
    records = [
        {
            "order_id": "1001",
            "product": "Milk",
            "quantity": "2",
            "price": "4.50"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 1
    assert len(invalid) == 0


def test_invalid_sales():
    records = [
        {
            "order_id": "1002",
            "product": "Bread",
            "quantity": "-2",
            "price": "3.00"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 0
    assert len(invalid) == 1


def test_revenue_calculation():
    records = [
        {
            "order_id": "1003",
            "product": "Coffee",
            "quantity": "2",
            "price": "8.00"
        }
    ]

    result = transform_sales(records)

    assert result[0]["revenue"] == Decimal("16.00")

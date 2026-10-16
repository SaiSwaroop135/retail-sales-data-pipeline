
import csv
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "src")
)

from extract_sales import (
    extract_sales,
    validate_sales,
    transform_sales,
    save_processed_sales,
    save_rejected_sales,
)


# TEST 1: Valid sales records
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


# TEST 2: Negative quantity
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


# TEST 3: Revenue calculation
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


# TEST 4: Zero quantity
def test_zero_quantity():
    records = [
        {
            "order_id": "1004",
            "product": "Eggs",
            "quantity": "0",
            "price": "5.00"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 0
    assert len(invalid) == 1


# TEST 5: Negative price
def test_negative_price():
    records = [
        {
            "order_id": "1005",
            "product": "Bread",
            "quantity": "2",
            "price": "-3.00"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 0
    assert len(invalid) == 1


# TEST 6: Missing order ID
def test_missing_order_id():
    records = [
        {
            "order_id": "",
            "product": "Milk",
            "quantity": "2",
            "price": "4.00"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 0
    assert len(invalid) == 1


# TEST 7: Missing product
def test_missing_product():
    records = [
        {
            "order_id": "1007",
            "product": "",
            "quantity": "2",
            "price": "4.00"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 0
    assert len(invalid) == 1


# TEST 8: Invalid quantity format
def test_invalid_quantity_format():
    records = [
        {
            "order_id": "1008",
            "product": "Coffee",
            "quantity": "abc",
            "price": "5.00"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 0
    assert len(invalid) == 1


# TEST 9: Invalid price format
def test_invalid_price_format():
    records = [
        {
            "order_id": "1009",
            "product": "Coffee",
            "quantity": "2",
            "price": "invalid"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 0
    assert len(invalid) == 1


# TEST 10: Extract sales from CSV
def test_extract_sales(tmp_path):
    csv_file = tmp_path / "test_sales.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["order_id", "product", "quantity", "price"]
        )

        writer.writeheader()
        writer.writerow({
            "order_id": "1010",
            "product": "Milk",
            "quantity": "3",
            "price": "4.00"
        })

    records = extract_sales(csv_file)

    assert len(records) == 1
    assert records[0]["product"] == "Milk"
    assert records[0]["quantity"] == "3"


# TEST 11: Save processed sales
def test_save_processed_sales(tmp_path):
    output_file = tmp_path / "clean_sales.csv"

    clean_sales = [
        {
            "order_id": "1011",
            "product": "Coffee",
            "quantity": 2,
            "price": Decimal("5.00"),
            "revenue": Decimal("10.00")
        }
    ]

    save_processed_sales(clean_sales, output_file)

    assert output_file.exists()

    with open(output_file, newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    assert len(records) == 1
    assert records[0]["revenue"] == "10.00"


# TEST 12: Save rejected sales
def test_save_rejected_sales(tmp_path):
    output_file = tmp_path / "rejected_sales.csv"

    invalid_sales = [
        {
            "order_id": "1012",
            "product": "Bread",
            "quantity": "-1",
            "price": "3.00"
        }
    ]

    save_rejected_sales(invalid_sales, output_file)

    assert output_file.exists()

    with open(output_file, newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    assert len(records) == 1
    assert records[0]["order_id"] == "1012"


# TEST 13: Empty dataset
def test_empty_dataset():
    valid, invalid = validate_sales([])

    assert valid == []
    assert invalid == []


# TEST 14: Multiple valid records
def test_multiple_valid_records():
    records = [
        {
            "order_id": "1013",
            "product": "Milk",
            "quantity": "2",
            "price": "4.00"
        },
        {
            "order_id": "1014",
            "product": "Eggs",
            "quantity": "3",
            "price": "5.00"
        }
    ]

    valid, invalid = validate_sales(records)

    assert len(valid) == 2
    assert len(invalid) == 0


# TEST 15: Missing input CSV
def test_missing_input_file(tmp_path):
    missing_file = tmp_path / "missing_sales.csv"

    with pytest.raises(FileNotFoundError):
        extract_sales(missing_file)

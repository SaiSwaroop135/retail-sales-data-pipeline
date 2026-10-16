import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from extract_sales import (
    validate_sales,
    generate_data_quality_report
)


def make_record(order_id="1001", product="Milk",
                quantity="2", price="4.50"):
    return {
        "order_id": order_id,
        "product": product,
        "quantity": quantity,
        "price": price
    }


def test_valid_record_has_no_rejection_reason():
    valid, invalid = validate_sales([make_record()])

    assert len(valid) == 1
    assert len(invalid) == 0


def test_invalid_quantity_has_rejection_reason():
    valid, invalid = validate_sales([
        make_record(quantity="-2")
    ])

    assert len(valid) == 0
    assert invalid[0]["rejection_reason"] == (
        "Quantity must be greater than zero"
    )


def test_invalid_price_has_rejection_reason():
    _, invalid = validate_sales([
        make_record(price="abc")
    ])

    assert invalid[0]["rejection_reason"] == (
        "Invalid price format"
    )


def test_multiple_rejection_reasons():
    _, invalid = validate_sales([
        make_record(product="", quantity="-1")
    ])

    reasons = invalid[0]["rejection_reason"]

    assert "Missing product name" in reasons
    assert "Quantity must be greater than zero" in reasons


def test_quality_score_calculation(tmp_path):
    records = [
        make_record(order_id="1001"),
        make_record(order_id="1002", quantity="-1"),
        make_record(order_id="1003", price="abc")
    ]

    valid, invalid = validate_sales(records)

    report = generate_data_quality_report(
        records,
        valid,
        invalid,
        tmp_path / "quality.csv"
    )

    assert report["total_records"] == 3
    assert report["valid_records"] == 1
    assert report["invalid_records"] == 2
    assert report["quality_score"] == 33.33


def test_quality_report_csv_created(tmp_path):
    records = [make_record()]
    valid, invalid = validate_sales(records)

    output_file = tmp_path / "quality.csv"

    generate_data_quality_report(
        records, valid, invalid, output_file
    )

    assert output_file.exists()

    with open(output_file, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    metrics = {
        row["metric"]: row["value"]
        for row in rows
    }

    assert metrics["Total Records"] == "1"
    assert metrics["Valid Records"] == "1"
    assert metrics["Data Quality Score (%)"] == "100.0"


def test_empty_dataset_quality_score(tmp_path):
    report = generate_data_quality_report(
        [], [], [], tmp_path / "empty.csv"
    )

    assert report["total_records"] == 0
    assert report["quality_score"] == 0.0


def test_rejection_reason_counts(tmp_path):
    records = [
        make_record(order_id="1001", quantity="-1"),
        make_record(order_id="1002", quantity="abc"),
        make_record(order_id="1003", quantity="-5")
    ]

    valid, invalid = validate_sales(records)

    report = generate_data_quality_report(
        records,
        valid,
        invalid,
        tmp_path / "quality.csv"
    )

    assert report["rejection_reasons"][
        "Quantity must be greater than zero"
    ] == 2

    assert report["rejection_reasons"][
        "Invalid quantity format"
    ] == 1
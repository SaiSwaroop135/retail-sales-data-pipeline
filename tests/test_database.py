import csv
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "src")
)

from load_sales import load_sales


@pytest.fixture
def sample_database(tmp_path):
    csv_file = tmp_path / "clean_sales.csv"
    db_file = tmp_path / "test_sales.db"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "order_id",
                "product",
                "quantity",
                "price",
                "revenue"
            ]
        )

        writer.writeheader()
        writer.writerows([
            {
                "order_id": "1001",
                "product": "Milk",
                "quantity": "2",
                "price": "4.50",
                "revenue": "9.00"
            },
            {
                "order_id": "1002",
                "product": "Coffee",
                "quantity": "3",
                "price": "5.00",
                "revenue": "15.00"
            }
        ])

    return csv_file, db_file


# TEST 16: Database file creation
def test_database_creation(sample_database):
    csv_file, db_file = sample_database

    load_sales(csv_file, db_file)

    assert db_file.exists()


# TEST 17: Records inserted correctly
def test_database_record_count(sample_database):
    csv_file, db_file = sample_database

    load_sales(csv_file, db_file)

    with sqlite3.connect(db_file) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

    assert count == 2


# TEST 18: Verify stored sales values
def test_database_values(sample_database):
    csv_file, db_file = sample_database

    load_sales(csv_file, db_file)

    with sqlite3.connect(db_file) as connection:
        result = connection.execute(
            "SELECT product, quantity FROM sales WHERE order_id = 1001"
        ).fetchone()

    assert result == ("Milk", 2)


# TEST 19: Prevent duplicate order IDs
def test_duplicate_order_ids(sample_database):
    csv_file, db_file = sample_database

    load_sales(csv_file, db_file)
    load_sales(csv_file, db_file)

    with sqlite3.connect(db_file) as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

    assert count == 2


# TEST 20: Verify total database revenue
def test_database_revenue(sample_database):
    csv_file, db_file = sample_database

    load_sales(csv_file, db_file)

    with sqlite3.connect(db_file) as connection:
        revenue = connection.execute(
            "SELECT SUM(revenue) FROM sales"
        ).fetchone()[0]

    assert revenue == pytest.approx(24.00)


# TEST 21: Missing CSV file
def test_missing_csv_file(tmp_path):
    csv_file = tmp_path / "missing.csv"
    db_file = tmp_path / "test.db"

    with pytest.raises(FileNotFoundError):
        load_sales(csv_file, db_file)

    assert not db_file.exists()
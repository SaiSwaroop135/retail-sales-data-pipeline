import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "processed" / "clean_sales.csv"
DB_FILE = BASE_DIR / "data" / "retail_sales.db"


def load_sales(csv_file=CSV_FILE, db_file=DB_FILE):
    csv_file = Path(csv_file)
    db_file = Path(db_file)

    if not csv_file.is_file():
        raise FileNotFoundError(
            f"Cleaned sales file not found: {csv_file}"
        )

    # Read and validate all input rows before modifying the database.
    with csv_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {
            "order_id", "product", "quantity", "price", "revenue"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("Cleaned CSV is missing required columns")

        records = [
            (
                int(row["order_id"]),
                row["product"],
                int(row["quantity"]),
                row["price"],
                row["revenue"]
            )
            for row in reader
        ]

    db_file.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_file)

    try:
        # Create the table if it does not exist.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                order_id INTEGER PRIMARY KEY,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price NUMERIC NOT NULL,
                revenue NUMERIC NOT NULL
            )
        """)

        # Start a transaction for the full refresh.
        connection.execute("BEGIN")

        # Remove records from the previous load.
        connection.execute("DELETE FROM sales")

        # Insert the latest cleaned records.
        connection.executemany("""
            INSERT INTO sales
            (order_id, product, quantity, price, revenue)
            VALUES (?, ?, ?, ?, ?)
        """, records)

        connection.commit()

        total_records = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        print("DATABASE LOAD COMPLETED")
        print("Total Records in Database:", total_records)

        return total_records

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    load_sales()
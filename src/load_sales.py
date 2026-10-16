import csv
import sqlite3
from pathlib import Path


# ==========================================
# PROJECT FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "processed" / "clean_sales.csv"

DB_FILE = BASE_DIR / "data" / "retail_sales.db"


# ==========================================
# LOAD SALES DATA INTO SQLITE
# ==========================================

def load_sales(csv_file=None, db_file=None):

    if csv_file is None:
        csv_file = CSV_FILE

    if db_file is None:
        db_file = DB_FILE

    csv_file = Path(csv_file)
    db_file = Path(db_file)

    # Check that the input file exists
    if not csv_file.is_file():
        raise FileNotFoundError(
            f"Cleaned sales CSV file not found: {csv_file}"
        )

    # Create database directory if necessary
    db_file.parent.mkdir(parents=True, exist_ok=True)

    # Automatically close connection
    try:
        with sqlite3.connect(db_file) as connection:

            cursor = connection.cursor()

            # Create sales table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    order_id INTEGER PRIMARY KEY,
                    product TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price NUMERIC NOT NULL,
                    revenue NUMERIC NOT NULL
                )
            """)

            # Read cleaned sales CSV
            with open(
                csv_file,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    cursor.execute("""
                        INSERT OR REPLACE INTO sales
                        (order_id, product, quantity, price, revenue)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        int(row["order_id"]),
                        row["product"],
                        int(row["quantity"]),
                        row["price"],
                        row["revenue"]
                    ))

            # Save changes
            connection.commit()

            # Verify loaded records
            cursor.execute("SELECT COUNT(*) FROM sales")

            total_records = cursor.fetchone()[0]

    except (sqlite3.Error, OSError, ValueError, KeyError):
        print("DATABASE LOAD FAILED")
        raise

    print("DATABASE LOAD COMPLETED")
    print("Total Records in Database:", total_records)

    return total_records


# ==========================================
# RUN DIRECTLY
# ==========================================

if __name__ == "__main__":
    load_sales()
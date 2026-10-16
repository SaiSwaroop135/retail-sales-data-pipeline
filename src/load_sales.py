import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "processed" / "clean_sales.csv"
DB_FILE = BASE_DIR / "data" / "retail_sales.db"

def load_sales():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            order_id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price NUMERIC NOT NULL,
            revenue NUMERIC NOT NULL
        )
    """)

    with open(CSV_FILE, "r", newline="") as file:
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

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM sales")
    total_records = cursor.fetchone()[0]

    print("DATABASE LOAD COMPLETED")
    print("Total Records in Database:", total_records)

    connection.close()

if __name__ == "__main__":
    load_sales()

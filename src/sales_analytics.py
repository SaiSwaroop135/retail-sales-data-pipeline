import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "retail_sales.db"

def analyze_sales():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    print("========== SALES ANALYTICS ==========")

    # 1. Total Revenue
    cursor.execute("SELECT SUM(revenue) FROM sales")
    total_revenue = cursor.fetchone()[0]
    print("Total Revenue: $", total_revenue)

    # 2. Total Orders
    cursor.execute("SELECT COUNT(*) FROM sales")
    total_orders = cursor.fetchone()[0]
    print("Total Orders:", total_orders)

    # 3. Total Quantity Sold
    cursor.execute("SELECT SUM(quantity) FROM sales")
    total_quantity = cursor.fetchone()[0]
    print("Total Quantity Sold:", total_quantity)

    # 4. Revenue by Product
    print("\nREVENUE BY PRODUCT")

    cursor.execute("""
        SELECT product, SUM(revenue)
        FROM sales
        GROUP BY product
        ORDER BY SUM(revenue) DESC
    """)

    for product, revenue in cursor.fetchall():
        print(product, ": $", revenue)

    # 5. Highest Revenue Product
    cursor.execute("""
        SELECT product, SUM(revenue) AS total
        FROM sales
        GROUP BY product
        ORDER BY total DESC
        LIMIT 1
    """)

    top_product = cursor.fetchone()

    print("\nTop Selling Product:", top_product[0])
    print("Top Product Revenue: $", top_product[1])

    connection.close()

if __name__ == "__main__":
    analyze_sales()

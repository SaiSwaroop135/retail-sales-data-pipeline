import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation


# ==========================================
# PROJECT FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "raw" / "sales.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "clean_sales.csv"

REJECTED_FILE = BASE_DIR / "data" / "processed" / "rejected_sales.csv"


# ==========================================
# STEP 1: EXTRACT SALES DATA
# ==========================================

def extract_sales(file_path):
    sales_data = []

    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sales_data.append(row)

    return sales_data


# ==========================================
# STEP 2: VALIDATE SALES DATA
# ==========================================

def validate_sales(transactions):
    valid_records = []
    invalid_records = []

    for row in transactions:
        order_id = row.get("order_id", "").strip()
        product = row.get("product", "").strip()

        if not order_id or not product:
            invalid_records.append(row)
            continue

        try:
            quantity = int(row["quantity"])
            price = Decimal(row["price"])

        except (ValueError, TypeError, InvalidOperation):
            invalid_records.append(row)
            continue

        if quantity <= 0 or not price.is_finite() or price < 0:
            invalid_records.append(row)
            continue

        valid_records.append(row)

    return valid_records, invalid_records


# ==========================================
# STEP 3: TRANSFORM SALES DATA
# ==========================================

def transform_sales(valid_sales):
    transformed_records = []

    for row in valid_sales:
        order_id = row["order_id"]
        product = row["product"]

        quantity = int(row["quantity"])
        price = Decimal(row["price"])

        revenue = quantity * price

        transformed_row = {
            "order_id": order_id,
            "product": product,
            "quantity": quantity,
            "price": price,
            "revenue": revenue
        }

        transformed_records.append(transformed_row)

    return transformed_records


# ==========================================
# STEP 4: GENERATE PIPELINE SUMMARY
# ==========================================

def generate_pipeline_summary(transactions, clean_sales, invalid_sales):

    total_revenue = Decimal("0.00")

    for sale in clean_sales:
        total_revenue += sale["revenue"]

    print("\n==============================")
    print("RETAIL SALES PIPELINE SUMMARY")
    print("==============================")

    print("Total Records Extracted:", len(transactions))
    print("Valid Records:", len(clean_sales))
    print("Invalid Records:", len(invalid_sales))
    print("Total Revenue: $", format(total_revenue, ".2f"))

    print("==============================")

    return total_revenue


# ==========================================
# STEP 5: SAVE CLEANED SALES DATA
# ==========================================

def save_processed_sales(clean_sales, output_file):

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "order_id",
            "product",
            "quantity",
            "price",
            "revenue"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(clean_sales)


# ==========================================
# STEP 6: SAVE REJECTED SALES DATA
# ==========================================

def save_rejected_sales(invalid_sales, output_file):

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "order_id",
            "product",
            "quantity",
            "price"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(invalid_sales)


# ==========================================
# STEP 7: MAIN PIPELINE EXECUTION
# ==========================================

def main():

    # Extract
    transactions = extract_sales(CSV_FILE)

    print("Extracted Transactions:")

    for transaction in transactions:
        print(transaction)

    print("Total Records Extracted:", len(transactions))

    # Validate
    valid_sales, invalid_sales = validate_sales(transactions)

    print("\n--------------------------")
    print("DATA VALIDATION SUMMARY")
    print("Valid Records:", len(valid_sales))
    print("Invalid Records:", len(invalid_sales))

    # Transform
    clean_sales = transform_sales(valid_sales)

    print("\n--------------------------")
    print("TRANSFORMED SALES DATA")

    for sale in clean_sales:
        print(sale)

    print("Total Transformed Records:", len(clean_sales))

    # Generate summary
    pipeline_revenue = generate_pipeline_summary(
        transactions,
        clean_sales,
        invalid_sales
    )

    # Save cleaned records
    save_processed_sales(clean_sales, OUTPUT_FILE)

    print("Cleaned sales data saved successfully!")

    # Save rejected records
    save_rejected_sales(invalid_sales, REJECTED_FILE)

    print("Rejected sales data saved successfully!")

    print("\n===================================")
    print("PIPELINE EXECUTION COMPLETED")
    print("===================================")


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()

import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
from collections import Counter


# ==========================================
# PROJECT FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "raw" / "sales.csv"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "clean_sales.csv"

REJECTED_FILE = BASE_DIR / "data" / "processed" / "rejected_sales.csv"

QUALITY_REPORT_FILE = (
    BASE_DIR / "data" / "processed" / "data_quality_report.csv"
)


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
        reasons = []

        order_id = str(row.get("order_id") or "").strip()
        product = str(row.get("product") or "").strip()

        if not order_id:
            reasons.append("Missing order ID")
        elif not order_id.isdecimal():
            reasons.append("Order ID must be numeric")

        if not product:
            reasons.append("Missing product name")

        try:
            quantity = int(row.get("quantity"))
            if quantity <= 0:
                reasons.append("Quantity must be greater than zero")
        except (ValueError, TypeError):
            reasons.append("Invalid quantity format")

        try:
            price = Decimal(row.get("price"))
            if not price.is_finite():
                reasons.append("Price must be finite")
            elif price < 0:
                reasons.append("Price cannot be negative")
        except (ValueError, TypeError, InvalidOperation):
            reasons.append("Invalid price format")

        if reasons:
            rejected_row = dict(row)
            rejected_row["rejection_reason"] = "; ".join(reasons)
            invalid_records.append(rejected_row)
        else:
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

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "order_id",
        "product",
        "quantity",
        "price",
        "revenue"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(clean_sales)


# ==========================================
# STEP 6: SAVE REJECTED SALES DATA
# ==========================================

def save_rejected_sales(invalid_sales, output_file):

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "order_id",
        "product",
        "quantity",
        "price",
        "rejection_reason"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(invalid_sales)


# ==========================================
# STEP 7: GENERATE DATA QUALITY REPORT
# ==========================================

def generate_data_quality_report(
    transactions,
    valid_sales,
    invalid_sales,
    output_file=QUALITY_REPORT_FILE
):
    total_records = len(transactions)
    valid_count = len(valid_sales)
    invalid_count = len(invalid_sales)

    quality_score = (
        round((valid_count / total_records) * 100, 2)
        if total_records > 0
        else 0.0
    )

    rejection_counts = Counter()

    for row in invalid_sales:
        reasons = row.get("rejection_reason", "")

        for reason in reasons.split(";"):
            reason = reason.strip()
            if reason:
                rejection_counts[reason] += 1

    report_rows = [
        {"metric": "Total Records", "value": total_records},
        {"metric": "Valid Records", "value": valid_count},
        {"metric": "Invalid Records", "value": invalid_count},
        {"metric": "Data Quality Score (%)", "value": quality_score}
    ]

    for reason, count in sorted(rejection_counts.items()):
        report_rows.append({
            "metric": f"Rejection Reason: {reason}",
            "value": count
        })

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["metric", "value"]
        )

        writer.writeheader()
        writer.writerows(report_rows)

    print("\n===================================")
    print("DATA QUALITY REPORT")
    print("===================================")
    print("Total Records:", total_records)
    print("Valid Records:", valid_count)
    print("Invalid Records:", invalid_count)
    print(f"Data Quality Score: {quality_score:.2f}%")

    print("\nREJECTION REASONS")

    if rejection_counts:
        for reason, count in sorted(rejection_counts.items()):
            print(f"{reason}: {count}")
    else:
        print("No rejected records")

    print("\nData quality report saved successfully!")

    return {
        "total_records": total_records,
        "valid_records": valid_count,
        "invalid_records": invalid_count,
        "quality_score": quality_score,
        "rejection_reasons": dict(rejection_counts)
    }


# ==========================================
# STEP 8: MAIN PIPELINE EXECUTION
# ==========================================

def main():

    transactions = extract_sales(CSV_FILE)

    print("STEP 1: EXTRACTING SALES DATA")
    print("Total Records Extracted:", len(transactions))

    valid_sales, invalid_sales = validate_sales(transactions)

    print("\nSTEP 2: VALIDATING SALES DATA")
    print("Valid Records:", len(valid_sales))
    print("Invalid Records:", len(invalid_sales))

    clean_sales = transform_sales(valid_sales)

    print("\nSTEP 3: TRANSFORMING SALES DATA")
    print("Total Transformed Records:", len(clean_sales))

    print("\nSTEP 4: SAVING PROCESSED DATA")

    save_processed_sales(clean_sales, OUTPUT_FILE)
    save_rejected_sales(invalid_sales, REJECTED_FILE)

    print("Cleaned sales data saved successfully!")
    print("Rejected sales data saved successfully!")

    print("\nSTEP 5: GENERATING PIPELINE SUMMARY")

    generate_pipeline_summary(
        transactions,
        clean_sales,
        invalid_sales
    )

    print("\nSTEP 6: GENERATING DATA QUALITY REPORT")

    generate_data_quality_report(
        transactions,
        valid_sales,
        invalid_sales
    )

    print("\n===================================")
    print("EXTRACTION AND QUALITY CHECKS COMPLETED")
    print("===================================")


# ==========================================
# PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
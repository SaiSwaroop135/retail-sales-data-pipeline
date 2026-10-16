import csv

total_revenue = 0
valid_records = 0
invalid_records = 0

with open("sales.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        order_id = row["order_id"]
        product = row["product"]

        if not order_id or not product:
            print("Rejected: Missing order ID or product")
            invalid_records += 1
            continue

        try:
            quantity = int(row["quantity"])
            price = float(row["price"])

        except (ValueError, TypeError):
            print("Rejected Order:", order_id)
            print("Reason: Invalid quantity or price")
            invalid_records += 1
            continue

        if quantity <= 0 or price < 0:
            print("Rejected Order:", order_id)
            print("Reason: Quantity or price violates business rules")
            invalid_records += 1
            continue

        revenue = quantity * price
        total_revenue += revenue
        valid_records += 1

        print("Order ID:", order_id)
        print("Product:", product)
        print("Revenue: $", format(revenue, ".2f"))
        print("--------------------")

print("PIPELINE SUMMARY")
print("Valid Records:", valid_records)
print("Invalid Records:", invalid_records)
print("Total Revenue: $", format(total_revenue, ".2f"))
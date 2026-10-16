# import csv

# with open("sales.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)

#     for row in reader:
#         print("Order ID:", row["order_id"])
#         print("Product:", row["product"])
#         print("Quantity:", row["quantity"])
#         print("Price:", row["price"])
#         print("--------------------")



#************************** Type Conversion ************************
# import csv

# with open("sales.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)

#     for row in reader:
#         order_id = row["order_id"]
#         product = row["product"]

#         quantity = int(row["quantity"])
#         price = float(row["price"])

#         print("Order ID:", order_id)
#         print("Product:", product)
#         print("Quantity:", quantity)
#         print("Price:", price)

#         print("Quantity Data Type:", type(quantity))
#         print("Price Data Type:", type(price))

#         print("--------------------")


# ******************** Data Transformation *****************

# import csv

# with open("sales.csv", "r", newline="") as file:
#     reader = csv.DictReader(file)

#     total_revenue = 0

#     for row in reader:
#         order_id = row["order_id"]
#         product = row["product"]

#         quantity = int(row["quantity"])
#         price = float(row["price"])

#         revenue = quantity * price

#         total_revenue = total_revenue + revenue

#         print("Order ID:", order_id)
#         print("Product:", product)
#         print("Quantity:", quantity)
#         print("Unit Price: $", format(price, ".2f"))
#         print("Revenue: $", format(revenue, ".2f"))
#         print("--------------------")

#     print("TOTAL SALES REVENUE: $", format(total_revenue, ".2f"))


# ************************** Try & Catch  ***************************

import csv

total_revenue = 0
valid_records = 0
invalid_records = 0

with open("sales.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        order_id = row["order_id"]
        product = row["product"]

        # Check required fields
        if not order_id or not product:
            print("Rejected: Missing order ID or product")
            invalid_records += 1
            continue

        # Convert numeric values safely
        try:
            quantity = int(row["quantity"])
            price = float(row["price"])

        except (ValueError, TypeError):
            print("Rejected Order:", order_id)
            print("Reason: Invalid quantity or price")
            invalid_records += 1
            continue

        # Check business rules
        if quantity <= 0 or price < 0:
            print("Rejected Order:", order_id)
            print("Reason: Quantity or price violates business rules")
            invalid_records += 1
            continue

        # Process valid transaction
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

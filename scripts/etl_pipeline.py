import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("ETL pipeline started successfully")

# ---------------- SETUP ----------------
os.makedirs("visuals", exist_ok=True)

# ---------------- PHASE 2: DISCOVERY ----------------

# Load datasets
orders = pd.read_csv("archive/olist_orders_dataset.csv")
order_items = pd.read_csv("archive/olist_order_items_dataset.csv")
products = pd.read_csv("archive/olist_products_dataset.csv")
customers = pd.read_csv("archive/olist_customers_dataset.csv")
reviews = pd.read_csv("archive/olist_order_reviews_dataset.csv")

print("\nDatasets loaded successfully.")
print("Orders shape:", orders.shape)
print("Order Items shape:", order_items.shape)
print("Products shape:", products.shape)
print("Customers shape:", customers.shape)
print("Reviews shape:", reviews.shape)

print("\nMissing values in orders:")
print(orders.isnull().sum())

# ---------------- PHASE 2: DATA CLEANING ----------------

# Convert date columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

print("\nDate conversion done:")
print(orders[date_columns].dtypes)

# Check invalid prices
print("\nNumber of invalid prices (<= 0):")
print((order_items["price"] <= 0).sum())

# Keep only valid prices
order_items = order_items[order_items["price"] > 0]

# Keep zip code as string
customers["customer_zip_code_prefix"] = customers["customer_zip_code_prefix"].astype(str)

print("\nDuplicate order_id in orders:")
print(orders["order_id"].duplicated().sum())

print("\nFull duplicate rows in order_items:")
print(order_items.duplicated().sum())

# Remove full duplicate rows if any
order_items = order_items.drop_duplicates()

# Key integrity checks
print("\nMissing product_id in products:")
print(products["product_id"].isnull().sum())

print("\nMissing customer_id in customers:")
print(customers["customer_id"].isnull().sum())

print("\nMissing product_id in order_items:")
print(order_items["product_id"].isnull().sum())

print("\nMissing customer_id in orders:")
print(orders["customer_id"].isnull().sum())

missing_products = ~order_items["product_id"].isin(products["product_id"])
print("\nOrder items with product_id not found in products:")
print(missing_products.sum())

missing_customers = ~orders["customer_id"].isin(customers["customer_id"])
print("\nOrders with customer_id not found in customers:")
print(missing_customers.sum())

# ---------------- PHASE 2: FEATURE ENGINEERING ----------------

# Create purchase month
orders["purchase_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

# Delivery gap = actual - estimated
orders["delivery_gap_days"] = (
    orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
).dt.days

print("\nDelivery gap column created successfully.")

# ---------------- PHASE 2: VISUAL EDA ----------------

# 1. Monthly Sales Revenue
sales_df = orders.merge(order_items, on="order_id", how="inner")

monthly_revenue = (
    sales_df.groupby("purchase_month")["price"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(12, 6))
monthly_revenue.plot(kind="line", marker="o")
plt.title("Monthly Sales Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visuals/monthly_sales_revenue.png")
plt.show()

# 2. Delivery Gap Histogram
delivery_gap = orders["delivery_gap_days"].dropna()

plt.figure(figsize=(10, 6))
plt.hist(delivery_gap, bins=30, edgecolor="black")
plt.title("Delivery Gap Distribution")
plt.xlabel("Delivery Gap (days)")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("visuals/delivery_gap_histogram.png")
plt.show()

# 3. Top 10 Product Categories by Order Volume
category_df = order_items.merge(products, on="product_id", how="left")

top_categories = (
    category_df["product_category_name"]
    .fillna("unknown")
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
top_categories.plot(kind="barh")
plt.title("Top 10 Product Categories by Order Volume")
plt.xlabel("Order Volume")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig("visuals/top_10_categories.png")
plt.show()

# 4. Review Score Distribution
review_counts = reviews["review_score"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
review_counts.plot(kind="bar")
plt.title("Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("visuals/review_score_distribution.png")
plt.show()

print("\nPhase 2 completed successfully.")
print("Charts saved in the visuals folder.")
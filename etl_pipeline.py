import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PHASE 2: DISCOVERY ----------------

print("ETL pipeline started successfully")

# Load orders dataset
df = pd.read_csv("archive/olist_orders_dataset.csv")

print("\nDataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

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
    df[col] = pd.to_datetime(df[col], errors="coerce")

print("\nDate conversion done:")
print(df[date_columns].dtypes)
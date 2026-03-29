# Phase 1 & 2 Guide: Setup, Cleaning, and Visual EDA

## Phase 1: Environment & Discovery

**Goal:** Prepare your workspace and understand the "raw" state of your data.

**Step 1:** Data Acquisition
 1. Download the Olist E-Commerce Dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

 2. Create a project folder: `advanced_data_pipeline`

 3. Unzip the files into your project folder (or upload them to Google Drive if using Colab).

**Option A: Local Environment (Recommended for Portfolio)**

 - **Tools:** Python VS Code, MySQL Workbench.

 - **Setup:**
   1. **In MySQL Workbench:** Create a database named `olist_intelligence`. We're going to use this database later.

   2. Open your project in VSCode

   3. Create or activate venv. Then installed dependencies: `pip install pandas sqlalchemy pymysql matplotlib`.

**Option B: Google Colab (Recommended for Quick Start)**
 - **Tools:** Web Browser, Google Drive.

 - **Setup:**
   1. **Upload Olist CSVs** to a folder in Google Drive.
   2. **Install libraries:** `!pip install pymysql sqlalchemy`.
   3. **Mount Drive** in your notebook:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    ```
    **Help:** 
     - https://colab.research.google.com/drive/1YppUP29n7S7w5rZahQeOCE2WVvTCdqys#scrollTo=zjlHdA7LgUcg

     - https://docs.google.com/document/d/19VflEPy47IhdsV_fymFTwWmMMjNXPdjE4t7FES-RkZw/edit?tab=t.0
   

## Phase 2: Data Cleaning & Visual EDA

### You will primarily work with the `orders`, `order_items`, `products`, and `customers` datasets.

**Goal:** Use Python to "fix" the data and Matplotlib to find hidden stories.

**Step 1:** The "Data Surgery" (Python/Pandas)
Before moving to SQL, you must standardize the Olist files.

 - **Date Conversion:** The Olist dataset has many timestamp columns. Convert them using pd.to_datetime().
   - **The Time Fix:** Convert columns like order_purchase_timestamp and order_delivered_customer_date into proper datetime objects.

 - **Handling Nulls:** Decide if a missing delivery_date means the order was canceled or is still in transit.
   - **Hint** Null Logic: Identify orders that have no delivery date. Are they canceled, or just late? 

 - **Deduplication:** Ensure `order_id` is unique in your items table.

 - **Key Integrity:** Ensure that the `product_id` and `customer_id` columns are clean and consistent across all tables.

**Step 2:** Exploratory Data Analysis (Matplotlib)
Before you build a dashboard, you must "feel" the data. Create these three plots to validate your cleaning:

1. **Revenue Seasonality (Line Plot):** Group sales by month.

    - Look for: Spikes during "Black Friday" (November) in Brazil.
    - Look for: Does Olist experience a massive spike during Black Friday (November)?

2. **Delivery Accuracy (Histogram):** Calculate the difference between `delivered_date` and `estimated_delivery_date`.

    - Look for: Is the distribution "Left Skewed" (mostly early) or "Right Skewed" (mostly late)?
    - Look for: Are most packages arriving earlier or later than promised?

3. **Category Popularity (Horizontal Bar Chart):** Plot the top 10 product categories by order volume.

### More Charts ideas!

Create these three essential charts to include in your final report:

 - **Sales Velocity:** A Line Plot showing total sales revenue per month. Are there spikes in November (Black Friday)?

 - **Logistics Health:** A Histogram of the "Delivery Gap" (Actual Delivery Date - Estimated Delivery Date). Are most packages early or late?

 - **Customer Satisfaction:** A Bar Chart of review scores by product category. Which categories struggle with low ratings?
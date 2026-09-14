import pandas as pd

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/online_retail_II.csv")

print("Original dataset shape:", df.shape)


# ==========================================
# 2. DATA CLEANING
# ==========================================

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove missing Customer IDs
df = df.dropna(subset=["Customer ID"])

# Remove cancelled invoices
df = df[~df["Invoice"].str.startswith("C")]

# Keep only positive quantities
df = df[df["Quantity"] > 0]

# Keep only positive prices
df = df[df["Price"] > 0]

# Remove duplicate transactions
df = df.drop_duplicates()

print("\nCleaned dataset shape:", df.shape)


# ==========================================
# 3. CREATE MONTH COLUMN
# ==========================================

df["PurchaseMonth"] = df["InvoiceDate"].dt.to_period("M")


# ==========================================
# 4. FIND FIRST PURCHASE MONTH
# ==========================================

df["CohortMonth"] = df.groupby("Customer ID")["PurchaseMonth"].transform("min")


# ==========================================
# 5. DISPLAY COHORT INFORMATION
# ==========================================

print("\nSample Cohort Data:")
print(
    df[
        [
            "Customer ID",
            "PurchaseMonth",
            "CohortMonth"
        ]
    ].head(20)
)


# ==========================================
# 6. NUMBER OF UNIQUE CUSTOMERS
# ==========================================

unique_customers = df["Customer ID"].nunique()

print("\nUnique Customers:", unique_customers)

print("\nNumber of Cohorts:", df["CohortMonth"].nunique())


# ==========================================
# 7. CALCULATE COHORT INDEX
# ==========================================

df["CohortIndex"] = (
    (df["PurchaseMonth"].dt.year - df["CohortMonth"].dt.year) * 12
    + (df["PurchaseMonth"].dt.month - df["CohortMonth"].dt.month)
)

print("\nSample Cohort Index:")
print(
    df[
        [
            "Customer ID",
            "PurchaseMonth",
            "CohortMonth",
            "CohortIndex"
        ]
    ].head(20)
)

print("\nCohort Index Range:")
print(df["CohortIndex"].min(), "to", df["CohortIndex"].max())

# ==========================================
# 8. CREATE COHORT RETENTION TABLE
# ==========================================

# Count unique customers for each cohort and cohort index
cohort_data = (
    df.groupby(["CohortMonth", "CohortIndex"])["Customer ID"]
    .nunique()
    .reset_index()
)

# Create retention matrix
cohort_table = cohort_data.pivot(
    index="CohortMonth",
    columns="CohortIndex",
    values="Customer ID"
)

print("\nCohort Retention Table:")
print(cohort_table)


# ==========================================
# 9. CALCULATE RETENTION PERCENTAGE
# ==========================================

# Divide each cohort's customer count
# by the number of customers in Cohort Index 0
retention_table = cohort_table.divide(
    cohort_table.iloc[:, 0],
    axis=0
) * 100

# Round percentages to 2 decimal places
retention_table = retention_table.round(2)

print("\nCohort Retention Percentage:")
print(retention_table)

# ==========================================
# 10. CREATE COHORT RETENTION HEATMAP
# ==========================================

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(16, 10))

sns.heatmap(
    retention_table,
    annot=True,
    fmt=".1f",
    cmap="Blues",
    vmin=0,
    vmax=100
)

plt.title("Cohort Retention Analysis", fontsize=18)
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")

plt.tight_layout()

# Save heatmap
plt.savefig("reports/cohort_retention_heatmap.png", dpi=300)

plt.show()

# ==========================================
# 11. KEY RETENTION INSIGHTS
# ==========================================

# Month 1 retention
month_1_retention = retention_table[1].mean()

# Month 3 retention
month_3_retention = retention_table[3].mean()

# Month 6 retention
month_6_retention = retention_table[6].mean()

# Month 12 retention
month_12_retention = retention_table[12].mean()

print("\n==========================================")
print("KEY RETENTION INSIGHTS")
print("==========================================")

print(f"Average Month 1 Retention: {month_1_retention:.2f}%")
print(f"Average Month 3 Retention: {month_3_retention:.2f}%")
print(f"Average Month 6 Retention: {month_6_retention:.2f}%")
print(f"Average Month 12 Retention: {month_12_retention:.2f}%")

# ==========================================
# 12. BEST PERFORMING COHORT
# ==========================================

# Consider only cohorts that have data for
# all first 6 months (Index 0 to 5)
six_month_data = retention_table.iloc[:, :6]

# Keep only cohorts with all 6 months available
valid_cohorts = six_month_data.dropna()

# Calculate average retention for valid cohorts
cohort_average_retention = valid_cohorts.mean(axis=1)

# Find the best performing cohort
best_cohort = cohort_average_retention.idxmax()
best_retention = cohort_average_retention.max()

print("\n==========================================")
print("BEST PERFORMING COHORT")
print("==========================================")

print(f"Best Cohort: {best_cohort}")
print(f"Average Retention (First 6 Months): {best_retention:.2f}%")

 # ==========================================
# 13. EXPORT CLEANED DATA FOR SQL
# ==========================================

# Export only the original columns required by SQL
sql_columns = [
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country"
]

df[sql_columns].to_csv(
    "data/online_retail_cleaned.csv",
    index=False
)

print("\nCleaned dataset exported successfully!")
print("File: data/online_retail_cleaned.csv")
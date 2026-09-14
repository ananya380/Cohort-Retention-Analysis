# Cohort Retention Analysis

## Project Overview
This project analyzes customer retention using cohort analysis on the Online Retail II dataset. The objective is to understand how customer purchasing behavior changes over time and identify cohorts with the strongest retention.

## Objectives
- Clean and prepare retail transaction data
- Identify each customer's first purchase month
- Group customers into monthly cohorts
- Calculate customer retention over time
- Create a cohort retention matrix
- Visualize retention using a heatmap
- Identify the best-performing customer cohort
- Perform supporting SQL analysis

## Dataset
**Dataset:** Online Retail II

- Original records: **1,067,371**
- Cleaned records: **779,425**
- Unique customers: **5,878**
- Number of cohorts: **25**

## Data Cleaning
1. Converted `InvoiceDate` to datetime.
2. Removed transactions without Customer IDs.
3. Removed cancelled invoices.
4. Kept only positive quantities.
5. Kept only positive prices.
6. Removed duplicate transactions.

## Cohort Analysis
Each customer was assigned to the month of their first purchase. A cohort index measures the number of months since that first purchase.

**Retention Rate = (Customers active in a month / Customers in the cohort at Month 0) × 100**

## Key Results

| Metric | Result |
|---|---:|
| Original Records | 1,067,371 |
| Cleaned Records | 779,425 |
| Unique Customers | 5,878 |
| Number of Cohorts | 25 |
| Average Month 1 Retention | 21.17% |
| Average Month 3 Retention | 21.62% |
| Average Month 6 Retention | 17.82% |
| Average Month 12 Retention | 18.24% |
| Best Cohort | December 2009 |
| Best 6-Month Average Retention | 47.52% |

## Key Insights
- Month 1 retention is approximately 21.17%, indicating substantial early customer drop-off.
- Retention generally decreases as time since first purchase increases.
- The December 2009 cohort performed best across the first six months, with 47.52% average retention.
- Recent cohorts have fewer observable months and should not be compared directly with older cohorts for long-term retention.

## Visualization
The Python analysis creates a cohort retention heatmap at:
`reports/cohort_retention_heatmap.png`

## Tools & Technologies
Python, Pandas, Matplotlib, Seaborn, MySQL, MySQL Workbench, VS Code.

## Project Structure
```text
Cohort_Retention
├── data
│   ├── online_retail_II.csv
│   └── online_retail_cleaned.csv
├── python
│   └── cohort_retention.py
├── sql
│   └── cohort_analysis.sql
├── reports
│   └── cohort_retention_heatmap.png
└── README.md
```

## Business Recommendations
- Improve post-purchase onboarding and follow-up.
- Use personalized offers to encourage second purchases.
- Run reactivation campaigns for inactive customers.
- Study successful early cohorts to identify retention drivers.
- Introduce loyalty programs for repeat customers.
- Track cohort retention regularly as a customer-health KPI.

## Author
**Ananya Garg**  
B.Tech CSE-IoT | Data Analytics Enthusiast  
Skills: Excel, SQL, Power BI, Python, Data Cleaning, Data Visualization

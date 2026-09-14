CREATE DATABASE cohort_retention;
USE cohort_retention;
CREATE TABLE online_retail (
    Invoice VARCHAR(20),
    StockCode VARCHAR(20),
    Description VARCHAR(255),
    Quantity INT,
    InvoiceDate DATETIME,
    Price DECIMAL(10,2),
    CustomerID DECIMAL(10,1),
    Country VARCHAR(100)
);
USE cohort_retention;

-- ==========================================
-- 1. TOTAL UNIQUE CUSTOMERS
-- ==========================================

SELECT COUNT(DISTINCT CustomerID) AS total_customers
FROM online_retail;


-- ==========================================
-- 2. MONTHLY ACTIVE CUSTOMERS
-- ==========================================

SELECT
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS purchase_month,
    COUNT(DISTINCT CustomerID) AS active_customers
FROM online_retail
GROUP BY DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY purchase_month;


-- ==========================================
-- 3. FIRST PURCHASE MONTH
-- ==========================================

CREATE TEMPORARY TABLE customer_cohorts AS
SELECT
    CustomerID,
    DATE_FORMAT(MIN(InvoiceDate), '%Y-%m') AS cohort_month
FROM online_retail
GROUP BY CustomerID;


-- ==========================================
-- 4. CUSTOMER COHORT DATA
-- ==========================================

SELECT
    o.CustomerID,
    c.cohort_month,
    DATE_FORMAT(o.InvoiceDate, '%Y-%m') AS purchase_month
FROM online_retail o
JOIN customer_cohorts c
    ON o.CustomerID = c.CustomerID
LIMIT 20;


-- ==========================================
-- 5. COHORT CUSTOMER COUNT
-- ==========================================

SELECT
    c.cohort_month,
    DATE_FORMAT(o.InvoiceDate, '%Y-%m') AS purchase_month,
    COUNT(DISTINCT o.CustomerID) AS customers
FROM online_retail o
JOIN customer_cohorts c
    ON o.CustomerID = c.CustomerID
GROUP BY
    c.cohort_month,
    DATE_FORMAT(o.InvoiceDate, '%Y-%m')
ORDER BY
    c.cohort_month,
    purchase_month;


-- ==========================================
-- 6. COHORT RETENTION ANALYSIS
-- ==========================================

SELECT
    c.cohort_month,
    COUNT(DISTINCT o.CustomerID) AS retained_customers
FROM online_retail o
JOIN customer_cohorts c
    ON o.CustomerID = c.CustomerID
GROUP BY c.cohort_month
ORDER BY c.cohort_month;

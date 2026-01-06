-- Database: fleximart_dw
USE fleximart_dw;

-- =========================================================
-- Query 1: Monthly Sales Drill-Down Analysis
-- Business Scenario: "The CEO wants to see sales performance broken down by time periods.
-- Start with yearly total, then quarterly, then monthly sales for 2024."
-- Demonstrates: Drill-down from Year -> Quarter -> Month
--
-- Output:
-- year | quarter | month_name | total_sales | total_quantity
-- =========================================================

SELECT
    d.year AS year,
    d.quarter AS quarter,
    d.month_name AS month_name,
    ROUND(SUM(fs.total_amount), 2) AS total_sales,
    SUM(fs.quantity_sold) AS total_quantity
FROM fact_sales fs
JOIN dim_date d
    ON fs.date_key = d.date_key
WHERE d.year = 2024
GROUP BY
    d.year, d.quarter, d.month, d.month_name
ORDER BY
    d.year,
    CASE d.quarter
        WHEN 'Q1' THEN 1
        WHEN 'Q2' THEN 2
        WHEN 'Q3' THEN 3
        WHEN 'Q4' THEN 4
        ELSE 5
    END,
    d.month;

-- =========================================================
-- Query 2: Product Performance Analysis
-- Business Scenario: "Show the top 10 products by revenue, along with their category,
-- total units sold, and revenue contribution percentage."
-- Includes: Revenue percentage calculation
--
-- Output:
-- product_name | category | units_sold | revenue | revenue_percentage
-- =========================================================

SELECT
    p.product_name,
    p.category,
    SUM(fs.quantity_sold) AS units_sold,
    ROUND(SUM(fs.total_amount), 2) AS revenue,
    ROUND(
        (SUM(fs.total_amount) / (SELECT SUM(total_amount) FROM fact_sales)) * 100,
        2
    ) AS revenue_percentage
FROM fact_sales fs
JOIN dim_product p
    ON fs.product_key = p.product_key
GROUP BY
    p.product_key, p.product_name, p.category
ORDER BY
    revenue DESC
LIMIT 10;

-- =========================================================
-- Query 3: Customer Segmentation Analysis
-- Business Scenario: "Segment customers into High/Medium/Low value based on total spend.
-- Show count of customers and total revenue in each segment."
-- Segments:
--   High Value   : > 50000
--   Medium Value : 20000 - 50000
--   Low Value    : < 20000
--
-- Output:
-- customer_segment | customer_count | total_revenue | avg_revenue_per_customer
-- =========================================================

WITH customer_spend AS (
    SELECT
        c.customer_key,
        c.customer_name,
        SUM(fs.total_amount) AS total_spent
    FROM fact_sales fs
    JOIN dim_customer c
        ON fs.customer_key = c.customer_key
    GROUP BY
        c.customer_key, c.customer_name
),
segmented AS (
    SELECT
        CASE
            WHEN total_spent > 50000 THEN 'High Value'
            WHEN total_spent BETWEEN 20000 AND 50000 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS customer_segment,
        total_spent
    FROM customer_spend
)
SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(SUM(total_spent), 2) AS total_revenue,
    ROUND(AVG(total_spent), 2) AS avg_revenue_per_customer
FROM segmented
GROUP BY customer_segment
ORDER BY
    CASE customer_segment
        WHEN 'High Value' THEN 1
        WHEN 'Medium Value' THEN 2
        WHEN 'Low Value' THEN 3
        ELSE 4
    END;

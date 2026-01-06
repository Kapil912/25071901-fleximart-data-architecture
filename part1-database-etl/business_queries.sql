-- =========================================
-- business_queries.sql
-- Database: fleximart
-- =========================================

USE fleximart;

-- -----------------------------------------
-- Query 1: Customer Purchase History
-- Business Question:
-- "Generate a detailed report showing each customer's name, email,
--  total number of orders placed, and total amount spent.
--  Include only customers who have placed at least 2 orders and spent
--  more than ₹5,000. Order by total amount spent in descending order."
-- Expected Output Columns:
-- customer_name | email | total_orders | total_spent
-- Requirements:
-- - Must join: customers, orders, order_items
-- - Use GROUP BY with HAVING
-- - COUNT orders, SUM spending
-- Expected to return customers with 2+ orders and >5000 spent
-- -----------------------------------------

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email AS email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.subtotal) AS total_spent
FROM customers c
JOIN orders o
    ON o.customer_id = c.customer_id
JOIN order_items oi
    ON oi.order_id = o.order_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email
HAVING
    COUNT(DISTINCT o.order_id) >= 2
    AND SUM(oi.subtotal) > 5000
ORDER BY
    total_spent DESC;


-- -----------------------------------------
-- Query 2: Product Sales Analysis
-- Business Question:
-- "For each product category, show the category name,
--  number of different products sold, total quantity sold,
--  and total revenue generated.
--  Only include categories that have generated more than ₹10,000 in revenue.
--  Order by total revenue descending."
-- Expected Output Columns:
-- category | num_products | total_quantity_sold | total_revenue
-- Requirements:
-- - Must join: products, order_items
-- - Use GROUP BY with HAVING
-- - COUNT(DISTINCT), SUM aggregates
-- Expected to return categories with >10000 revenue
-- -----------------------------------------

SELECT
    p.category AS category,
    COUNT(DISTINCT p.product_id) AS num_products,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.subtotal) AS total_revenue
FROM products p
JOIN order_items oi
    ON oi.product_id = p.product_id
GROUP BY
    p.category
HAVING
    SUM(oi.subtotal) > 10000
ORDER BY
    total_revenue DESC;


-- -----------------------------------------
-- Query 3: Monthly Sales Trend (Year 2024)
-- Business Question:
-- "Show monthly sales trends for the year 2024. For each month,
--  display the month name, total number of orders, total revenue,
--  and the running total of revenue (cumulative revenue from January to that month)."
-- Expected Output Columns:
-- month_name | total_orders | monthly_revenue | cumulative_revenue
-- Requirements:
-- - Use window function (SUM() OVER) for running total OR subquery
-- - Extract month from order_date
-- - Group by month
-- - Order chronologically
-- Hint: DATE_FORMAT() / MONTHNAME()
-- Expected to show monthly and cumulative revenue for 2024 only
-- -----------------------------------------

WITH monthly AS (
    SELECT
        MONTH(o.order_date) AS month_num,
        MONTHNAME(o.order_date) AS month_name,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.subtotal) AS monthly_revenue
    FROM orders o
    JOIN order_items oi
        ON oi.order_id = o.order_id
    WHERE
        o.order_date >= '2024-01-01'
        AND o.order_date < '2025-01-01'
    GROUP BY
        MONTH(o.order_date),
        MONTHNAME(o.order_date)
)
SELECT
    month_name,
    total_orders,
    monthly_revenue,
    SUM(monthly_revenue) OVER (ORDER BY month_num) AS cumulative_revenue
FROM monthly
ORDER BY
    month_num;

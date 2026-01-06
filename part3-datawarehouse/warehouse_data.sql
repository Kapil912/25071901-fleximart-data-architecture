-- =========================================
-- warehouse_data.sql
-- Database: fleximart_dw
-- Loads:
--   - dim_date: 30 rows
--   - dim_product: 15 rows
--   - dim_customer: 12 rows
--   - fact_sales: 40 rows
-- =========================================

USE fleximart_dw;

SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------
-- 1) dim_date (30 dates: Jan 1–20 + Feb 1–10)
-- -----------------------------------------
INSERT INTO dim_date
(date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend)
VALUES
(20240101,'2024-01-01','Monday',1,1,'January','Q1',2024,0),
(20240102,'2024-01-02','Tuesday',2,1,'January','Q1',2024,0),
(20240103,'2024-01-03','Wednesday',3,1,'January','Q1',2024,0),
(20240104,'2024-01-04','Thursday',4,1,'January','Q1',2024,0),
(20240105,'2024-01-05','Friday',5,1,'January','Q1',2024,0),
(20240106,'2024-01-06','Saturday',6,1,'January','Q1',2024,1),
(20240107,'2024-01-07','Sunday',7,1,'January','Q1',2024,1),
(20240108,'2024-01-08','Monday',8,1,'January','Q1',2024,0),
(20240109,'2024-01-09','Tuesday',9,1,'January','Q1',2024,0),
(20240110,'2024-01-10','Wednesday',10,1,'January','Q1',2024,0),
(20240111,'2024-01-11','Thursday',11,1,'January','Q1',2024,0),
(20240112,'2024-01-12','Friday',12,1,'January','Q1',2024,0),
(20240113,'2024-01-13','Saturday',13,1,'January','Q1',2024,1),
(20240114,'2024-01-14','Sunday',14,1,'January','Q1',2024,1),
(20240115,'2024-01-15','Monday',15,1,'January','Q1',2024,0),
(20240116,'2024-01-16','Tuesday',16,1,'January','Q1',2024,0),
(20240117,'2024-01-17','Wednesday',17,1,'January','Q1',2024,0),
(20240118,'2024-01-18','Thursday',18,1,'January','Q1',2024,0),
(20240119,'2024-01-19','Friday',19,1,'January','Q1',2024,0),
(20240120,'2024-01-20','Saturday',20,1,'January','Q1',2024,1),

(20240201,'2024-02-01','Thursday',1,2,'February','Q1',2024,0),
(20240202,'2024-02-02','Friday',2,2,'February','Q1',2024,0),
(20240203,'2024-02-03','Saturday',3,2,'February','Q1',2024,1),
(20240204,'2024-02-04','Sunday',4,2,'February','Q1',2024,1),
(20240205,'2024-02-05','Monday',5,2,'February','Q1',2024,0),
(20240206,'2024-02-06','Tuesday',6,2,'February','Q1',2024,0),
(20240207,'2024-02-07','Wednesday',7,2,'February','Q1',2024,0),
(20240208,'2024-02-08','Thursday',8,2,'February','Q1',2024,0),
(20240209,'2024-02-09','Friday',9,2,'February','Q1',2024,0),
(20240210,'2024-02-10','Saturday',10,2,'February','Q1',2024,1);

-- -----------------------------------------
-- 2) dim_product (15 products, 3 categories)
-- IMPORTANT: inserted in a fixed order => product_key becomes 1..15
-- -----------------------------------------
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('P001','iPhone 14','Electronics','Mobile',79999),
('P002','Samsung TV 55','Electronics','Television',65999),
('P003','Dell Laptop','Electronics','Laptop',89999),
('P004','Bluetooth Speaker','Electronics','Audio',4999),
('P005','Headphones','Electronics','Audio',2999),

('P006','Nike Shoes','Fashion','Footwear',5999),
('P007','Adidas Jacket','Fashion','Clothing',7999),
('P008','Levis Jeans','Fashion','Clothing',3999),
('P009','Puma T-Shirt','Fashion','Clothing',1999),
('P010','Reebok Shorts','Fashion','Clothing',2499),

('P011','Office Chair','Furniture','Seating',12999),
('P012','Dining Table','Furniture','Table',45999),
('P013','Bookshelf','Furniture','Storage',8999),
('P014','Sofa','Furniture','Seating',99999),
('P015','Bed Frame','Furniture','Bedroom',55999);

-- -----------------------------------------
-- 3) dim_customer (12 customers, 4+ cities)
-- IMPORTANT: inserted in a fixed order => customer_key becomes 1..12
-- -----------------------------------------
INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001','Rahul Sharma','Mumbai','Maharashtra','Retail'),
('C002','Priya Patel','Ahmedabad','Gujarat','Retail'),
('C003','Amit Verma','Delhi','Delhi','Corporate'),
('C004','Sneha Reddy','Hyderabad','Telangana','Retail'),
('C005','Karan Mehta','Mumbai','Maharashtra','Corporate'),
('C006','Anjali Singh','Delhi','Delhi','Retail'),
('C007','Rohit Iyer','Bengaluru','Karnataka','Corporate'),
('C008','Neha Jain','Ahmedabad','Gujarat','Retail'),
('C009','Vikram Rao','Hyderabad','Telangana','Retail'),
('C010','Pooja Nair','Bengaluru','Karnataka','Corporate'),
('C011','Arjun Malhotra','Delhi','Delhi','Retail'),
('C012','Meera Das','Mumbai','Maharashtra','Corporate');

-- -----------------------------------------
-- 4) fact_sales (EXACTLY 40 transactions)
-- Notes:
-- - date_key values exist in dim_date
-- - total_amount = (quantity_sold * unit_price) - discount_amount
-- -----------------------------------------
INSERT INTO fact_sales
(date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount)
VALUES
(20240106, 1,  1, 2, 79999, 2000, 157998),
(20240106, 2,  2, 1, 65999,    0,  65999),
(20240107, 3,  3, 1, 89999, 5000,  84999),
(20240107, 6,  4, 3,  5999,    0,  17997),
(20240113, 14, 5, 1, 99999,10000,  89999),
(20240114, 15, 6, 1, 55999, 3000,  52999),
(20240120, 2,  7, 1, 65999, 2000,  63999),
(20240120, 3,  8, 1, 89999, 5000,  84999),
(20240120, 7,  5, 1,  7999,  500,   7499),
(20240120, 13, 8, 2,  8999,    0,  17998),
(20240101, 4,  9, 5,  4999,    0,  24995),
(20240102, 10,10, 2,  2499,    0,   4998),
(20240103, 11,11, 1, 12999,    0,  12999),
(20240104, 8, 12, 3,  3999,    0,  11997),
(20240105, 5,  7, 2,  2999,    0,   5998),
(20240108, 8,  7, 2,  3999,    0,   7998),
(20240109, 10, 8, 1,  2499,    0,   2499),
(20240110, 11, 9, 1, 12999, 1000,  11999),
(20240111, 12,10, 1, 45999, 3000,  42999),
(20240112, 13,11, 2,  8999,    0,  17998),
(20240115, 1, 12, 1, 79999,    0,  79999),
(20240116, 6,  1, 2,  5999,    0,  11998),
(20240117, 4,  2, 3,  4999,    0,  14997),
(20240118, 5,  3, 2,  2999,    0,   5998),
(20240119, 9,  4, 4,  1999,    0,   7996),
(20240201, 4,  1, 2,  4999,    0,   9998),
(20240201, 12, 2, 1, 45999, 3000,  42999),
(20240202, 11, 3, 1, 12999,    0,  12999),
(20240202, 10, 4, 3,  2499,    0,   7497),
(20240202, 5,  5, 4,  2999,    0,  11996),
(20240203, 1,  6, 1, 79999,    0,  79999),
(20240203, 6,  2, 2,  5999,    0,  11998),
(20240203, 14, 3, 1, 99999,10000,  89999),
(20240204, 7,  5, 2,  7999,    0,  15998),
(20240204, 9,  6, 4,  1999,    0,   7996),
(20240204, 12, 4, 1, 45999, 3000,  42999),
(20240205, 13, 8, 1,  8999,    0,   8999),
(20240206, 2,  9, 1, 65999, 2000,  63999),
(20240207, 15,11, 1, 55999, 3000,  52999),
(20240208, 8,  1, 2,  3999,    0,   7998),
(20240209, 4,  4, 3,  4999,    0,  14997),
(20240209, 3, 12, 1, 89999, 5000,  84999),
(20240210, 6,  5, 2,  5999,    0,  11998),
(20240210, 1,  6, 1, 79999, 3000,  76999),
(20240210, 12, 8, 1, 45999,    0,  45999);

-- Test row counts
SELECT COUNT(*) AS dim_date_rows FROM dim_date;
SELECT COUNT(*) AS dim_product_rows FROM dim_product;
SELECT COUNT(*) AS dim_customer_rows FROM dim_customer;
SELECT COUNT(*) AS fact_sales_rows FROM fact_sales;

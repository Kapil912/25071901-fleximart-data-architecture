# FlexiMart Database Schema Documentation

---

## 1. Entity–Relationship Description

The FlexiMart operational database is designed to support an e-commerce platform and consists of four core entities: **customers**, **products**, **orders**, and **order_items**.  

The **customers** table stores personal and contact information for each customer. The **products** table maintains catalog-level information such as product name, category, price, and available stock. The **orders** table captures order-level transactional information, including which customer placed the order, the order date, total amount, and current status. The **order_items** table stores line-level details for each order, specifying which products were purchased, in what quantity, at what unit price, and the calculated subtotal.

Relationships in the schema are as follows:
- One **customer** can place **many orders** (1:M relationship between customers and orders).
- One **order** can contain **many order items** (1:M relationship between orders and order_items).
- One **product** can appear in **many order items** (1:M relationship between products and order_items).
- The many-to-many relationship between orders and products is resolved through the **order_items** table.

---

## 2. ENTITY: customers

**Purpose:**  
Stores customer information and contact details.

**Attributes:**
- **customer_id**: Unique identifier for a customer (Primary Key, auto-increment)
- **first_name**: Customer’s first name
- **last_name**: Customer’s last name
- **email**: Customer’s email address (unique, not null)
- **phone**: Customer’s phone number (standardized format)
- **city**: City of residence
- **registration_date**: Date the customer registered on the platform

**Relationships:**
- One customer can place **MANY** orders (1:M relationship with the `orders` table)

---

## 3. ENTITY: products

**Purpose:**  
Stores product catalog and inventory information.

**Attributes:**
- **product_id**: Unique identifier for a product (Primary Key, auto-increment)
- **product_name**: Name of the product
- **category**: Product category (standardized)
- **price**: Price of the product
- **stock_quantity**: Available stock quantity

**Relationships:**
- One product can appear in **MANY** order items (1:M relationship with `order_items`)

---

## 4. ENTITY: orders

**Purpose:**  
Stores order-level transaction details.

**Attributes:**
- **order_id**: Unique identifier for an order (Primary Key, auto-increment)
- **customer_id**: Identifier of the customer who placed the order (Foreign Key → customers.customer_id)
- **order_date**: Date when the order was placed
- **total_amount**: Total monetary value of the order
- **status**: Current order status (e.g., Pending, Completed)

**Relationships:**
- Many orders belong to **ONE** customer (M:1 relationship with customers)
- One order can have **MANY** order items (1:M relationship with order_items)

---

## 5. ENTITY: order_items

**Purpose:**  
Stores detailed line items for each order.

**Attributes:**
- **order_item_id**: Unique identifier for an order item (Primary Key, auto-increment)
- **order_id**: Identifier of the associated order (Foreign Key → orders.order_id)
- **product_id**: Identifier of the purchased product (Foreign Key → products.product_id)
- **quantity**: Quantity of the product purchased
- **unit_price**: Price per unit at the time of purchase
- **subtotal**: Line total calculated as quantity × unit_price

**Relationships:**
- Many order items belong to **ONE** order (M:1 relationship with orders)
- Many order items reference **ONE** product (M:1 relationship with products)

---

## 6. Normalization Explanation (Third Normal Form)

The FlexiMart database schema is designed to satisfy Third Normal Form (3NF) by ensuring that all data is organized to minimize redundancy and maintain data integrity. Each table represents a single entity with attributes that depend only on the primary key and not on other non-key attributes.

In the customers table, the primary key customer_id uniquely determines all other attributes such as first_name, last_name, email, phone, city, and registration_date. The functional dependency is customer_id → customer attributes. No attribute depends on another non-key attribute, and customer details are stored only once, preventing duplication across orders.

In the products table, product_id determines product_name, category, price, and stock_quantity. The functional dependency product_id → product attributes ensures that product information is maintained independently of sales transactions, avoiding update anomalies when prices or stock levels change.

The orders table separates order-level information from customers and products. Here, order_id → customer_id, order_date, total_amount, status. This design prevents insert anomalies by allowing customers to exist without orders and ensures that deleting an order does not remove customer data.

The order_items table resolves the many-to-many relationship between orders and products. The functional dependency order_item_id → order_id, product_id, quantity, unit_price, subtotal ensures that each line item is stored independently without redundant product or customer data.

By separating entities and enforcing foreign key relationships, the schema avoids update, insert, and delete anomalies and fully complies with 3NF principles.

Additionally, the schema satisfies First Normal Form (1NF) by ensuring all attributes contain atomic values and no repeating groups, and Second Normal Form (2NF) by removing partial dependencies through the use of surrogate primary keys. Non-key attributes depend entirely on their respective primary keys rather than on subsets of keys. This layered normalization approach ensures consistency, scalability, and long-term maintainability of the database design.

---

## 7. Sample Data Representation (Real Data)

### customers (sample)

| customer_id | first_name | last_name | email                    | phone           | city       | registration_date |
|------------:|------------|-----------|--------------------------|-----------------|------------|-------------------|
| 1           | Rahul      | Sharma    | rahul.sharma@gmail.com   | +91-9876543210  | Bangalore  | 2023-01-15        |
| 2           | Priya      | Patel     | priya.patel@yahoo.com    | +91-9988776655  | Mumbai     | 2023-02-20        |
| 3           | Sneha      | Reddy     | sneha.reddy@gmail.com    | +91-9123456789  | Hyderabad  | 2023-04-15        |

---

### products (sample)

| product_id | product_name           | category     | price    | stock_quantity |
|-----------:|------------------------|--------------|---------:|---------------:|
| 1          | Samsung Galaxy S21     | Electronics  | 45999.00 | 150            |
| 2          | Nike Running Shoes     | Fashion      | 3499.00  | 80             |
| 3          | Levi's Jeans           | Fashion      | 2999.00  | 120            |

---

### orders (sample)

| order_id | customer_id | order_date  | total_amount | status     |
|---------:|------------:|------------:|-------------:|------------|
| 1        | 1           | 2024-01-15  | 45999.00     | Completed  |
| 2        | 2           | 2024-01-16  | 5998.00      | Completed  |
| 3        | 4           | 2024-01-20  | 1950.00      | Completed  |

---

### order_items (sample)

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
|--------------:|---------:|-----------:|---------:|-----------:|---------:|
| 1             | 1        | 1          | 1        | 45999.00   | 45999.00 |
| 2             | 2        | 3          | 2        | 2999.00    | 5998.00  |
| 3             | 3        | 8          | 3        | 650.00     | 1950.00  |

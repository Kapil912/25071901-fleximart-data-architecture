# FlexiMart Star Schema Design Documentation

---

## Section 1: Schema Overview

### FACT TABLE: fact_sales
**Grain:** One row per product per order line item  
**Business Process:** Sales transactions

**Measures (Numeric Facts):**
- **quantity_sold:** Number of units sold
- **unit_price:** Price per unit at time of sale
- **discount_amount:** Discount applied
- **total_amount:** Final amount (`quantity_sold × unit_price - discount_amount`)

**Foreign Keys:**
- **date_key → dim_date(date_key)**
- **product_key → dim_product(product_key)**
- **customer_key → dim_customer(customer_key)**

---

### DIMENSION TABLE: dim_date
**Purpose:** Date dimension for time-based analysis  
**Type:** Conformed dimension

**Attributes:**
- **date_key (PK):** Surrogate key (integer format: YYYYMMDD)
- **full_date:** Actual date
- **day_of_week:** Monday, Tuesday, etc.
- **day_of_month:** Numeric day (1–31)
- **month:** Month number (1–12)
- **month_name:** January, February, etc.
- **quarter:** Q1, Q2, Q3, Q4
- **year:** 2023, 2024, etc.
- **is_weekend:** Boolean flag (TRUE/FALSE)

---

### DIMENSION TABLE: dim_product
**Purpose:** Product dimension for category and product-level analysis  
**Type:** Descriptive dimension

**Attributes:**
- **product_key (PK):** Surrogate key (auto-increment)
- **product_id:** Natural product identifier from the source system
- **product_name:** Product name
- **category:** Product category (e.g., Electronics, Fashion, Furniture)
- **subcategory:** Product subcategory (e.g., Mobile, Footwear, Chairs)
- **unit_price:** Product unit price used for reporting in the warehouse

---

### DIMENSION TABLE: dim_customer
**Purpose:** Customer dimension for customer and geography-based analysis  
**Type:** Descriptive dimension

**Attributes:**
- **customer_key (PK):** Surrogate key (auto-increment)
- **customer_id:** Natural customer identifier from the source system
- **customer_name:** Full customer name
- **city:** Customer city
- **state:** Customer state
- **customer_segment:** Segment label (e.g., Retail, Corporate, Home Office)

---

## Section 2: Design Decisions

The fact table uses a transaction line-item grain (one row per product per order line) because it captures the most detailed level of sales activity. This granularity supports flexible analysis such as sales by product, category, customer, city, and time, while still allowing roll-ups to monthly, quarterly, or yearly summaries. If the fact table were stored only at the order level, product-level analysis (e.g., units sold per category) would either be impossible or require complex transformations outside the warehouse.

Surrogate keys are used for all dimensions instead of natural keys because they improve query performance, keep joins consistent, and decouple the warehouse from operational system key changes. Surrogate keys also simplify handling of attribute changes over time (e.g., customer segment or product categorization changes), making the warehouse more stable and maintainable.

This design supports drill-down and roll-up operations naturally: users can roll up from day to month/quarter/year using dim_date and drill down from category to subcategory to product using dim_product.

---

## Section 3: Sample Data Flow

### Source Transaction
Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000

### Becomes in Data Warehouse

**fact_sales:**
```json
{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000,
  "discount_amount": 0,
  "total_amount": 100000
}
```
**dim_date:**
```json
{
  "date_key": 20240115,
  "full_date": "2024-01-15",
  "day_of_week": "Monday",
  "day_of_month": 15,
  "month": 1,
  "month_name": "January",
  "quarter": "Q1",
  "year": 2024,
  "is_weekend": false
}

```
**dim_product:**
```json
{
  "product_key": 5,
  "product_id": "ELEC005",
  "product_name": "Laptop",
  "category": "Electronics",
  "subcategory": "Computers",
  "unit_price": 50000
}

```

**dim_customer:**
```json
{
  "customer_key": 12,
  "customer_id": "CUST012",
  "customer_name": "John Doe",
  "city": "Mumbai",
  "state": "Maharashtra",
  "customer_segment": "Retail"
}

```
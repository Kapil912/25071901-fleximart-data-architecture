# Part 3: Data Warehouse and OLAP Analytics

## Overview

This part focuses on building a dimensional data warehouse for FlexiMart to analyze historical sales trends. A star schema is implemented, populated with realistic data, and queried using OLAP-style analytical SQL queries to support business decision-making.

---

## Objectives

- Design a star schema using fact and dimension tables
- Populate the data warehouse with clean, consistent data
- Enable drill-down, roll-up, and segmentation analysis
- Write analytical SQL queries for executive reporting

---

## Files in This Folder

- **star_schema_design.md**  
  Documentation describing the star schema, design decisions, granularity, surrogate keys, and sample data flow.

- **warehouse_schema.sql**  
  SQL script to create dimension and fact tables in the data warehouse.

- **warehouse_data.sql**  
  SQL INSERT statements populating:
  - 30 dates (January–February 2024)
  - 15 products across 3 categories
  - 12 customers across multiple cities
  - 40 sales transactions with realistic patterns

- **analytics_queries.sql**  
  OLAP queries for:
  - Time-based drill-down analysis
  - Top product performance with revenue contribution
  - Customer segmentation based on total spend

---

## Database Used

- **Database Name:** `fleximart_dw`
- **Schema Type:** Star Schema
- **Fact Table:** fact_sales
- **Dimensions:** dim_date, dim_product, dim_customer

---

## Key Highlights

- Line-item level granularity for maximum analytical flexibility
- Surrogate keys for performance and consistency
- Realistic sales distributions (weekday vs weekend)
- Use of CTEs, CASE statements, and aggregations

---

## Outcome

The data warehouse enables FlexiMart to perform advanced analytics such as trend analysis, customer segmentation, and product performance evaluation, supporting strategic business decisions.

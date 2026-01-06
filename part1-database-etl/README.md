# Part 1: Database Design and ETL Pipeline

## Overview

This part of the project focuses on building a reliable ETL (Extract, Transform, Load) pipeline for FlexiMart’s operational data. Raw CSV files containing customers, products, and sales data are cleaned, standardized, and loaded into a relational MySQL database. The goal is to ensure data quality, enforce relationships, and enable accurate business reporting.

---

## Objectives

- Ingest raw CSV files with data quality issues
- Clean and standardize inconsistent and missing data
- Load data into a normalized relational database
- Document the database schema and relationships
- Answer business questions using SQL queries

---

## Files in This Folder

- **etl_pipeline.py**  
  Python ETL script that reads raw CSV files, cleans the data, handles duplicates and missing values, and loads data into MySQL tables.

- **schema_documentation.md**  
  Text-based documentation describing entities, attributes, relationships, and normalization (3NF justification).

- **business_queries.sql**  
  SQL queries answering business questions related to customer behavior, product sales, and monthly trends.

- **data_quality_report.txt**  
  Automatically generated report summarizing records processed, duplicates removed, missing values handled, and successful loads.

---

## Database Used

- **Database Name:** `fleximart`
- **Tables:** customers, products, orders, order_items
- **Design:** Fully normalized (Third Normal Form)

---

## Key Highlights

- Standardized phone numbers and category names
- Removed duplicate records across all datasets
- Enforced referential integrity using foreign keys
- Used aggregation, HAVING clauses, and window functions in SQL queries

---

## Outcome

At the end of this part, FlexiMart has a clean, well-structured relational database that supports reliable operational reporting and serves as a foundation for downstream analytics.

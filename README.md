# FlexiMart Data Architecture Project

**Student Name:** Kapil Goyla  
**Student ID:** 25071901  
**Email:** kapilgoyla83@gmail.com  
**Date:** 06/01/2026

---

## Project Overview

This project implements a complete data architecture pipeline for FlexiMart, an e-commerce company. It covers end-to-end data processing from raw CSV ingestion and cleaning, relational database design and querying, NoSQL analysis using MongoDB, and analytical reporting using a dimensional data warehouse. The goal is to demonstrate practical data engineering, modeling, and analytics skills across multiple data systems.

---

## Repository Structure
```
├── part1-database-etl/
│ ├── etl_pipeline.py
│ ├── schema_documentation.md
│ ├── business_queries.sql
│ └── data_quality_report.txt
│
├── part2-nosql/
│ ├── nosql_analysis.md
│ ├── mongodb_operations.js
│ └── products_catalog.json
│
├── part3-datawarehouse/
│ ├── star_schema_design.md
│ ├── warehouse_schema.sql
│ ├── warehouse_data.sql
│ └── analytics_queries.sql
│
└── README.md
```

---

## Technologies Used

- **Python 3.11 (pandas, SQLAlchemy, mysql-connector-python)**
- **MySQL 8.0**
- **MongoDB 8.2.3**
- **SQL**
- **JavaScript (MongoDB Shell)**

---

## Setup Instructions

### Database Setup (MySQL)

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"
```

# Run Part 1 - ETL Pipeline
```bash
python part1-database-etl/etl_pipeline.py
```

# Run Part 1 - Business Queries
```bash
mysql -u root -p fleximart < part1-database-etl/business_queries.sql
```

# Run Part 3 - Data Warehouse Schema & Data
```bash
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
```

# Run Part 3 - Analytics Queries
```bash
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql
```

# MongoDB Setup - Run MongoDB operations
```bash
mongosh < part2-nosql/mongodb_operations.js
```

Note: The product catalog JSON file is imported using mongoimport as documented inside mongodb_operations.js.

# Key Learnings

This project strengthened my understanding of real-world data quality issues and how to handle them through ETL processes. I gained hands-on experience designing normalized relational schemas, writing complex SQL queries, and building dimensional models for analytics. I also learned how NoSQL databases like MongoDB support flexible schemas and aggregation-based analysis for semi-structured data.

# Challenges Faced

1. Handling data quality issues in raw CSV files:
Duplicate records, missing values, and inconsistent formats required careful transformation logic and validation before loading data into the database.

2. Maintaining referential integrity in the data warehouse:
Ensuring that all foreign keys in the fact table correctly referenced dimension tables required consistent surrogate key handling and controlled data insertion order.

# Notes

All SQL scripts and Python code are documented and structured for readability.

The project follows standard data engineering and dimensional modeling best practices.
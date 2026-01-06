# Part 2: NoSQL Database Analysis and MongoDB Implementation

## Overview

This part evaluates the limitations of relational databases for handling highly diverse product data and demonstrates how MongoDB can be used as a flexible alternative. It includes both theoretical justification and practical MongoDB operations using a product catalog dataset.

---

## Objectives

- Analyze why a traditional RDBMS is not ideal for highly variable product attributes
- Explain how MongoDB addresses schema flexibility and scalability needs
- Implement core MongoDB operations for querying, updating, and aggregating data

---

## Files in This Folder

- **nosql_analysis.md**  
  Written analysis covering:
  - Limitations of relational databases
  - Benefits of MongoDB for product catalogs
  - Trade-offs of using MongoDB instead of MySQL

- **mongodb_operations.js**  
  MongoDB shell script implementing:
  - Data loading verification
  - Filtered queries
  - Review-based aggregations
  - Update operations
  - Category-level analytics

- **products_catalog.json**  
  Sample product catalog containing flexible attributes and embedded reviews.

---

## Database Used

- **Database Name:** `fleximart_nosql`
- **Collection:** `products`
- **Model:** Document-based (schema-less)

---

## Key Highlights

- Used embedded documents for customer reviews
- Performed aggregation pipelines for average ratings and pricing analysis
- Demonstrated real-world NoSQL querying patterns
- Compared NoSQL trade-offs with relational systems

---

## Outcome

This part shows how MongoDB supports flexible schemas, nested data, and scalable analytics, making it suitable for dynamic product catalogs where relational schemas become restrictive.

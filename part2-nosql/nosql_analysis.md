# NoSQL Database Analysis for FlexiMart

## Section A: Limitations of RDBMS

A traditional relational database like MySQL is well-suited for structured and predictable data but struggles when product data becomes highly diverse. In an e-commerce platform such as FlexiMart, different product categories require different attributes. For example, laptops require attributes like RAM, processor, and storage, while shoes require size, color, and material. In a relational schema, this would require either a large number of nullable columns or multiple subtype tables, leading to complex joins and sparse data.

Frequent schema changes present another challenge. Introducing a new product type often requires altering table structures, which is costly, risky, and disruptive in production systems. Additionally, relational databases are not ideal for storing nested data such as customer reviews, ratings, and comments. These require separate tables and joins, increasing query complexity and reducing performance for read-heavy workloads.

Overall, rigid schemas and normalization constraints make relational databases less flexible for rapidly evolving and heterogeneous product catalogs.

---

## Section B: Benefits of MongoDB

MongoDB addresses these challenges through its flexible, document-based data model. Each product is stored as a JSON-like document, allowing different products to have different attributes without enforcing a fixed schema. For example, a laptop document can include RAM and processor fields, while a shoe document can include size and color fields, all within the same collection.

MongoDB also supports embedded documents, which makes it ideal for storing customer reviews directly inside product documents. Reviews, ratings, and comments can be nested as arrays, enabling faster read operations without complex joins. This aligns well with typical e-commerce access patterns where product details and reviews are fetched together.

In addition, MongoDB is designed for horizontal scalability using sharding. As the product catalog grows, data can be distributed across multiple servers, improving performance and availability. These features make MongoDB highly suitable for dynamic, large-scale product catalogs.

MongoDB also supports indexing on nested fields, allowing efficient filtering and sorting even when documents have varying structures.

---

## Section C: Trade-offs

Despite its advantages, MongoDB has trade-offs compared to MySQL. First, MongoDB provides weaker transactional guarantees across multiple documents. While it supports ACID transactions, they are more complex and less performant than single-table transactions in relational databases. This can be a limitation for operations requiring strong consistency across multiple entities.

Second, the lack of enforced schema can lead to data inconsistency if validation rules are not carefully implemented. Unlike MySQL, where constraints ensure data integrity, MongoDB relies more on application-level validation, increasing the risk of inconsistent or malformed data.

Additionally, analytics-style queries that require complex joins or strict reporting consistency are often simpler to express and optimize in a relational model.
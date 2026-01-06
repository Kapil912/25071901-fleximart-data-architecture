/*
Task 2.2 MongoDB Operations

Comments:
- Data was imported using mongoimport (CLI tool).
- The queries below were run in CMD and tested in MongoDB shell.
*/

use("fleximart_nosql");

// -----------------------------
// Operation 1: Load Data
// -----------------------------
// Import command used (run in CMD/PowerShell):
// mongoimport --db fleximart_nosql --collection products --file products_catalog.json --jsonArray
//
// Quick check:
print("\n[Op1] Documents in products collection:");
print(db.products.countDocuments());

// -----------------------------
// Operation 2: Basic Query
// -----------------------------
// Electronics products with price < 50000
// Return: name, price, stock
print("\n[Op2] Electronics (price < 50000) -> name, price, stock:");

const op2 = db.products.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { _id: 0, name: 1, price: 1, stock: 1 }
).toArray();

printjson(op2);

// -----------------------------
// Operation 3: Review Analysis
// -----------------------------
// Products with average rating >= 4.0
// Average is computed from the reviews array
print("\n[Op3] Products with avg rating >= 4.0:");

const op3 = db.products.aggregate([
  {
    $addFields: {
      avg_rating: { $avg: { $ifNull: ["$reviews.rating", []] } },
      review_count: { $size: { $ifNull: ["$reviews", []] } }
    }
  },
  { $match: { avg_rating: { $gte: 4.0 } } },
  {
    $project: {
      _id: 0,
      product_id: 1,
      name: 1,
      category: 1,
      avg_rating: { $round: ["$avg_rating", 2] },
      review_count: 1
    }
  },
  { $sort: { avg_rating: -1, review_count: -1 } }
]).toArray();

printjson(op3);

// -----------------------------
// Operation 4: Update Operation
// -----------------------------
// Add a review to product ELEC001
print("\n[Op4] Add review to ELEC001:");

const op4_update = db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user: "U999",
        rating: 4,
        comment: "Good value",
        date: new Date()
      }
    }
  }
);

print("Matched: " + op4_update.matchedCount + " | Modified: " + op4_update.modifiedCount);

// quick verify (show the product with reviews)
print("\n[Op4] Verify ELEC001 (reviews):");
printjson(
  db.products.find(
    { product_id: "ELEC001" },
    { _id: 0, product_id: 1, name: 1, reviews: 1 }
  ).toArray()
);

// -----------------------------
// Operation 5: Complex Aggregation
// -----------------------------
// Average price by category
// Return: category, avg_price, product_count
print("\n[Op5] Avg price by category:");

const op5 = db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: { $round: ["$avg_price", 2] },
      product_count: 1
    }
  },
  { $sort: { avg_price: -1 } }
]).toArray();

printjson(op5);

print("\nDone.\n");

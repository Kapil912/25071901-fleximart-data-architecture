import os
import re
import logging
from decimal import Decimal, InvalidOperation
from typing import Dict, Tuple

import pandas as pd
from dateutil import parser
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError



# =========================
# CONFIG
# =========================
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_DIR = os.path.join(BASE_DIR, "data")

CUSTOMERS_CSV = os.path.join(DATA_DIR, "customers_raw.csv")
PRODUCTS_CSV = os.path.join(DATA_DIR, "products_raw.csv")
SALES_CSV = os.path.join(DATA_DIR, "sales_raw.csv")

REPORT_FILE = "data_quality_report.txt"
LOG_FILE = "etl_pipeline.log"

DB_URL = "mysql+pymysql://root:testpractice@localhost:3306/fleximart"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ],
)


# =========================
# HELPERS
# =========================

def parse_date_any(value) -> pd.Timestamp:
    """
    Converts many date formats into a proper date (YYYY-MM-DD).
    Examples handled:
      - 2024-01-15
      - 15/01/2024
      - 02/22/2024
      - 15-04-2023
    Returns pd.NaT if it cannot parse.
    """
    if pd.isna(value):
        return pd.NaT

    s = str(value).strip()
    if not s:
        return pd.NaT

    # unify separators
    s2 = s.replace(".", "/").replace("-", "/")

    try:
        parts = s2.split("/")
        # If the first chunk is >12, it's very likely day-first (DD/MM/YYYY)
        if len(parts) >= 3 and parts[0].isdigit() and int(parts[0]) > 12:
            dt = parser.parse(s2, dayfirst=True)
        else:
            dt = parser.parse(s2, dayfirst=False)
        return pd.Timestamp(dt.date())
    except Exception:
        return pd.NaT


def standardize_phone(phone: str, default_cc="+91") -> str:
    """
    Standardizes phones to +91-XXXXXXXXXX (keeps the last 10 digits).
    Examples:
      9876543210 -> +91-9876543210
      09988112233 -> +91-9988112233
      +919876501234 -> +91-9876501234
    """
    if pd.isna(phone):
        return None

    s = str(phone).strip()
    if not s:
        return None

    digits = re.sub(r"\D", "", s)  # keep only digits
    if len(digits) < 10:
        return None

    last10 = digits[-10:]
    return f"{default_cc}-{last10}"


def standardize_category(cat: str) -> str:
    """
    Makes category consistent:
      electronics/ELECTRONICS -> Electronics
    """
    if pd.isna(cat):
        return "Uncategorized"
    s = str(cat).strip()
    if not s:
        return "Uncategorized"
    return s.lower().title()


def to_decimal(x, default=None):
    """
    Converts values into Decimal for money fields.
    If invalid/missing, returns default.
    """
    if pd.isna(x):
        return default
    try:
        s = str(x).strip()
        if s == "":
            return default
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return default


def write_report(report: dict, path: str = REPORT_FILE):
    """
    Writes the grading-friendly data_quality_report.txt
    """
    lines = []
    lines.append("FlexiMart ETL Data Quality Report")
    lines.append("=" * 35)
    lines.append("")

    for section, metrics in report.items():
        lines.append(f"[{section}]")
        for k, v in metrics.items():
            lines.append(f"- {k}: {v}")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# =========================
# EXTRACT
# =========================

def extract_csv(path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a pandas DataFrame.
    Fails fast if the file is missing.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File not found: {path}. "
            f"Make sure it is in the same folder as etl_pipeline.py"
        )

    df = pd.read_csv(path)
    return df


# =========================
# TRANSFORM: CUSTOMERS
# =========================

def transform_customers(df: pd.DataFrame, report: dict) -> pd.DataFrame:
    """
    Cleans customers_raw.csv to match the DB schema.
    Returns a cleaned DataFrame ready for loading into the customers table.
    Also updates the report dict with data-quality metrics.
    """
    section = "customers_raw.csv"
    metrics = {
        "records_read": int(len(df)),
        "duplicates_removed": 0,
        "missing_values_handled": 0,
        "records_after_cleaning": 0,
    }

    out = df.copy()

    # 1) Remove exact duplicate rows
    before = len(out)
    out = out.drop_duplicates()
    metrics["duplicates_removed"] += int(before - len(out))

    # 2) Normalize emails (lowercase + trim)
    out["email"] = out["email"].astype(str).str.strip().str.lower()

    # Convert placeholder strings to real missing values
    out.loc[out["email"].isin(["nan", "none", ""]), "email"] = None

    # 3) Drop rows with missing email (required by schema: UNIQUE NOT NULL)
    before = len(out)
    out = out[out["email"].notna()].copy()
    metrics["missing_values_handled"] += int(before - len(out))

    # 4) Remove duplicate customers by email (email must be unique in DB)
    before = len(out)
    out = out.drop_duplicates(subset=["email"], keep="first")
    metrics["duplicates_removed"] += int(before - len(out))

    # 5) Standardize phone numbers to +91-XXXXXXXXXX
    out["phone"] = out["phone"].apply(standardize_phone)

    # 6) Standardize registration_date to a real date
    out["registration_date"] = out["registration_date"].apply(parse_date_any)
    out["registration_date"] = pd.to_datetime(out["registration_date"], errors="coerce").dt.date

    # 7) Basic text cleanup
    out["first_name"] = out["first_name"].astype(str).str.strip()
    out["last_name"] = out["last_name"].astype(str).str.strip()
    out["city"] = out["city"].astype(str).str.strip()

    # Final metric
    metrics["records_after_cleaning"] = int(len(out))
    report[section] = metrics

    # Keep raw customer_id for mapping later (C001 -> DB customer_id)
    return out[["customer_id", "first_name", "last_name", "email", "phone", "city", "registration_date"]]

# =========================
# TRANSFORM: PRODUCTS
# =========================

def transform_products(df: pd.DataFrame, report: dict) -> pd.DataFrame:
    """
    Cleans products_raw.csv to match the DB schema.
    Returns a cleaned DataFrame ready for loading into products table.
    Also updates the report dict with data-quality metrics.
    """
    section = "products_raw.csv"
    metrics = {
        "records_read": int(len(df)),
        "duplicates_removed": 0,
        "missing_values_handled": 0,
        "records_after_cleaning": 0,
    }

    out = df.copy()

    # 1) Standardize category names (e.g., electronics/ELECTRONICS -> Electronics)
    out["category"] = out["category"].apply(standardize_category)

    # 2) Convert price to Decimal; drop rows where price is missing/invalid
    out["price"] = out["price"].apply(lambda x: to_decimal(x, default=None))

    before = len(out)
    out = out[out["price"].notna()].copy()
    metrics["missing_values_handled"] += int(before - len(out))

    # 3) stock_quantity: convert to int; fill missing/null with 0 (schema default)
    stock_num = pd.to_numeric(out["stock_quantity"], errors="coerce")
    missing_stock = int(stock_num.isna().sum())

    out["stock_quantity"] = stock_num.fillna(0).astype(int)
    metrics["missing_values_handled"] += missing_stock

    # 4) Remove duplicates using (product_name, category)
    before = len(out)
    out = out.drop_duplicates(subset=["product_name", "category"], keep="first")
    metrics["duplicates_removed"] += int(before - len(out))

    metrics["records_after_cleaning"] = int(len(out))
    report[section] = metrics

    # Keep raw product_id for mapping later (P001 -> DB product_id)
    return out[["product_id", "product_name", "category", "price", "stock_quantity"]]

# =========================
# TRANSFORM: SALES
# =========================

def transform_sales(df: pd.DataFrame, report: dict) -> pd.DataFrame:
    """
    Cleans sales_raw.csv and returns a cleaned DataFrame.
    This cleaned sales data will later be converted into orders + order_items.
    """
    section = "sales_raw.csv"
    metrics = {
        "records_read": int(len(df)),
        "duplicates_removed": 0,
        "missing_values_handled": 0,
        "records_after_cleaning": 0,
    }

    out = df.copy()

    # 1) Remove exact duplicate rows
    before = len(out)
    out = out.drop_duplicates()
    metrics["duplicates_removed"] += int(before - len(out))

    # 2) Remove duplicate transaction_id (duplicate transactions)
    before = len(out)
    out = out.drop_duplicates(subset=["transaction_id"], keep="first")
    metrics["duplicates_removed"] += int(before - len(out))

    # 3) Drop rows missing customer_id or product_id (needed for FK mapping later)
    before = len(out)
    out = out[out["customer_id"].notna() & out["product_id"].notna()].copy()
    metrics["missing_values_handled"] += int(before - len(out))

    # 4) Standardize transaction_date
    out["transaction_date"] = out["transaction_date"].apply(parse_date_any)

    before = len(out)
    out = out[out["transaction_date"].notna()].copy()
    metrics["missing_values_handled"] += int(before - len(out))

    out["transaction_date"] = pd.to_datetime(out["transaction_date"], errors="coerce").dt.date

    # 5) quantity must be numeric and > 0
    out["quantity"] = pd.to_numeric(out["quantity"], errors="coerce")

    before = len(out)
    out = out[(out["quantity"].notna()) & (out["quantity"] > 0)].copy()
    metrics["missing_values_handled"] += int(before - len(out))

    out["quantity"] = out["quantity"].astype(int)

    # 6) unit_price as Decimal (fallback 0.00 if missing/invalid)
    out["unit_price"] = out["unit_price"].apply(lambda x: to_decimal(x, default=Decimal("0.00")))

    # 7) status: fill blanks with 'Pending'
    out["status"] = out["status"].astype(str).str.strip()
    out.loc[out["status"].isin(["nan", "none", ""]), "status"] = "Pending"

    metrics["records_after_cleaning"] = int(len(out))
    report[section] = metrics

    return out

# =========================
# LOAD: DB SETUP
# =========================

def ensure_tables_exist(engine):
    """
    Safety net: Creates tables if they don't exist.
    If you already created tables in MySQL Workbench, this will simply do nothing.
    """
    ddl = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        city VARCHAR(50),
        registration_date DATE
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY AUTO_INCREMENT,
        product_name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        stock_quantity INT DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT NOT NULL,
        order_date DATE NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending',
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INT PRIMARY KEY AUTO_INCREMENT,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        unit_price DECIMAL(10,2) NOT NULL,
        subtotal DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """

    with engine.begin() as conn:
        for stmt in ddl.strip().split(";"):
            s = stmt.strip()
            if s:
                conn.execute(text(s))

# =========================
# LOAD: CUSTOMERS + PRODUCTS
# =========================

def load_customers(engine, customers_df: pd.DataFrame) -> int:
    """
    Loads cleaned customers into MySQL.
    INSERT IGNORE prevents duplicate email errors.
    Returns number of attempted inserts (for reporting).
    """
    loaded = 0
    with engine.begin() as conn:
        for _, r in customers_df.iterrows():
            conn.execute(text("""
                INSERT IGNORE INTO customers (first_name, last_name, email, phone, city, registration_date)
                VALUES (:first_name, :last_name, :email, :phone, :city, :registration_date)
            """), {
                "first_name": r["first_name"],
                "last_name": r["last_name"],
                "email": r["email"],
                "phone": r["phone"],
                "city": r["city"],
                "registration_date": r["registration_date"]
            })
            loaded += 1
    return loaded

def load_products(engine, products_df: pd.DataFrame) -> int:
    """
    Loads cleaned products into MySQL.
    Returns number of inserts attempted (for reporting).
    """
    loaded = 0
    with engine.begin() as conn:
        for _, r in products_df.iterrows():
            conn.execute(text("""
                INSERT INTO products (product_name, category, price, stock_quantity)
                VALUES (:product_name, :category, :price, :stock_quantity)
            """), {
                "product_name": r["product_name"],
                "category": r["category"],
                "price": r["price"],
                "stock_quantity": int(r["stock_quantity"])
            })
            loaded += 1
    return loaded

# =========================
# LOAD: ID MAPPINGS
# =========================

def build_customer_map(engine, customers_clean: pd.DataFrame) -> Dict[str, int]:
    """
    Creates mapping:
      raw_customer_id (e.g., C001) -> db_customer_id (e.g., 1)
    Uses email to link the cleaned customer row to the inserted DB row.
    """
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT customer_id, email FROM customers")).fetchall()

    db_email_to_id = {str(r[1]).lower(): int(r[0]) for r in rows}

    raw_to_db = {}
    for _, r in customers_clean.iterrows():
        email = str(r["email"]).lower()
        raw = r["customer_id"]
        if email in db_email_to_id:
            raw_to_db[raw] = db_email_to_id[email]

    return raw_to_db

def build_product_map(engine, products_clean: pd.DataFrame) -> Dict[str, int]:
    """
    Creates mapping:
      raw_product_id (e.g., P001) -> db_product_id (e.g., 1)
    Uses (product_name, category) as the matching key.
    """
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT product_id, product_name, category FROM products")).fetchall()

    db_key_to_id = {(r[1], r[2]): int(r[0]) for r in rows}

    raw_to_db = {}
    for _, r in products_clean.iterrows():
        raw = r["product_id"]
        key = (r["product_name"], r["category"])
        if key in db_key_to_id:
            raw_to_db[raw] = db_key_to_id[key]

    return raw_to_db

# =========================
# LOAD: ORDERS + ORDER_ITEMS
# =========================

def load_orders_and_items(
    engine,
    sales_clean: pd.DataFrame,
    cust_map: Dict[str, int],
    prod_map: Dict[str, int]
) -> Tuple[int, int, int, int, int]:
    """
    Loads orders and order_items from sales data.

    Each row in sales_clean is treated as:
      1 order + 1 order_item

    Returns:
      (orders_loaded,
       items_loaded,
       skipped_rows_due_to_missing_mapping,
       skipped_missing_customer_mapping,
       skipped_missing_product_mapping)
    """
    orders_loaded = 0
    items_loaded = 0
    skipped = 0
    missing_customer = 0
    missing_product = 0

    with engine.begin() as conn:
        for _, r in sales_clean.iterrows():
            raw_cust = r["customer_id"]
            raw_prod = r["product_id"]

            # Track why mapping fails (customer vs product)
            cust_ok = raw_cust in cust_map
            prod_ok = raw_prod in prod_map

            if not cust_ok:
                missing_customer += 1
            if not prod_ok:
                missing_product += 1

            # Skip if we can't map raw ids to DB ids
            if not cust_ok or not prod_ok:
                skipped += 1
                continue

            db_cust = cust_map[raw_cust]
            db_prod = prod_map[raw_prod]

            qty = int(r["quantity"])
            unit_price = r["unit_price"]
            subtotal = Decimal(qty) * unit_price

            # Insert order
            res = conn.execute(text("""
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (:customer_id, :order_date, :total_amount, :status)
            """), {
                "customer_id": db_cust,
                "order_date": r["transaction_date"],
                "total_amount": subtotal,
                "status": r["status"] if r["status"] else "Pending"
            })

            order_id = res.lastrowid
            orders_loaded += 1

            # Insert order_item
            conn.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
                VALUES (:order_id, :product_id, :quantity, :unit_price, :subtotal)
            """), {
                "order_id": order_id,
                "product_id": db_prod,
                "quantity": qty,
                "unit_price": unit_price,
                "subtotal": subtotal
            })

            items_loaded += 1

    return orders_loaded, items_loaded, skipped, missing_customer, missing_product


# =========================
# MAIN ETL RUNNER
# =========================

def main():
    # This dict will accumulate quality metrics for each file + the final load summary
    report = {}

    logging.info("Connecting to MySQL...")
    engine = create_engine(DB_URL, future=True)

    # Safety: ensure DB tables exist (won't overwrite if already created)
    logging.info("Ensuring tables exist...")
    ensure_tables_exist(engine)

    # --------
    # EXTRACT
    # --------
    logging.info("Extracting CSV files...")
    customers_raw = extract_csv(CUSTOMERS_CSV)
    products_raw = extract_csv(PRODUCTS_CSV)
    sales_raw = extract_csv(SALES_CSV)

    # --------
    # TRANSFORM
    # --------
    logging.info("Transforming customers...")
    customers_clean = transform_customers(customers_raw, report)

    logging.info("Transforming products...")
    products_clean = transform_products(products_raw, report)

    logging.info("Transforming sales...")
    sales_clean = transform_sales(sales_raw, report)

    # --------
    # LOAD
    # --------
    logging.info("Loading customers into DB...")
    customers_loaded = load_customers(engine, customers_clean)

    logging.info("Loading products into DB...")
    products_loaded = load_products(engine, products_clean)

    # Build mappings from raw IDs (C001/P001) -> DB auto-increment IDs (1/2/3...)
    logging.info("Building raw->DB ID mappings...")
    cust_map = build_customer_map(engine, customers_clean)
    prod_map = build_product_map(engine, products_clean)

    # Load orders and order_items from sales
    logging.info("Loading orders and order_items into DB...")
    (
        orders_loaded,
        items_loaded,
        skipped_sales,
        skipped_missing_customer,
        skipped_missing_product
    ) = load_orders_and_items(engine, sales_clean, cust_map, prod_map)

    # Add a final summary section for your report file
    report["LOAD_SUMMARY"] = {
        "customers_loaded_successfully": customers_loaded,
        "products_loaded_successfully": products_loaded,
        "orders_loaded_successfully": orders_loaded,
        "order_items_loaded_successfully": items_loaded,
        "sales_rows_skipped_due_to_missing_id_mapping": skipped_sales,
        "sales_rows_skipped_missing_customer_mapping": skipped_missing_customer,
        "sales_rows_skipped_missing_product_mapping": skipped_missing_product
    }

    # Write the data_quality_report.txt
    write_report(report, REPORT_FILE)

    logging.info(f" ETL complete. Report generated: {REPORT_FILE}")
    logging.info(f" Log generated: {LOG_FILE}")

if __name__ == "__main__":
    try:
        main()
    except SQLAlchemyError:
        logging.exception(" Database error occurred during ETL.")
        raise
    except Exception:
        logging.exception(" ETL failed due to an unexpected error.")
        raise



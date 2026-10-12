-- Cloudflare D1 Schema for Fair Dinkum Publishing & AI Advisory

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    price REAL NOT NULL,
    provider TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prospects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    contact_name TEXT,
    email TEXT,
    city TEXT,
    industry TEXT,
    status TEXT DEFAULT 'New',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sales_created ON sales(created_at);
CREATE INDEX IF NOT EXISTS idx_prospects_city ON prospects(city);

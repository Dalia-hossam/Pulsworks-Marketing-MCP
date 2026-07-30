PRAGMA foreign_keys = ON;

-- 1. Users Table (Used for Authentication and notifications/tools/list_changed)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('ANALYST', 'MANAGER', 'ADMIN'))
);

-- 2. Customers Table
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    company TEXT,
    status TEXT NOT NULL CHECK(status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED')) DEFAULT 'ACTIVE'
);

-- 3. Campaigns Table
CREATE TABLE IF NOT EXISTS campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    budget REAL NOT NULL CHECK(budget >= 0),
    max_daily_spend REAL DEFAULT 1000.0,
    status TEXT NOT NULL CHECK(status IN ('DRAFT', 'ACTIVE', 'PAUSED', 'COMPLETED')) DEFAULT 'DRAFT'
);

-- 4. Campaign Results / Performance Logs
CREATE TABLE IF NOT EXISTS campaign_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    clicks INTEGER DEFAULT 0 CHECK(clicks >= 0),
    conversions INTEGER DEFAULT 0 CHECK(conversions >= 0),
    revenue REAL DEFAULT 0.0 CHECK(revenue >= 0.0),
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- 5. Audit Logs (Mandatory for tracking mutations & Elicitation outputs)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    performed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
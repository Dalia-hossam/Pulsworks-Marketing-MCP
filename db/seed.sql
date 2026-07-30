-- 1. Seed Users
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'ADMIN'),
('manager', 'manager123', 'MANAGER'),
('employee', 'employee123', 'ANALYST');

-- 2. Seed Customers
INSERT INTO customers (full_name, email, company, status) VALUES
('Ahmed Ali', 'ahmed@company.com', 'ABC Corp', 'ACTIVE'),
('Sara Mohamed', 'sara@company.com', 'Tech Solutions', 'ACTIVE'),
('Omar Hassan', 'omar@company.com', 'Future Media', 'INACTIVE');

-- 3. Seed Campaigns
INSERT INTO campaigns (campaign_name, start_date, end_date, budget, max_daily_spend, status) VALUES
('Summer Sale 2026', '2026-07-01', '2026-07-31', 5000.0, 1000.0, 'ACTIVE'),
('Back to School', '2026-08-01', '2026-08-31', 7000.0, 1500.0, 'DRAFT');

-- 4. Seed Campaign Results
INSERT INTO campaign_results (campaign_id, customer_id, clicks, conversions, revenue) VALUES
(1, 1, 1200, 45, 8500.0),
(1, 2, 900, 30, 5400.0),
(2, 3, 300, 10, 1800.0);
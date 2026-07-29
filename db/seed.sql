-- Users
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('manager', 'manager123', 'manager'),
('employee', 'employee123', 'employee');

-- Customers
INSERT INTO customers (full_name, email, company, status) VALUES
('Ahmed Ali', 'ahmed@company.com', 'ABC Corp', 'Active'),
('Sara Mohamed', 'sara@company.com', 'Tech Solutions', 'Active'),
('Omar Hassan', 'omar@company.com', 'Future Media', 'Inactive');

-- Campaigns
INSERT INTO campaigns (campaign_name, start_date, end_date, budget, status) VALUES
('Summer Sale', '2026-07-01', '2026-07-31', 5000, 'Running'),
('Back to School', '2026-08-01', '2026-08-31', 7000, 'Planned');

-- Campaign Results
INSERT INTO campaign_results (campaign_id, customer_id, clicks, conversions, revenue) VALUES
(1, 1, 1200, 45, 8500),
(1, 2, 900, 30, 5400),
(2, 3, 300, 10, 1800);
CREATE TABLE IF NOT EXISTS clients_clean (
    client_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT NOT NULL,
    phone TEXT,
    join_date DATE,
    risk_level TEXT,
    assets_under_management INT
);

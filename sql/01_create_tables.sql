CREATE TABLE user_profiles (
    user_id VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(100),
    city VARCHAR(50),
    account_age_days INT,
    avg_monthly_txn_amt DECIMAL(12,2),
    typical_hour_min INT,
    typical_hour_max INT,
    risk_tier VARCHAR(10),
    last_txn_date DATE
);

CREATE TABLE merchant_profiles (
    merchant_id VARCHAR(10) PRIMARY KEY,
    merchant_name VARCHAR(150),
    category VARCHAR(30),
    city VARCHAR(50),
    registration_days INT,
    avg_txn_count_daily INT,
    refund_rate_pct DECIMAL(5,2),
    chargeback_count INT,
    merchant_risk_flag VARCHAR(10)
);

CREATE TABLE upi_transactions (
    txn_id VARCHAR(20) PRIMARY KEY,
    user_id VARCHAR(10),
    merchant_id VARCHAR(10),
    txn_timestamp TIMESTAMP,
    txn_date DATE,
    txn_hour INT,
    txn_day_of_week VARCHAR(10),
    amount DECIMAL(12,2),
    merchant_category VARCHAR(30),
    payment_mode VARCHAR(20),
    device_id VARCHAR(20),
    is_new_device BOOLEAN,
    is_fraud BOOLEAN,
    fraud_type VARCHAR(30)
);

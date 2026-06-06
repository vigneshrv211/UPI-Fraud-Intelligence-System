# UPI Fraud Intelligence System

An end-to-end data engineering and analytics project that simulates, detects, and analyzes fraudulent UPI transactions. Built to demonstrate real-world fraud monitoring capabilities using Python, PostgreSQL, SQL analytics, and Power BI.

---

## What This Project Does

UPI fraud is one of the fastest-growing financial crime vectors in India. This project replicates a production-style fraud intelligence pipeline — from synthetic transaction data generation all the way to executive-level Power BI dashboards — covering velocity detection, Z-score anomaly analysis, merchant risk scoring, and behavioral analytics.

---

## Architecture
<img width="917" height="612" alt="image" src="https://github.com/user-attachments/assets/07f3107a-6d64-41cf-87cd-0f0d7c4c064e" />

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data Generation | Python, Pandas, NumPy, Faker |
| Database | PostgreSQL, psycopg2 |
| Analytics | SQL (Window Functions, CTEs, Z-Score) |
| Visualization | Power BI, DAX, Power Query |
| Dev Tools | VS Code, Git, GitHub, Draw.io |

## Project Structure

```text
UPI-Fraud-Intelligence-System/
│
├── data/
│   ├── user_profiles.csv
│   ├── merchant_profiles.csv
│   ├── upi_transactions.csv
│   └── upi_txn_features.csv
│
├── outputs/
│   ├── 01_Executive_Fraud_Overview_Dashboard.png
│   ├── 02_Fraud_Investigation_Report_Dashboard.png
│   ├── 03_Merchant_Risk_Intelligence_Dashboard.png
│   ├── 04_User_Behavorial_Analytics_Dashboard.png
│   ├── fraud_by_hour.png
│   ├── fraud_score_dist.png
│   └── risk_level_distribution.png
│
├── scripts/
│   ├── db_connection.py
│   ├── generate_user_data.py
│   ├── generate_merchant_profiles.py
│   ├── generate_transactions.py
│   ├── Feature_engineering.py
│   ├── eda_fraud_analysis.py
│   └── test_setup.py
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_velocity_detection.sql
│   ├── 03_user_anomaly_zscore.sql
│   ├── 04_merchant_risk_ranking.sql
│   └── 05_hourly_fraud_heatmap.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Fraud Detection Logic

**Velocity Detection** — flags users or merchants with abnormally high transaction frequency within short time windows.

**Z-Score Anomaly Detection** — identifies users whose transaction amounts deviate significantly from their own historical baseline.

**Merchant Risk Ranking** — scores merchants based on fraud rate, chargeback volume, and transaction patterns.

**Hourly Fraud Heatmap** — reveals temporal fraud patterns to support operational alerting.

**Fraud Score Calculation** — composite risk score combining all signals for investigation prioritization.

---

## Power BI Dashboards

**1. Executive Fraud Overview** — KPIs (total transactions, fraud amount, fraud rate %), risk distribution, and trend lines.

<img width="1157" height="730" alt="01_Executive Fraud_Overview_Dashboard" src="https://github.com/user-attachments/assets/882b41a9-3699-4c2c-aa5e-3a8514316bd8" />

**2. Fraud Investigation Report** — fraud type breakdown, high-risk transaction drilldown, fraud score distribution.

<img width="1156" height="647" alt="02_Fraud_Investigation_Report_Dashboard" src="https://github.com/user-attachments/assets/4108876b-6e04-48e5-9a2c-6a8588844da4" />

**3. Merchant Risk Intelligence** — merchant risk rankings, category-level risk analysis, chargeback patterns.

<img width="1167" height="660" alt="03_Merchant_Risk_Intelligence_Dashboard" src="https://github.com/user-attachments/assets/253fdcfe-4b77-42a6-bb92-3216d2bf1ee0" />

**4. User Behavioral Analytics** — user risk segmentation, transaction hour analysis, anomaly detection view.
<img width="1157" height="652" alt="04_User_Behavorial_Analytics_Dashboard" src="https://github.com/user-attachments/assets/cd25c397-7fc2-4f28-a2ab-f7f6dfa26fb4" />


---

## Key Findings

- Identified high-risk merchant clusters through composite risk scoring
- Detected suspicious user behavior using Z-score deviation from personal baselines
- Found peak fraud hours through temporal heatmap analysis
- Enabled investigation prioritization using risk segmentation (High / Medium / Low)

---

## Getting Started

**Clone the repository**
```bash
git clone https://github.com/vigneshrv211/UPI-Fraud-Intelligence-System.git
cd UPI-Fraud-Intelligence-System
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Set up PostgreSQL**

Create a local PostgreSQL database and configure your `.env` file with the connection details.

**Generate data**
```bash
python scripts/generate_user_data.py
python scripts/generate_merchant_profiles.py
python scripts/generate_transactions.py
```

**Run feature engineering**
```bash
python scripts/Feature_engineering.py
```

**Execute SQL analytics**

Run scripts inside the `sql/` folder in sequence (01 → 05).

**Load into Power BI**

Import the CSV files from `data/` into Power BI and connect to the dashboards.

---

## Project Structure

import pandas as pd
import random
from datetime import datetime, timedelta
from db_connection import engine

# -----------------------------
# LOAD USERS & MERCHANTS
# -----------------------------
users_df = pd.read_sql(
    "SELECT * FROM user_profiles1",
    engine
)

merchants_df = pd.read_sql(
    "SELECT * FROM merchants_profiles",
    engine
)


# -----------------------------
# CONFIG
# -----------------------------
NUM_TXN = 15000
FRAUD_RATE = 0.08

MODES = [
    "UPI_QR",
    "UPI_ID",
    "COLLECT_REQUEST"
]

FRAUD_TYPES = [
    "VELOCITY",
    "ACCOUNT_TAKEOVER",
    "UNUSUAL_AMOUNT",
    "DORMANT_SPIKE",
    "MERCHANT_FRAUD"
]

start_date = datetime(2023, 4, 1)
end_date = datetime(2024, 3, 31)

transactions = []
devices_used = {}

# -----------------------------
# GENERATE TRANSACTIONS
# -----------------------------
for i in range(NUM_TXN):

    user = users_df.sample(1).iloc[0]
    merchant = merchants_df.sample(1).iloc[0]

    user_id = user["user_id"]
    merchant_id = merchant["merchant_id"]

    is_fraud = random.random() < FRAUD_RATE

    fraud_type = None

    if is_fraud:
        fraud_type = random.choice(FRAUD_TYPES)

    # -------------------------
    # Timestamp
    # -------------------------
    random_seconds = random.randint(
        0,
        int((end_date - start_date).total_seconds())
    )

    txn_time = start_date + timedelta(seconds=random_seconds)

    if fraud_type in ["ACCOUNT_TAKEOVER", "DORMANT_SPIKE"]:
        txn_time = txn_time.replace(
            hour=random.randint(1, 4),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

    # -------------------------
    # Amount
    # -------------------------
    avg_amt = float(user["avg_monthly_txn_amt"])

    if fraud_type == "UNUSUAL_AMOUNT":
        amount = round(avg_amt * random.uniform(8, 25), 2)

    elif fraud_type == "VELOCITY":
        amount = round(random.uniform(1, 200), 2)

    elif fraud_type == "DORMANT_SPIKE":
        amount = round(avg_amt * random.uniform(5, 15), 2)

    else:
        amount = round(avg_amt * random.uniform(0.5, 2), 2)

    # -------------------------
    # Device Logic
    # -------------------------
    if user_id not in devices_used:
        devices_used[user_id] = []

    if fraud_type == "ACCOUNT_TAKEOVER" or len(devices_used[user_id]) == 0:

        device_id = f"DEV-{random.randint(10000,99999)}"
        is_new_device = True

        devices_used[user_id].append(device_id)

    else:

        device_id = random.choice(devices_used[user_id])
        is_new_device = False

    # -------------------------
    # Create Record
    # -------------------------
    transactions.append({

        "txn_id": f"TXN-{i+1:05d}",

        "user_id": user_id,

        "merchant_id": merchant_id,

        "txn_timestamp": txn_time,

        "txn_date": txn_time.date(),

        "txn_hour": txn_time.hour,

        "txn_day_of_week":
            txn_time.strftime("%A").upper()[:3],

        "amount": amount,

        "merchant_category":
            merchant["category"],

        "payment_mode":
            random.choice(MODES),

        "device_id":
            device_id,

        "is_new_device":
            is_new_device,

        "is_fraud":
            is_fraud,

        "fraud_type":
            fraud_type
    })

# -----------------------------
# SAVE CSV
# -----------------------------
txn_df = pd.DataFrame(transactions)

txn_df.to_sql(
    "upi_transaction",
    engine,
    if_exists="replace",
    index=False
)

# -----------------------------
# SUMMARY
# -----------------------------
print("\nTransactions Generated")
print("=" * 40)

print("Total Transactions :", len(txn_df))
print("Fraud Count        :", txn_df["is_fraud"].sum())
print("Fraud Rate         :", round(txn_df["is_fraud"].mean() * 100, 2), "%")

print("\nFraud Type Breakdown")
print(txn_df[txn_df["is_fraud"]]["fraud_type"].value_counts())
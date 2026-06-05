import pandas as pd
import numpy as np
from db_connection import engine

txn = pd.read_sql(
    "SELECT * FROM upi_transaction",
    engine
)

users = pd.read_sql(
    "SELECT * FROM user_profiles1",
    engine
)

merchants = pd.read_sql(
    "SELECT * FROM merchants_profiles",
    engine
)

txn["txn_timestamp"] = pd.to_datetime(txn["txn_timestamp"])
txn["txn_date"] = pd.to_datetime(txn["txn_date"])

user_stats = (
    txn.groupby("user_id")["amount"]
       .agg(["mean", "std"])
       .reset_index()
)

user_stats.columns = [
    "user_id",
    "user_avg_amt",
    "user_std_amt"
]

txn = txn.merge(
    user_stats,
    on="user_id",
    how="left"
)

txn["user_amt_zscore"] = (
    (txn["amount"] - txn["user_avg_amt"])
    /
    txn["user_std_amt"].replace(0, 1)
).round(2)

print(
    txn[
        [
            "user_id",
            "amount",
            "user_avg_amt",
            "user_std_amt",
            "user_amt_zscore"
        ]
    ].head()
)

def hour_risk(hour):

    if 1 <= hour <= 4:
        return 100

    elif hour == 0 or hour == 23:
        return 70

    elif 5 <= hour <= 7:
        return 40

    else:
        return 10


txn["hour_risk_score"] = txn["txn_hour"].apply(hour_risk)

print(
    txn[
        [
            "txn_hour",
            "hour_risk_score"
        ]
    ].head(20)
)

txn = txn.merge(
    users[
        [
            "user_id",
            "typical_hour_min",
            "typical_hour_max"
        ]
    ],
    on="user_id",
    how="left"
)

txn["is_outside_typical_hour"] = (
    (txn["txn_hour"] < txn["typical_hour_min"])
    |
    (txn["txn_hour"] > txn["typical_hour_max"])
).astype(int)

print(
    txn[
        [
            "user_id",
            "txn_hour",
            "typical_hour_min",
            "typical_hour_max",
            "is_outside_typical_hour"
        ]
    ].head(20)
)

txn = txn.merge(
    users[
        [
            "user_id",
            "last_txn_date"
        ]
    ],
    on="user_id",
    how="left"
)

txn["last_txn_date"] = pd.to_datetime(
    txn["last_txn_date"]
)

txn["days_since_last_txn"] = (
    txn["txn_date"] - txn["last_txn_date"]
).dt.days

print(
    txn[
        [
            "user_id",
            "txn_date",
            "last_txn_date",
            "days_since_last_txn"
        ]
    ].head(20)
)

txn["is_new_device_high_amount"] = (
    (txn["is_new_device"] == True)
    &
    (txn["amount"] > txn["user_avg_amt"] * 2)
).astype(int)

print(
    txn[
        [
            "is_new_device",
            "amount",
            "user_avg_amt",
            "is_new_device_high_amount"
        ]
    ].head(20)
)

print(
    txn["is_new_device_high_amount"]
    .value_counts()
)
txn[
    txn["is_new_device_high_amount"] == 1
][
    [
        "user_id",
        "is_new_device",
        "amount",
        "user_avg_amt",
        "is_new_device_high_amount"
    ]
].head(10)

txn = txn.merge(
    merchants[
        [
            "merchant_id",
            "refund_rate_pct",
            "chargeback_count",
            "registration_days",
            "merchant_risk_flag"
        ]
    ],
    on="merchant_id",
    how="left"
)

txn.rename(
    columns={
        "refund_rate_pct": "merchant_refund_rate"
    },
    inplace=True
)

txn["merchant_is_new"] = (
    txn["registration_days"] < 30
).astype(int)

print(
    txn[
        [
            "merchant_id",
            "merchant_refund_rate",
            "registration_days",
            "merchant_is_new"
        ]
    ].head(20)
)

CATEGORY_RISK = {
    "FOOD": 5,
    "RETAIL": 10,
    "FUEL": 10,
    "TRAVEL": 20,
    "GAMING": 60,
    "CRYPTO_EXCHANGE": 90
}

txn["category_risk_score"] = (
    txn["merchant_category"]
    .map(CATEGORY_RISK)
    .fillna(15)
)

print(
    txn[
        [
            "merchant_category",
            "category_risk_score"
        ]
    ].head(20)
)

print(
    txn["merchant_category"]
    .value_counts()
)

txn["fraud_score"] = (

    txn["user_amt_zscore"].clip(0, 10) * 3.0

    +

    txn["hour_risk_score"] * 0.2

    +

    txn["is_new_device_high_amount"] * 15

    +

    txn["merchant_refund_rate"] * 0.8

    +

    txn["category_risk_score"] * 0.1

    +

    txn["is_outside_typical_hour"] * 5

    +

    (txn["days_since_last_txn"] > 60).astype(int) * 10

).clip(0, 100).round(2)

txn["risk_level"] = pd.cut(
    txn["fraud_score"],
    bins=[0, 20, 40, 70, 100],
    labels=[
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]
)

print(
    txn[
        [
            "fraud_score",
            "risk_level"
        ]
    ].head(20)
)

print(
    txn["risk_level"]
    .value_counts()
)

txn.to_sql(
    "upi_txn_features",
    engine,
    if_exists="replace",
    index=False
)
print("Feature engineered dataset saved.")
import pandas as pd
import matplotlib.pyplot as plt

txn = pd.read_csv("data/upi_txn_features.csv")

hourly = (
    txn.groupby("txn_hour")
       .agg(
            total=("txn_id", "count"),
            fraud=("is_fraud", "sum")
       )
       .reset_index()
)

hourly["fraud_rate"] = (
    hourly["fraud"] / hourly["total"]
) * 100

print(hourly.head())

plt.figure(figsize=(12,5))

plt.bar(
    hourly["txn_hour"],
    hourly["fraud_rate"]
)

plt.title("Fraud Rate by Hour")
plt.xlabel("Hour")
plt.ylabel("Fraud Rate %")

plt.tight_layout()

plt.savefig(
    "outputs/fraud_by_hour.png"
)

plt.show()

plt.figure(figsize=(12,5))

plt.hist(
    txn["fraud_score"],
    bins=30
)

plt.title("Fraud Score Distribution")
plt.xlabel("Fraud Score")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "outputs/fraud_score_dist.png"
)

plt.show()

risk_counts = (
    txn["risk_level"]
    .value_counts()
)

plt.figure(figsize=(8,5))

plt.bar(
    risk_counts.index.astype(str),
    risk_counts.values
)

plt.title("Risk Level Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Transaction Count")

plt.tight_layout()

plt.savefig(
    "outputs/risk_level_distribution.png"
)

plt.show()
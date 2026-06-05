import pandas as pd
import random
from faker import Faker
from db_connection import engine

fake = Faker('en_IN')

NUM_MERCHANTS = 300

CATEGORIES = [
    'FOOD',
    'RETAIL',
    'FUEL',
    'TRAVEL',
    'GAMING',
    'CRYPTO_EXCHANGE'
]

CITIES = [
    'Chennai',
    'Mumbai',
    'Delhi',
    'Bangalore',
    'Hyderabad',
    'Pune',
    'Kolkata'
]

merchants = []

for i in range(NUM_MERCHANTS):

    category = random.choice(CATEGORIES)

    refund_rate = round(
        random.uniform(5, 15)
        if category in ['GAMING', 'CRYPTO_EXCHANGE']
        else random.uniform(0.1, 4),
        2
    )

    merchants.append({
        'merchant_id': f'MRC-{i+1:04d}',
        'merchant_name': fake.company(),
        'category': category,
        'city': random.choice(CITIES),
        'registration_days': random.randint(7, 2000),
        'avg_txn_count_daily': random.randint(5, 500),
        'refund_rate_pct': refund_rate,
        'chargeback_count': random.randint(0, 50),
        'merchant_risk_flag':
            'HIGH' if refund_rate > 10
            else 'MEDIUM' if refund_rate > 4
            else 'LOW'
    })

merchant_df = pd.DataFrame(merchants)

merchant_df.to_sql(
    "merchants_profiles",
    engine,
    if_exists="replace",
    index=False
)

print(merchant_df.head())
print("Merchant Profiles Created")
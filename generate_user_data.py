import pandas as pd
import random
from faker import Faker
from datetime import date
from db_connection import engine

fake = Faker('en_IN')

NUM_USERS = 500

CITIES = [
    'Chennai',
    'Mumbai',
    'Delhi',
    'Bangalore',
    'Hyderabad',
    'Pune',
    'Kolkata'
]

users = []

for i in range(NUM_USERS):
    users.append({
        'user_id': f'USR-{i+1:04d}',
        'user_name': fake.name(),
        'city': random.choice(CITIES),
        'account_age_days': random.randint(30, 1800),
        'avg_monthly_txn_amt': round(random.uniform(500, 50000), 2),
        'typical_hour_min': random.randint(7, 10),
        'typical_hour_max': random.randint(20, 23),
        'risk_tier': random.choice(['LOW', 'MEDIUM', 'HIGH']),
        'last_txn_date': fake.date_between(start_date=date(2023, 1, 1),end_date=date(2023, 3, 31))
    })

users_df = pd.DataFrame(users)

users_df.to_sql(
    "user_profiles1",
    engine,
    if_exists="replace",
    index=False
)

print("user_profiles loaded to PostgreSQL")
import pandas as pd
import numpy as np
from faker import Faker

print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)

fake = Faker()
print("Sample Name:", fake.name())

print("Setup Successful!")
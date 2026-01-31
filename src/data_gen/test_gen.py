from faker import Faker
import pandas as pd
import random
from pathlib import Path

fake = Faker()

def generate_dummy_data(num_rows=10):
    data = []
    for _ in range(num_rows):
        data.append({
            "company_id": f"MSME_{random.randint(100, 105)}",
            "date": fake.date_between(start_date='-1y', end_date='today'),
            "amount": round(random.uniform(100, 5000), 2),
            "mode": random.choice(['UPI', 'GST_CHALLAN', 'UTILITY_BILL'])
        })
    return pd.DataFrame(data)

# Test it
df = generate_dummy_data()
print(df.head())
# Save it so Member 3 can try loading it
output_file = Path("data/raw/dummy_week1.csv")
output_file.parent.mkdir(parents=True, exist_ok=True) # Creates data/raw/
df.to_csv(output_file, index=False)
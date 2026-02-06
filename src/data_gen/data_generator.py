import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()


def generate_msme_data(num_companies=10, days=90):
    """
    Generates a synthetic transaction log for 'num_companies' over 'days'.
    """
    data = []

    # Define Transaction Types based on Problem Statement
    txn_types = [
        'UPI_COLLECTION',  # Revenue (High frequency, low value)
        'UPI_PAYMENT',  # Expense
        'GST_PAYMENT',  # Compliance Signal (Monthly)
        'UTILITY_BILL',  # Stability Signal (Monthly)
        'VENDOR_PAYOUT'  # Expense
    ]

    for company_id in range(101, 101 + num_companies):
        current_date = datetime.now() - timedelta(days=days)

        # Give each company a "base revenue" to make them different
        base_revenue = random.randint(5000, 50000)

        for day in range(days):
            date_str = (current_date + timedelta(days=day)).strftime('%Y-%m-%d')

            # 1. Simulate Daily UPI Traffic (High Velocity)
            # Random number of transactions per day (0 to 10)
            num_txns = random.randint(0, 10)

            for _ in range(num_txns):
                txn_amount = round(np.random.normal(base_revenue / 50, 200), 2)  # Normal distribution
                if txn_amount < 10: txn_amount = 10  # Floor value

                data.append({
                    "company_id": f"MSME_{company_id}",
                    "date": date_str,
                    "txn_type": "UPI_COLLECTION",
                    "amount": abs(txn_amount),
                    "direction": "CREDIT",
                    "description": "Customer Payment via QR"
                })

            # 2. Simulate Monthly Events (GST/Utility)
            # If it's the 1st of the month, pay Utility Bill
            if (current_date + timedelta(days=day)).day == 1:
                data.append({
                    "company_id": f"MSME_{company_id}",
                    "date": date_str,
                    "txn_type": "UTILITY_BILL",
                    "amount": random.uniform(2000, 8000),
                    "direction": "DEBIT",
                    "description": "Electricity Bill Payment"
                })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating synthetic MSME data...")
    df = generate_msme_data(num_companies=5, days=60)

    # 1. Get the folder where THIS script lives
    # Result: .../msme-momentum-credit-score/src/data_gen
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Create the path INSIDE the current folder (src/data_gen/data/raw)
    # We removed the "..", ".." so it no longer goes up to the root
    output_dir = os.path.join(current_script_dir, "data", "raw")

    # 3. FORCE CREATE the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # 4. Save the file
    output_path = os.path.join(output_dir, "synthetic_transactions_v1.csv")
    df.to_csv(output_path, index=False)

    # Use normpath to print a clean, readable path
    print(f"Success! Data saved to: {os.path.normpath(output_path)}")
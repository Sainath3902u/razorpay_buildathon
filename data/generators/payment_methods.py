import numpy as np
import pandas as pd
from config import NUM_PAYMENT_METHODS, BANKS, RANDOM_SEED

def generate_payment_methods(df_customers):
    np.random.seed(RANDOM_SEED)
    pm_ids = [f"PM{i:05d}" for i in range(1, NUM_PAYMENT_METHODS + 1)]
    
    assigned_customers = np.random.choice(df_customers["customer_id"], size=NUM_PAYMENT_METHODS)
    banks = np.random.choice(BANKS, size=NUM_PAYMENT_METHODS, p=[0.32, 0.24, 0.18, 0.14, 0.08, 0.04])
    methods = np.random.choice(["UPI", "CARD", "NETBANKING", "MANDATE"], size=NUM_PAYMENT_METHODS, p=[0.45, 0.35, 0.12, 0.08])
    
    # Expiry distribution relative to Reference Date (2026-08-31)
    # Scenario 7: Some expired, some in 1-7d, 8-30d, 1-6m, >6m
    expiries = []
    for _ in range(NUM_PAYMENT_METHODS):
        r = np.random.rand()
        if r < 0.05:  # Expired (2026-07-01 to 2026-08-25)
            expiries.append(pd.Timestamp("2026-08-01") + pd.Timedelta(days=int(np.random.randint(-40, -1))))
        elif r < 0.12:  # 1-7 days (2026-09-01 to 2026-09-07)
            expiries.append(pd.Timestamp("2026-08-31") + pd.Timedelta(days=int(np.random.randint(1, 8))))
        elif r < 0.25:  # 8-30 days
            expiries.append(pd.Timestamp("2026-08-31") + pd.Timedelta(days=int(np.random.randint(8, 31))))
        elif r < 0.50:  # 1-6 months
            expiries.append(pd.Timestamp("2026-08-31") + pd.Timedelta(days=int(np.random.randint(31, 180))))
        else:  # Long validity
            expiries.append(pd.Timestamp("2026-08-31") + pd.Timedelta(days=int(np.random.randint(181, 1000))))
            
    return pd.DataFrame({
        "payment_method_id": pm_ids,
        "customer_id": assigned_customers,
        "bank": banks,
        "payment_method": methods,
        "payment_method_expiry": [d.strftime("%Y-%m-%d") for d in expiries]
    })
import numpy as np
import pandas as pd
from config import NUM_SUBSCRIPTIONS, RANDOM_SEED

def generate_subscriptions(df_customers, df_pm):
    np.random.seed(RANDOM_SEED)
    sub_ids = [f"S{i:05d}" for i in range(1, NUM_SUBSCRIPTIONS + 1)]
    
    assigned_customers = np.random.choice(df_customers["customer_id"], size=NUM_SUBSCRIPTIONS)
    amounts = np.random.choice([299.0, 499.0, 999.0, 1499.0, 2999.0, 9999.0, 24999.0], 
                               size=NUM_SUBSCRIPTIONS, p=[0.25, 0.30, 0.20, 0.10, 0.08, 0.05, 0.02])
    
    # Dates between 2026-08-01 and 2026-09-30
    renewal_dates = [
        (pd.Timestamp("2026-08-01") + pd.Timedelta(days=int(np.random.randint(0, 60)))).strftime("%Y-%m-%d")
        for _ in range(NUM_SUBSCRIPTIONS)
    ]
    
    statuses = np.random.choice(["ACTIVE", "PAST_DUE", "CANCELLED", "PAUSED"], size=NUM_SUBSCRIPTIONS, p=[0.80, 0.12, 0.05, 0.03])
    
    return pd.DataFrame({
        "subscription_id": sub_ids,
        "customer_id": assigned_customers,
        "subscription_amount": amounts,
        "subscription_status": statuses,
        "renewal_date": renewal_dates
    })
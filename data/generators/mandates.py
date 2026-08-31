import numpy as np
import pandas as pd
from config import NUM_MANDATES, RANDOM_SEED

def generate_mandates(df_customers):
    np.random.seed(RANDOM_SEED)
    mandate_ids = [f"M{i:05d}" for i in range(1, NUM_MANDATES + 1)]
    assigned_customers = np.random.choice(df_customers["customer_id"], size=NUM_MANDATES)
    statuses = np.random.choice(["ACTIVE", "FAILED", "SUSPENDED"], size=NUM_MANDATES, p=[0.82, 0.12, 0.06])
    
    # Retries for failed/suspended
    retries = []
    for s in statuses:
        if s == "ACTIVE":
            retries.append(0)
        else:
            retries.append(int(np.random.choice([0, 1, 2, 3], p=[0.3, 0.4, 0.2, 0.1])))
            
    return pd.DataFrame({
        "mandate_id": mandate_ids,
        "customer_id": assigned_customers,
        "mandate_status": statuses,
        "retry_count": retries
    })
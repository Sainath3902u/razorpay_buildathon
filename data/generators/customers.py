import numpy as np
import pandas as pd
from config import NUM_CUSTOMERS, RANDOM_SEED

def generate_customers():
    np.random.seed(RANDOM_SEED)
    customer_ids = [f"C{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)]
    
    # 70% Retail, 20% Prosumer, 10% B2B/Enterprise
    segments = np.random.choice(["RETAIL", "PROSUMER", "ENTERPRISE"], size=NUM_CUSTOMERS, p=[0.70, 0.20, 0.10])
    
    # Base baseline spend affinity
    spend_multipliers = []
    for seg in segments:
        if seg == "RETAIL":
            spend_multipliers.append(np.random.uniform(0.5, 2.0))
        elif seg == "PROSUMER":
            spend_multipliers.append(np.random.uniform(2.0, 8.0))
        else:
            spend_multipliers.append(np.random.uniform(10.0, 50.0))
            
    df_customers = pd.DataFrame({
        "customer_id": customer_ids,
        "segment": segments,
        "spend_multiplier": spend_multipliers
    })
    return df_customers
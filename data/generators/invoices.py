import numpy as np
import pandas as pd
from config import NUM_INVOICES, RANDOM_SEED

def generate_invoices(df_customers):
    np.random.seed(RANDOM_SEED)
    inv_ids = [f"INV{i:05d}" for i in range(1, NUM_INVOICES + 1)]
    
    enterprise_custs = df_customers[df_customers["segment"] == "ENTERPRISE"]["customer_id"].values
    if len(enterprise_custs) == 0:
        enterprise_custs = df_customers["customer_id"].values
        
    assigned_customers = np.random.choice(enterprise_custs, size=NUM_INVOICES)
    amounts = np.random.choice(
        [25000.0, 50000.0, 120000.0, 250000.0, 500000.0, 1200000.0, 4500000.0],
        size=NUM_INVOICES, p=[0.25, 0.30, 0.20, 0.12, 0.08, 0.04, 0.01]
    )
    
    # Due dates spread from 90 days ago to 30 days ahead
    due_dates = [
        (pd.Timestamp("2026-08-31") + pd.Timedelta(days=int(np.random.randint(-90, 31)))).strftime("%Y-%m-%d")
        for _ in range(NUM_INVOICES)
    ]
    
    # Status calculation relative to reference date (2026-08-31)
    statuses = []
    for d in due_dates:
        due_dt = pd.Timestamp(d)
        if due_dt > pd.Timestamp("2026-08-31"):
            statuses.append(np.random.choice(["ISSUED", "PAID"], p=[0.7, 0.3]))
        else:
            days_overdue = (pd.Timestamp("2026-08-31") - due_dt).days
            if days_overdue < 15:
                statuses.append(np.random.choice(["PAID", "OVERDUE"], p=[0.75, 0.25]))
            elif days_overdue < 45:
                statuses.append(np.random.choice(["PAID", "OVERDUE"], p=[0.55, 0.45]))
            else:
                statuses.append(np.random.choice(["PAID", "OVERDUE"], p=[0.30, 0.70]))
                
    return pd.DataFrame({
        "invoice_id": inv_ids,
        "customer_id": assigned_customers,
        "invoice_amount": amounts,
        "invoice_due_date": due_dates,
        "invoice_status": statuses
    })
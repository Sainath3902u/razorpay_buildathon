import numpy as np
import pandas as pd
from config import NUM_TRANSACTIONS, RANDOM_SEED, TIMELINE_START, TIMELINE_END

def generate_master_transactions(df_customers, df_products, df_pm, df_subs, df_inv, df_mandates):
    np.random.seed(RANDOM_SEED)
    
    tx_ids = [f"T{i:06d}" for i in range(1, NUM_TRANSACTIONS + 1)]
    order_ids = [f"O{(i % 30000) + 1:06d}" for i in range(NUM_TRANSACTIONS)]
    
    # 1. Temporal distribution across timeline
    start_ts = int(pd.Timestamp(TIMELINE_START).timestamp())
    end_ts = int(pd.Timestamp(TIMELINE_END).timestamp())
    random_timestamps = np.random.randint(start_ts, end_ts, size=NUM_TRANSACTIONS)
    random_timestamps.sort()
    timestamps = [pd.to_datetime(ts, unit='s').strftime("%Y-%m-%dT%H:%M:%S") for ts in random_timestamps]
    
    # 2. Assign customers weighted by spend multiplier
    cust_weights = df_customers["spend_multiplier"].values / df_customers["spend_multiplier"].sum()
    assigned_custs = np.random.choice(df_customers["customer_id"].values, size=NUM_TRANSACTIONS, p=cust_weights)
    
    # 3. Fast de-duplicated entity lookup maps (taking the latest record per customer)
    pm_dedup = df_pm.drop_duplicates(subset=["customer_id"], keep="last").set_index("customer_id").to_dict(orient="index")
    subs_dedup = df_subs.drop_duplicates(subset=["customer_id"], keep="last").set_index("customer_id").to_dict(orient="index")
    inv_dedup = df_inv.drop_duplicates(subset=["customer_id"], keep="last").set_index("customer_id").to_dict(orient="index")
    mand_dedup = df_mandates.drop_duplicates(subset=["customer_id"], keep="last").set_index("customer_id").to_dict(orient="index")
    
    p_lookup = df_products.set_index("product_id").to_dict(orient="index")
    all_pids = df_products["product_id"].values
    
    # 4. Pre-allocate arrays
    banks = []
    p_methods = []
    pm_ids = []
    pm_expiries = []
    prod_ids = []
    categories = []
    prices = []
    
    sub_ids, sub_statuses, sub_amounts, renewal_dates = [], [], [], []
    inv_ids, inv_amounts, inv_due_dates, inv_statuses = [], [], [], []
    mand_ids, mand_statuses, retry_counts = [], [], []
    
    # Default fallback instrument
    default_pm = {
        "bank": "HDFC_BANK",
        "payment_method": "UPI",
        "payment_method_id": "PM00001",
        "payment_method_expiry": "2027-12-31"
    }

    # 5. Populate rows
    for c in assigned_custs:
        # Payment Method
        pm_info = pm_dedup.get(c, default_pm)
        banks.append(pm_info["bank"])
        p_methods.append(pm_info["payment_method"])
        pm_ids.append(pm_info["payment_method_id"])
        pm_expiries.append(pm_info["payment_method_expiry"])
        
        # Product selection with latent basket probability
        r_prod = np.random.rand()
        if r_prod < 0.08:
            pid = "P00001"
        elif r_prod < 0.14:
            pid = "P00002"
        elif r_prod < 0.20:
            pid = "P00003"
        else:
            pid = np.random.choice(all_pids)
            
        prod_ids.append(pid)
        categories.append(p_lookup[pid]["product_category"])
        prices.append(p_lookup[pid]["product_price"])
        
        # Subscriptions
        if c in subs_dedup and np.random.rand() < 0.35:
            s = subs_dedup[c]
            sub_ids.append(s["subscription_id"])
            sub_statuses.append(s["subscription_status"])
            sub_amounts.append(s["subscription_amount"])
            renewal_dates.append(s["renewal_date"])
        else:
            sub_ids.append(None)
            sub_statuses.append(None)
            sub_amounts.append(None)
            renewal_dates.append(None)
            
        # Invoices
        if c in inv_dedup and np.random.rand() < 0.20:
            inv = inv_dedup[c]
            inv_ids.append(inv["invoice_id"])
            inv_amounts.append(inv["invoice_amount"])
            inv_due_dates.append(inv["invoice_due_date"])
            inv_statuses.append(inv["invoice_status"])
        else:
            inv_ids.append(None)
            inv_amounts.append(None)
            inv_due_dates.append(None)
            inv_statuses.append(None)
            
        # Mandates
        if c in mand_dedup and np.random.rand() < 0.25:
            m = mand_dedup[c]
            mand_ids.append(m["mandate_id"])
            mand_statuses.append(m["mandate_status"])
            retry_counts.append(m["retry_count"])
        else:
            mand_ids.append(None)
            mand_statuses.append(None)
            retry_counts.append(None)

    # 6. Statuses and financials
    quantities = np.random.choice([1, 1, 2], size=NUM_TRANSACTIONS, p=[0.80, 0.15, 0.05])
    amounts = np.array(prices, dtype=float) * quantities
    cart_values = np.round(amounts * np.random.uniform(1.0, 1.25, size=NUM_TRANSACTIONS), 2)
    
    statuses = np.random.choice(["SUCCESS", "FAILED", "PENDING"], size=NUM_TRANSACTIONS, p=[0.89, 0.08, 0.03])
    failure_reasons = [
        np.random.choice(["insufficient_funds", "timeout", "network_error", "card_expired"]) if s == "FAILED" else None
        for s in statuses
    ]

    # 7. Assemble DataFrame
    df_master = pd.DataFrame({
        "customer_id": assigned_custs,
        "transaction_id": tx_ids,
        "order_id": order_ids,
        "timestamp": timestamps,
        "amount": amounts,
        "transaction_status": statuses,
        "payment_method": p_methods,
        "bank": banks,
        "failure_reason": failure_reasons,
        "checkout_started": [True] * NUM_TRANSACTIONS,
        "checkout_completed": [s == "SUCCESS" for s in statuses],
        "cart_value": cart_values,
        "subscription_id": sub_ids,
        "subscription_status": sub_statuses,
        "subscription_amount": sub_amounts,
        "renewal_date": renewal_dates,
        "invoice_id": inv_ids,
        "invoice_amount": inv_amounts,
        "invoice_due_date": inv_due_dates,
        "invoice_status": inv_statuses,
        "mandate_id": mand_ids,
        "mandate_status": mand_statuses,
        "retry_count": retry_counts,
        "payment_method_id": pm_ids,
        "payment_method_expiry": pm_expiries,
        "product_id": prod_ids,
        "product_category": categories,
        "product_price": prices,
        "promise_date": [None] * NUM_TRANSACTIONS,
        "promise_status": [None] * NUM_TRANSACTIONS
    })
    
    return df_master
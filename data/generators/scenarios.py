import json
import os
import numpy as np
import pandas as pd
from config import RANDOM_SEED, REFERENCE_DATE

def inject_all_scenarios(df_all, df_customers, df_products, df_pm, df_subs, df_inv, df_mandates):
    np.random.seed(RANDOM_SEED)
    ground_truth = []
    
    # ----------------------------------------------------
    # SCENARIO 1: Payment Degradation (Bank + UPI)
    # ----------------------------------------------------
    deg_start = "2026-03-10T14:00:00"
    deg_end = "2026-03-12T18:00:00"
    deg_bank = "HDFC_BANK"
    deg_method = "UPI"
    
    mask_s1 = (
        (df_all["timestamp"] >= deg_start) & 
        (df_all["timestamp"] <= deg_end) & 
        (df_all["bank"] == deg_bank) & 
        (df_all["payment_method"] == deg_method)
    )
    
    affected_s1_tx = []
    for idx in df_all[mask_s1].index:
        # Increase failure probability to ~11.5% from 2.5%
        if np.random.rand() < 0.09 and df_all.at[idx, "transaction_status"] == "SUCCESS":
            df_all.at[idx, "transaction_status"] = "FAILED"
            df_all.at[idx, "failure_reason"] = np.random.choice(["timeout", "provider_error", "bank_unavailable"])
            affected_s1_tx.append(df_all.at[idx, "transaction_id"])
            
    ground_truth.append({
        "scenario_id": "RECOVER_01_PAYMENT_DEGRADATION",
        "type": "RECOVER",
        "affected_bank": deg_bank,
        "affected_method": deg_method,
        "time_window": {"start": deg_start, "end": deg_end},
        "injected_failure_count": len(affected_s1_tx),
        "expected_root_cause": "temporary_provider_degradation"
    })
    
    # ----------------------------------------------------
    # SCENARIO 2 & 8: High-Value Checkout Abandonment
    # ----------------------------------------------------
    high_val_drops = []
    for idx in df_all.sample(n=3500, random_state=RANDOM_SEED).index:
        if df_all.at[idx, "cart_value"] is not None and not np.isnan(df_all.at[idx, "cart_value"]):
            c_val = df_all.at[idx, "cart_value"]
            if c_val > 50000.0 and np.random.rand() < 0.45:
                df_all.at[idx, "checkout_started"] = True
                df_all.at[idx, "checkout_completed"] = False
                df_all.at[idx, "transaction_status"] = "PENDING"
                high_val_drops.append({
                    "transaction_id": df_all.at[idx, "transaction_id"],
                    "customer_id": df_all.at[idx, "customer_id"],
                    "cart_value": float(c_val)
                })
                
    ground_truth.append({
        "scenario_id": "RECOVER_02_08_HIGH_VALUE_ABANDONMENT",
        "type": "RECOVER",
        "affected_records_count": len(high_val_drops),
        "total_abandoned_pipeline": float(sum(x["cart_value"] for x in high_val_drops))
    })

    # ----------------------------------------------------
    # SCENARIO 3: Failed Subscription Recovery
    # ----------------------------------------------------
    failed_subs = []
    for idx in df_all[df_all["subscription_id"].notnull()].index:
        sub_id = df_all.at[idx, "subscription_id"]
        r_date = df_all.at[idx, "renewal_date"]
        if r_date and r_date <= "2026-08-31" and np.random.rand() < 0.15:
            df_all.at[idx, "transaction_status"] = "FAILED"
            df_all.at[idx, "failure_reason"] = np.random.choice(["insufficient_funds", "network_error"])
            df_all.at[idx, "subscription_status"] = "PAST_DUE"
            failed_subs.append(sub_id)
            
    ground_truth.append({
        "scenario_id": "RECOVER_03_FAILED_SUBSCRIPTIONS",
        "type": "RECOVER",
        "affected_subscriptions": list(set(failed_subs)),
        "recoverable_count": len(set(failed_subs))
    })

    # ----------------------------------------------------
    # SCENARIO 4 & 6: B2B Receivables & Promise to Pay
    # ----------------------------------------------------
    broken_promises = []
    for idx in df_all[df_all["invoice_id"].notnull()].index:
        inv_stat = df_all.at[idx, "invoice_status"]
        if inv_stat == "OVERDUE":
            p_rand = np.random.rand()
            if p_rand < 0.40:
                # Past promise date -> broken promise
                df_all.at[idx, "promise_date"] = "2026-08-15"
                df_all.at[idx, "promise_status"] = "UNFULFILLED"
                broken_promises.append(df_all.at[idx, "invoice_id"])
            elif p_rand < 0.70:
                # Future promise date -> pending
                df_all.at[idx, "promise_date"] = "2026-09-10"
                df_all.at[idx, "promise_status"] = "PENDING"
                
    ground_truth.append({
        "scenario_id": "RECOVER_04_06_B2B_RECEIVABLES_BROKEN_PROMISES",
        "type": "RECOVER",
        "broken_promises_count": len(set(broken_promises)),
        "invoices_affected": list(set(broken_promises))[:50]
    })

    # ----------------------------------------------------
    # SCENARIO 5: Mandate Retries Stopping Rule
    # ----------------------------------------------------
    exhausted_mandates = []
    for idx in df_all[df_all["mandate_id"].notnull()].index:
        if df_all.at[idx, "retry_count"] >= 2 and np.random.rand() < 0.70:
            df_all.at[idx, "transaction_status"] = "FAILED"
            df_all.at[idx, "failure_reason"] = "limit_exceeded"
            df_all.at[idx, "mandate_status"] = "SUSPENDED"
            exhausted_mandates.append(df_all.at[idx, "mandate_id"])
            
    ground_truth.append({
        "scenario_id": "RECOVER_05_MANDATE_STOPPING_RULE",
        "type": "RECOVER",
        "description": "Mandates with >=2 retries showing structural decline requiring hard stop",
        "exhausted_mandates_count": len(set(exhausted_mandates))
    })

    # ----------------------------------------------------
    # SCENARIO 7: Payment Method Expiry Pre-Dunning
    # ----------------------------------------------------
    expiring_at_risk = []
    for idx in df_all[df_all["subscription_id"].notnull()].index:
        pm_exp = df_all.at[idx, "payment_method_expiry"]
        ren_dt = df_all.at[idx, "renewal_date"]
        if pm_exp and ren_dt and pm_exp <= "2026-09-15" and ren_dt >= "2026-09-01":
            expiring_at_risk.append({
                "customer_id": df_all.at[idx, "customer_id"],
                "subscription_id": df_all.at[idx, "subscription_id"],
                "payment_method_id": df_all.at[idx, "payment_method_id"],
                "expiry": pm_exp,
                "renewal_date": ren_dt
            })
            
    ground_truth.append({
        "scenario_id": "RECOVER_07_PRE_DUNNING_EXPIRY",
        "type": "RECOVER",
        "at_risk_renewals_count": len(expiring_at_risk)
    })

    # ----------------------------------------------------
    # PREVENT 1: Churn Risk Cohort
    # ----------------------------------------------------
    churn_cohort = df_customers.sample(n=350, random_state=RANDOM_SEED)["customer_id"].tolist()
    # Dampen recent activity for churn cohort (no purchases after 2026-05-01)
    churn_mask = (df_all["customer_id"].isin(churn_cohort)) & (df_all["timestamp"] > "2026-05-01T00:00:00")
    df_all.loc[churn_mask, "transaction_status"] = np.random.choice(["FAILED", "PENDING"], size=churn_mask.sum(), p=[0.7, 0.3])
    
    ground_truth.append({
        "scenario_id": "PREVENT_01_CUSTOMER_CHURN_COHORT",
        "type": "PREVENT",
        "target_customer_count": len(churn_cohort),
        "cohort_sample": churn_cohort[:20]
    })

    # ----------------------------------------------------
    # PREVENT 2: Future Renewal Failures
    # ----------------------------------------------------
    risk_renewals = df_subs.sample(n=250, random_state=RANDOM_SEED)["subscription_id"].tolist()
    ground_truth.append({
        "scenario_id": "PREVENT_02_FUTURE_RENEWAL_FAILURE_RISK",
        "type": "PREVENT",
        "predicted_risk_subscriptions": risk_renewals[:25]
    })

    # ----------------------------------------------------
    # GROW 1: Cross-Sell Latent Affinity
    # ----------------------------------------------------
    ground_truth.append({
        "scenario_id": "GROW_01_CROSS_SELL_ASSOCIATION",
        "type": "GROW",
        "rules": [
            {"antecedent": "P00001 (Laptop)", "consequent": "P00002 (Laptop Bag)", "expected_lift": ">2.5"},
            {"antecedent": "P00001 (Laptop)", "consequent": "P00003 (Wireless Mouse)", "expected_lift": ">2.0"}
        ]
    })

    # ----------------------------------------------------
    # GROW 2: Upsell / Plan Upgrade
    # ----------------------------------------------------
    upsell_candidates = df_customers[df_customers["spend_multiplier"] > 3.5]["customer_id"].tolist()[:150]
    ground_truth.append({
        "scenario_id": "GROW_02_UPGRADE_CANDIDATES",
        "type": "GROW",
        "target_candidates_count": len(upsell_candidates),
        "candidate_sample": upsell_candidates[:15]
    })

    return df_all, ground_truth
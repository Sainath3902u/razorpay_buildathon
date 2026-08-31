import os
import json
import pandas as pd
from config import EXACT_COLUMNS
from customers import generate_customers
from products import generate_products
from payment_methods import generate_payment_methods
from subscriptions import generate_subscriptions
from invoices import generate_invoices
from mandates import generate_mandates
from orders import generate_master_transactions
from scenarios import inject_all_scenarios
from validate_dataset import generate_quality_report

def main():
    print("[1/6] Generating foundational entities...")
    os.makedirs("data/demo", exist_ok=True)
    os.makedirs("data/validation", exist_ok=True)
    
    df_customers = generate_customers()
    df_products = generate_products()
    df_pm = generate_payment_methods(df_customers)
    df_subs = generate_subscriptions(df_customers, df_pm)
    df_inv = generate_invoices(df_customers)
    df_mandates = generate_mandates(df_customers)

    print("[2/6] Assembling ~100,000 master transaction rows...")
    df_master = generate_master_transactions(df_customers, df_products, df_pm, df_subs, df_inv, df_mandates)

    print("[3/6] Injecting 8 Recovery + 2 Prevention + 2 Growth scenarios (latently)...")
    df_final, ground_truth = inject_all_scenarios(
        df_master, df_customers, df_products, df_pm, df_subs, df_inv, df_mandates
    )

    # Ensure EXACT column ordering and no auxiliary columns
    df_final = df_final[EXACT_COLUMNS]

    print("[4/6] Exporting master dataset CSV...")
    csv_out = "data/demo/merchant_revenue_data.csv"
    df_final.to_csv(csv_out, index=False)
    print(f"      -> Successfully saved: {csv_out} ({len(df_final):,} rows)")

    print("[5/6] Exporting isolated ground truth verification file...")
    gt_out = "data/validation/ground_truth.json"
    with open(gt_out, "w") as f:
        json.dump(ground_truth, f, indent=2)
    print(f"      -> Successfully saved: {gt_out}")

    print("[6/6] Generating data quality and validation report...")
    report_out = "data/validation/data_quality_report.json"
    generate_quality_report(df_final, report_out)
    print(f"      -> Successfully saved: {report_out}")
    print("\nDataset generation pipeline complete.")

if __name__ == "__main__":
    main()
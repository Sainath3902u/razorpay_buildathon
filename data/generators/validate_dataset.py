# import json
# import pandas as pd
# from config import EXACT_COLUMNS

# def generate_quality_report(df, output_path):
#     # Strict Schema Validation
#     assert list(df.columns) == EXACT_COLUMNS, f"Schema mismatch! Columns must be exactly {EXACT_COLUMNS}"
#     assert df["transaction_id"].is_unique, "Duplicate transaction IDs found!"
#     assert (df["amount"] >= 0).all(), "Negative amounts found!"

#     missing_percentages = (df.isnull().sum() / len(df) * 100).round(2).to_dict()
#     status_distribution = (df["transaction_status"].value_counts(normalize=True) * 100).round(2).to_dict()
#     pm_distribution = (df["payment_method"].value_counts(normalize=True) * 100).round(2).to_dict()

#     report = {
#         "dataset_summary": {
#             "total_rows": int(len(df)),
#             "unique_customers": int(df["customer_id"].nunique()),
#             "unique_transactions": int(df["transaction_id"].nunique()),
#             "unique_orders": int(df["order_id"].nunique()),
#             "unique_subscriptions": int(df["subscription_id"].dropna().nunique()),
#             "unique_invoices": int(df["invoice_id"].dropna().nunique()),
#             "unique_mandates": int(df["mandate_id"].dropna().nunique()),
#             "unique_payment_methods": int(df["payment_method_id"].dropna().nunique()),
#             "unique_products": int(df["product_id"].dropna().nunique()),
#             "date_range": {
#                 "start": str(df["timestamp"].min()),
#                 "end": str(df["timestamp"].max())
#             }
#         },
#         "financial_statistics": {
#             "total_transaction_volume": float(df["amount"].sum()),
#             "mean_transaction_amount": float(round(df["amount"].mean(), 2)),
#             "median_transaction_amount": float(round(df["amount"].median(), 2)),
#             "max_transaction_amount": float(df["amount"].max())
#         },
#         "distributions": {
#             "transaction_status_pct": status_distribution,
#             "payment_method_pct": pm_distribution
#         },
#         "missing_value_percentages": missing_percentages,
#         "integrity_checks": {
#             "no_duplicate_transaction_ids": bool(df["transaction_id"].is_unique),
#             "no_negative_amounts": bool((df["amount"] >= 0).all()),
#             "exact_columns_verified": True
#         }
#     }




import os
import json
import pandas as pd
from config import EXACT_COLUMNS

def generate_quality_report(df: pd.DataFrame, output_path: str = "data/validation/data_quality_report.json"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Strict Schema Validation
    assert list(df.columns) == EXACT_COLUMNS, f"Schema mismatch! Columns must be exactly {EXACT_COLUMNS}"
    assert df["transaction_id"].is_unique, "Duplicate transaction IDs found!"
    assert (df["amount"] >= 0).all(), "Negative amounts found!"

    missing_percentages = (df.isnull().sum() / len(df) * 100).round(2).to_dict()
    status_distribution = (df["transaction_status"].value_counts(normalize=True) * 100).round(2).to_dict()
    pm_distribution = (df["payment_method"].value_counts(normalize=True) * 100).round(2).to_dict()

    report = {
        "dataset_summary": {
            "total_rows": int(len(df)),
            "unique_customers": int(df["customer_id"].nunique()),
            "unique_transactions": int(df["transaction_id"].nunique()),
            "unique_orders": int(df["order_id"].nunique()),
            "unique_subscriptions": int(df["subscription_id"].dropna().nunique()),
            "unique_invoices": int(df["invoice_id"].dropna().nunique()),
            "unique_mandates": int(df["mandate_id"].dropna().nunique()),
            "unique_payment_methods": int(df["payment_method_id"].dropna().nunique()),
            "unique_products": int(df["product_id"].dropna().nunique()),
            "date_range": {
                "start": str(df["timestamp"].min()),
                "end": str(df["timestamp"].max())
            }
        },
        "financial_statistics": {
            "total_transaction_volume": float(df["amount"].sum()),
            "mean_transaction_amount": float(round(df["amount"].mean(), 2)),
            "median_transaction_amount": float(round(df["amount"].median(), 2)),
            "max_transaction_amount": float(df["amount"].max())
        },
        "distributions": {
            "transaction_status_pct": status_distribution,
            "payment_method_pct": pm_distribution
        },
        "missing_value_percentages": missing_percentages,
        "integrity_checks": {
            "no_duplicate_transaction_ids": bool(df["transaction_id"].is_unique),
            "no_negative_amounts": bool((df["amount"] >= 0).all()),
            "exact_columns_verified": True
        }
    }

    # 1. Write to JSON file
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    # 2. Print readable summary to console
    print("\n" + "=" * 50)
    print("           DATA QUALITY REPORT SUMMARY")
    print("=" * 50)
    print(f"Total Records           : {report['dataset_summary']['total_rows']:,}")
    print(f"Unique Customers        : {report['dataset_summary']['unique_customers']:,}")
    print(f"Unique Orders           : {report['dataset_summary']['unique_orders']:,}")
    print(f"Unique Subscriptions    : {report['dataset_summary']['unique_subscriptions']:,}")
    print(f"Unique Invoices         : {report['dataset_summary']['unique_invoices']:,}")
    print(f"Date Window             : {report['dataset_summary']['date_range']['start']} to {report['dataset_summary']['date_range']['end']}")
    print(f"Total Volume Processed  : ₹{report['financial_statistics']['total_transaction_volume']:,.2f}")
    print(f"Status Breakdown        : {report['distributions']['transaction_status_pct']}")
    print(f"Integrity Validations   : ALL PASSED (0 duplicates, 0 negative amounts)")
    print(f"Report Output Saved To  : {os.path.abspath(output_path)}")
    print("=" * 50 + "\n")

    return report

if __name__ == "__main__":
    csv_file = "data/demo/merchant_revenue_data.csv"
    if os.path.exists(csv_file):
        print(f"Reading dataset from {csv_file}...")
        df = pd.read_csv(csv_file)
        generate_quality_report(df)
    else:
        print(f"Error: {csv_file} not found. Run generate_all.py first.")
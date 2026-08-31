import pandas as pd


def normalize_dataset(df, mapping):

    rename_map = {
        original: canonical
        for canonical, original in mapping.items()
    }

    normalized = df.rename(columns=rename_map).copy()

    if "timestamp" in normalized.columns:
        normalized["timestamp"] = pd.to_datetime(
            normalized["timestamp"],
            errors="coerce"
        )

    if "amount" in normalized.columns:
        normalized["amount"] = pd.to_numeric(
            normalized["amount"],
            errors="coerce"
        )

    if "cart_value" in normalized.columns:
        normalized["cart_value"] = pd.to_numeric(
            normalized["cart_value"],
            errors="coerce"
        )

    if "subscription_amount" in normalized.columns:
        normalized["subscription_amount"] = pd.to_numeric(
            normalized["subscription_amount"],
            errors="coerce"
        )

    if "invoice_amount" in normalized.columns:
        normalized["invoice_amount"] = pd.to_numeric(
            normalized["invoice_amount"],
            errors="coerce"
        )

    return normalized
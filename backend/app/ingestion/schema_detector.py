def detect_schema(df):
    columns = {
        col.lower().strip()
        for col in df.columns
    }

    capabilities = {
        "payments": False,
        "checkout": False,
        "subscriptions": False,
        "receivables": False,
        "mandates": False,
        "payment_methods": False,
        "products": False,
        "promises": False,
    }

    if "transaction_status" in columns and "amount" in columns:
        capabilities["payments"] = True

    if (
        "checkout_started" in columns
        and "checkout_completed" in columns
    ):
        capabilities["checkout"] = True

    if (
        "subscription_id" in columns
        and "subscription_status" in columns
    ):
        capabilities["subscriptions"] = True

    if (
        "invoice_id" in columns
        and "invoice_status" in columns
    ):
        capabilities["receivables"] = True

    if (
        "mandate_id" in columns
        and "mandate_status" in columns
    ):
        capabilities["mandates"] = True

    if "payment_method_expiry" in columns:
        capabilities["payment_methods"] = True

    if (
        "product_id" in columns
        and "product_category" in columns
    ):
        capabilities["products"] = True

    if (
        "promise_date" in columns
        and "promise_status" in columns
    ):
        capabilities["promises"] = True

    return capabilities
COLUMN_ALIASES = {
    "customer_id": [
        "customer_id",
        "user_id",
        "userid",
        "client_id",
        "buyer_id"
    ],

    "transaction_id": [
        "transaction_id",
        "txn_id",
        "transactionid",
        "payment_id"
    ],

    "amount": [
        "amount",
        "txn_amt",
        "transaction_amount",
        "payment_amount"
    ],

    "timestamp": [
        "timestamp",
        "txn_time",
        "transaction_time",
        "date",
        "datetime"
    ],

    "transaction_status": [
        "transaction_status",
        "txn_status",
        "payment_status",
        "status"
    ],

    "payment_method": [
        "payment_method",
        "pay_type",
        "payment_type",
        "method"
    ],

    "bank": [
        "bank",
        "bank_name",
        "provider",
        "bank_provider"
    ],

    "failure_reason": [
        "failure_reason",
        "failure_type",
        "error_reason",
        "payment_error"
    ]
}


def normalize_column_name(column):
    return (
        column.lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
    )


def map_columns(df):
    original_columns = list(df.columns)

    normalized_lookup = {
        normalize_column_name(col): col
        for col in original_columns
    }

    mapping = {}

    for canonical, aliases in COLUMN_ALIASES.items():

        for alias in aliases:

            alias = normalize_column_name(alias)

            if alias in normalized_lookup:
                mapping[canonical] = normalized_lookup[alias]
                break

    return mapping
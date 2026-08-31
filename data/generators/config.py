import numpy as np

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Reference timeline anchors
TIMELINE_START = "2026-01-01T00:00:00"
TIMELINE_END = "2026-08-30T23:59:59"
REFERENCE_DATE = "2026-08-31T00:00:00"

NUM_CUSTOMERS = 5000
NUM_TRANSACTIONS = 100000
NUM_ORDERS = 30000
NUM_CHECKOUTS = 30000
NUM_SUBSCRIPTIONS = 3000
NUM_MANDATES = 3000
NUM_INVOICES = 10000
NUM_PAYMENT_METHODS = 5000
NUM_PRODUCTS = 500

BANKS = ["HDFC_BANK", "ICICI_BANK", "SBI", "AXIS_BANK", "KOTAK_BANK", "CITI_BANK"]
PAYMENT_METHODS = ["UPI", "CARD", "NETBANKING", "WALLET", "MANDATE"]
CATEGORIES = ["Electronics", "Accessories", "Software", "Cloud Services", "Office Supplies", "Hardware"]

FAILURE_REASONS = [
    "insufficient_funds",
    "timeout",
    "provider_error",
    "bank_unavailable",
    "network_error",
    "card_expired",
    "authentication_failed",
    "limit_exceeded"
]

EXACT_COLUMNS = [
    "customer_id",
    "transaction_id",
    "order_id",
    "timestamp",
    "amount",
    "transaction_status",
    "payment_method",
    "bank",
    "failure_reason",
    "checkout_started",
    "checkout_completed",
    "cart_value",
    "subscription_id",
    "subscription_status",
    "subscription_amount",
    "renewal_date",
    "invoice_id",
    "invoice_amount",
    "invoice_due_date",
    "invoice_status",
    "mandate_id",
    "mandate_status",
    "retry_count",
    "payment_method_id",
    "payment_method_expiry",
    "product_id",
    "product_category",
    "product_price",
    "promise_date",
    "promise_status"
]
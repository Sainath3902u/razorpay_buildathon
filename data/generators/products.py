import numpy as np
import pandas as pd
from config import NUM_PRODUCTS, CATEGORIES, RANDOM_SEED

def generate_products():
    np.random.seed(RANDOM_SEED)
    product_ids = [f"P{i:05d}" for i in range(1, NUM_PRODUCTS + 1)]
    
    # Catalog design for cross-sell scenarios
    categories = np.random.choice(CATEGORIES, size=NUM_PRODUCTS, p=[0.25, 0.30, 0.15, 0.10, 0.10, 0.10])
    prices = []
    
    for i, cat in enumerate(categories):
        if i == 0:  # Anchor Laptop
            prices.append(65000.0)
            categories[i] = "Electronics"
        elif i == 1:  # Laptop Bag
            prices.append(2499.0)
            categories[i] = "Accessories"
        elif i == 2:  # Wireless Mouse
            prices.append(1299.0)
            categories[i] = "Accessories"
        elif cat == "Electronics":
            prices.append(float(np.random.choice([15000, 25000, 45000, 85000, 120000])))
        elif cat == "Accessories":
            prices.append(float(np.random.choice([499, 999, 1499, 2999, 4999])))
        elif cat in ["Software", "Cloud Services"]:
            prices.append(float(np.random.choice([999, 2499, 4999, 14999, 29999])))
        else:
            prices.append(float(np.random.choice([299, 799, 1999, 5999])))
            
    return pd.DataFrame({
        "product_id": product_ids,
        "product_category": categories,
        "product_price": prices
    })
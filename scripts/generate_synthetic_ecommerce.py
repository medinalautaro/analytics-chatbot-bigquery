from __future__ import annotations

import math
import random
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ============================================================
# CONFIG
# ============================================================

SEED = 42
OUTPUT_DIR = Path("synthetic_ecommerce_data")

N_CUSTOMERS = 10_000
N_PRODUCTS = 500
N_ORDERS = 80_000

START_DATE = pd.Timestamp("2024-01-01")
END_DATE = pd.Timestamp("2025-12-31")

COUNTRIES = [
    ("US", 0.35),
    ("UK", 0.12),
    ("DE", 0.10),
    ("FR", 0.09),
    ("ES", 0.08),
    ("BR", 0.12),
    ("AR", 0.07),
    ("MX", 0.07),
]

CHANNELS = [
    ("organic", 0.35),
    ("paid_search", 0.20),
    ("email", 0.15),
    ("social", 0.18),
    ("referral", 0.07),
    ("affiliate", 0.05),
]

DEVICES = [
    ("mobile", 0.58),
    ("desktop", 0.34),
    ("tablet", 0.08),
]

PAYMENT_METHODS = [
    ("credit_card", 0.55),
    ("debit_card", 0.15),
    ("paypal", 0.17),
    ("bank_transfer", 0.08),
    ("gift_card", 0.05),
]

ORDER_STATUSES = [
    ("completed", 0.90),
    ("cancelled", 0.04),
    ("refunded", 0.03),
    ("partially_refunded", 0.03),
]

PAYMENT_STATUSES = [
    ("paid", 0.94),
    ("failed", 0.04),
    ("pending", 0.02),
]

CARRIERS = [
    ("DHL", 0.28),
    ("FedEx", 0.24),
    ("UPS", 0.22),
    ("LocalCarrier", 0.18),
    ("PostalService", 0.08),
]

PRODUCT_CATEGORIES = {
    "electronics": {
        "weight": 0.20,
        "price_mean": 4.4,
        "price_sigma": 0.45,
        "return_rate": 0.05,
    },
    "fashion": {
        "weight": 0.25,
        "price_mean": 3.5,
        "price_sigma": 0.40,
        "return_rate": 0.20,
    },
    "home": {
        "weight": 0.18,
        "price_mean": 3.8,
        "price_sigma": 0.42,
        "return_rate": 0.08,
    },
    "beauty": {
        "weight": 0.12,
        "price_mean": 3.2,
        "price_sigma": 0.35,
        "return_rate": 0.06,
    },
    "sports": {
        "weight": 0.10,
        "price_mean": 3.7,
        "price_sigma": 0.38,
        "return_rate": 0.09,
    },
    "books": {
        "weight": 0.08,
        "price_mean": 2.9,
        "price_sigma": 0.30,
        "return_rate": 0.03,
    },
    "toys": {
        "weight": 0.07,
        "price_mean": 3.1,
        "price_sigma": 0.33,
        "return_rate": 0.07,
    },
}

RETURN_REASONS = [
    ("damaged", 0.22),
    ("wrong_item", 0.12),
    ("not_as_described", 0.20),
    ("size_issue", 0.25),   # mostly fashion
    ("late_delivery", 0.10),
    ("changed_mind", 0.11),
]


# ============================================================
# UTILITIES
# ============================================================

def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def weighted_choice(items: list[tuple[str, float]]) -> str:
    labels = [x[0] for x in items]
    probs = [x[1] for x in items]
    return random.choices(labels, weights=probs, k=1)[0]


def weighted_choice_from_dict(weights_dict: dict[str, float]) -> str:
    labels = list(weights_dict.keys())
    probs = list(weights_dict.values())
    return random.choices(labels, weights=probs, k=1)[0]


def random_timestamp_between(start: pd.Timestamp, end: pd.Timestamp) -> pd.Timestamp:
    delta = int((end - start).total_seconds())
    offset = random.randint(0, delta)
    return start + pd.Timedelta(seconds=offset)


def clamp(x: float, low: float, high: float) -> float:
    return max(low, min(high, x))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def make_id(prefix: str, n: int, width: int = 6) -> str:
    return f"{prefix}_{n:0{width}d}"


def month_growth_factor(ts: pd.Timestamp) -> float:
    """
    Simulate business growth + seasonal effects.
    """
    # Growth from 2024 to 2025
    months_since_start = (ts.year - START_DATE.year) * 12 + (ts.month - START_DATE.month)
    growth = 1.0 + 0.018 * months_since_start  # gradual growth

    # Seasonality
    seasonal_map = {
        1: 0.92,
        2: 0.95,
        3: 0.98,
        4: 1.00,
        5: 1.02,
        6: 1.03,
        7: 1.01,
        8: 1.00,
        9: 1.04,
        10: 1.08,
        11: 1.18,
        12: 1.35,
    }
    return growth * seasonal_map[ts.month]


def hour_weight(hour: int) -> float:
    """
    More orders in afternoon/evening, fewer overnight.
    """
    if 0 <= hour <= 5:
        return 0.15
    if 6 <= hour <= 8:
        return 0.45
    if 9 <= hour <= 11:
        return 0.80
    if 12 <= hour <= 14:
        return 1.00
    if 15 <= hour <= 18:
        return 1.15
    if 19 <= hour <= 22:
        return 1.30
    return 0.75


def weekday_weight(weekday: int) -> float:
    """
    Monday=0 ... Sunday=6
    Slightly more activity on Friday/Saturday/Sunday.
    """
    mapping = {
        0: 0.95,
        1: 0.96,
        2: 1.00,
        3: 1.03,
        4: 1.08,
        5: 1.15,
        6: 1.10,
    }
    return mapping[weekday]


def sample_order_timestamp() -> pd.Timestamp:
    """
    Sample with temporal patterns by rejection sampling.
    """
    while True:
        ts = random_timestamp_between(START_DATE, END_DATE)
        weight = month_growth_factor(ts) * weekday_weight(ts.weekday()) * hour_weight(ts.hour)
        # Normalize roughly to 0..1.8 then compare
        prob = min(weight / 1.8, 0.98)
        if random.random() < prob:
            return ts


# ============================================================
# DATA GENERATION
# ============================================================

def generate_customers(n_customers: int) -> pd.DataFrame:
    rows = []
    for i in range(1, n_customers + 1):
        customer_id = make_id("cust", i)

        signup_date = random_timestamp_between(
            START_DATE - pd.Timedelta(days=180),
            END_DATE - pd.Timedelta(days=5)
        )

        country = weighted_choice(COUNTRIES)
        marketing_channel = weighted_choice(CHANNELS)
        device_type = weighted_choice(DEVICES)

        # Slightly more likely to become repeat buyers through email/referral
        if marketing_channel == "email":
            repeat_propensity = np.random.beta(4, 3)
        elif marketing_channel in {"referral", "organic"}:
            repeat_propensity = np.random.beta(3, 3)
        else:
            repeat_propensity = np.random.beta(2, 4)

        # Customer value tier
        value_score = np.random.lognormal(mean=0.0, sigma=0.8)

        rows.append(
            {
                "customer_id": customer_id,
                "signup_date": signup_date,
                "country": country,
                "marketing_channel": marketing_channel,
                "device_type": device_type,
                "repeat_propensity": round(float(repeat_propensity), 4),
                "value_score": round(float(value_score), 4),
            }
        )

    df = pd.DataFrame(rows)

    # Add a tiny bit of messy data for realism
    messy_idx = df.sample(frac=0.003, random_state=SEED).index
    df.loc[messy_idx[: len(messy_idx) // 2], "device_type"] = None
    df.loc[messy_idx[len(messy_idx) // 2 :], "marketing_channel"] = None

    return df


def generate_products(n_products: int) -> pd.DataFrame:
    category_weights = {k: v["weight"] for k, v in PRODUCT_CATEGORIES.items()}

    adjective_pool = [
        "Premium", "Classic", "Essential", "Smart", "Comfort", "Pro", "Ultra",
        "Eco", "Compact", "Modern", "Elite", "Lite", "Advanced", "Portable"
    ]
    noun_pool = {
        "electronics": ["Headphones", "Speaker", "Monitor", "Keyboard", "Mouse", "Tablet", "Camera"],
        "fashion": ["Jacket", "Sneakers", "Jeans", "T-Shirt", "Dress", "Backpack", "Boots"],
        "home": ["Lamp", "Chair", "Bedding", "Cookware", "Storage Box", "Desk", "Blender"],
        "beauty": ["Serum", "Moisturizer", "Lipstick", "Shampoo", "Conditioner", "Cleanser"],
        "sports": ["Yoga Mat", "Dumbbell", "Bottle", "Gloves", "Shorts", "Tracker"],
        "books": ["Novel", "Workbook", "Guide", "Manual", "Anthology", "Notebook"],
        "toys": ["Puzzle", "Figure", "Board Game", "Plush", "Blocks", "Car Set"],
    }

    rows = []
    for i in range(1, n_products + 1):
        product_id = make_id("prod", i)
        category = weighted_choice_from_dict(category_weights)

        category_cfg = PRODUCT_CATEGORIES[category]
        base_price = np.random.lognormal(
            mean=category_cfg["price_mean"],
            sigma=category_cfg["price_sigma"],
        )
        price = round(clamp(base_price, 5.0, 1200.0), 2)

        product_name = f"{random.choice(adjective_pool)} {random.choice(noun_pool[category])}"
        supplier = f"Supplier_{random.randint(1, 70):03d}"

        rows.append(
            {
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "price": price,
                "supplier": supplier,
                "base_return_rate": category_cfg["return_rate"],
            }
        )

    return pd.DataFrame(rows)


def compute_customer_order_weights(customers: pd.DataFrame) -> np.ndarray:
    """
    Create a long-tail ordering behavior.
    """
    repeat_propensity = customers["repeat_propensity"].fillna(customers["repeat_propensity"].median()).values
    value_score = customers["value_score"].values

    raw = 0.6 * repeat_propensity + 0.4 * (value_score / np.max(value_score))
    raw = np.power(raw + 0.03, 2.2)  # accentuate heavy buyers
    weights = raw / raw.sum()
    return weights


def choose_order_status(payment_status: str) -> str:
    if payment_status == "failed":
        return "cancelled"
    # Otherwise mostly completed, with some refunds later
    return weighted_choice(ORDER_STATUSES)


def choose_payment_status(channel: str, device: str) -> str:
    probs = dict(PAYMENT_STATUSES)

    # Slightly more failures on mobile/social traffic
    if device == "mobile":
        probs["failed"] += 0.01
        probs["paid"] -= 0.01
    if channel == "social":
        probs["failed"] += 0.01
        probs["paid"] -= 0.01

    labels = list(probs.keys())
    weights = list(probs.values())
    return random.choices(labels, weights=weights, k=1)[0]


def product_popularity_weights(products: pd.DataFrame) -> np.ndarray:
    """
    Long-tail product popularity.
    """
    n = len(products)
    ranks = np.arange(1, n + 1)
    weights = 1 / np.power(ranks, 0.75)
    weights = weights / weights.sum()

    shuffled_indices = np.random.permutation(n)
    final_weights = np.zeros(n)
    final_weights[shuffled_indices] = weights
    return final_weights


def choose_num_items(device_type: str, channel: str) -> int:
    base = np.random.poisson(2.2) + 1
    if device_type == "mobile":
        base -= 0.2
    if channel == "email":
        base += 0.3
    return max(1, min(int(round(base)), 8))


def choose_quantity(category: str) -> int:
    if category in {"books", "beauty", "toys"}:
        q = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.40, 0.18, 0.12, 0.16, 0.09, 0.05])
    elif category == "fashion":
        q = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.45, 0.15, 0.10, 0.18, 0.08, 0.04])
    else:
        q = np.random.choice([1, 1, 2, 2, 3], p=[0.46, 0.20, 0.20, 0.10, 0.04])
    return int(q)


def generate_orders_and_related(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    n_orders: int
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customer_weights = compute_customer_order_weights(customers)
    product_weights = product_popularity_weights(products)

    customer_lookup = customers.set_index("customer_id").to_dict("index")
    products_lookup = products.set_index("product_id").to_dict("index")
    product_ids = products["product_id"].tolist()

    orders_rows = []
    order_items_rows = []
    payments_rows = []
    shipments_rows = []
    returns_rows = []

    customer_ids = customers["customer_id"].tolist()

    order_item_counter = 1
    payment_counter = 1
    shipment_counter = 1
    return_counter = 1

    for order_num in range(1, n_orders + 1):
        order_id = make_id("ord", order_num)
        customer_id = np.random.choice(customer_ids, p=customer_weights)

        cust = customer_lookup[customer_id]

        order_timestamp = sample_order_timestamp()

        # Ensure customer signed up before placing order
        signup_date = pd.Timestamp(cust["signup_date"])
        if order_timestamp < signup_date:
            order_timestamp = signup_date + pd.Timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

        device_type = cust["device_type"] if pd.notna(cust["device_type"]) else weighted_choice(DEVICES)
        marketing_channel = cust["marketing_channel"] if pd.notna(cust["marketing_channel"]) else weighted_choice(CHANNELS)
        country = cust["country"]

        payment_method = weighted_choice(PAYMENT_METHODS)
        payment_status = choose_payment_status(marketing_channel, device_type)
        order_status = choose_order_status(payment_status)

        num_distinct_items = choose_num_items(device_type, marketing_channel)

        chosen_product_ids = np.random.choice(
            product_ids,
            size=num_distinct_items,
            replace=False if num_distinct_items <= len(product_ids) else True,
            p=product_weights,
        )

        order_subtotal = 0.0
        item_ids_for_return_consideration = []

        for pid in chosen_product_ids:
            prod = products_lookup[pid]
            quantity = choose_quantity(prod["category"])

            # Slight price noise / discount
            price_noise = np.random.normal(1.0, 0.06)
            unit_price = round(clamp(prod["price"] * price_noise, 1.0, 1500.0), 2)

            line_amount = round(unit_price * quantity, 2)
            order_subtotal += line_amount

            order_items_rows.append(
                {
                    "order_item_id": make_id("item", order_item_counter, width=7),
                    "order_id": order_id,
                    "product_id": pid,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_amount": line_amount,
                }
            )

            item_ids_for_return_consideration.append(
                (make_id("item", order_item_counter, width=7), prod, quantity, unit_price)
            )

            order_item_counter += 1

        # Shipping cost depends loosely on country + basket
        shipping_cost = round(clamp(4.0 + math.log1p(order_subtotal) * 1.7 + np.random.normal(0, 1.2), 2.0, 35.0), 2)
        total_amount = round(order_subtotal + shipping_cost, 2)

        payment_timestamp = order_timestamp + pd.Timedelta(minutes=random.randint(1, 180))

        if payment_status == "failed":
            paid_amount = 0.0
        elif payment_status == "pending":
            paid_amount = round(total_amount * np.random.uniform(0.5, 1.0), 2)
        else:
            paid_amount = total_amount

        payments_rows.append(
            {
                "payment_id": make_id("pay", payment_counter),
                "order_id": order_id,
                "payment_timestamp": payment_timestamp,
                "payment_status": payment_status,
                "payment_method": payment_method,
                "amount": paid_amount,
            }
        )
        payment_counter += 1

        shipment_timestamp = pd.NaT
        delivery_timestamp = pd.NaT
        carrier = None
        final_shipping_cost = None

        if order_status != "cancelled" and payment_status == "paid":
            shipment_timestamp = payment_timestamp + pd.Timedelta(hours=random.randint(4, 72))
            carrier = weighted_choice(CARRIERS)

            # Delivery delay distribution
            delay_days = max(1, int(np.random.gamma(shape=2.2, scale=1.4)))
            if random.random() < 0.05:
                delay_days += random.randint(5, 12)

            delivery_timestamp = shipment_timestamp + pd.Timedelta(days=delay_days, hours=random.randint(0, 12))
            final_shipping_cost = shipping_cost

            shipments_rows.append(
                {
                    "shipment_id": make_id("ship", shipment_counter),
                    "order_id": order_id,
                    "shipment_timestamp": shipment_timestamp,
                    "delivery_timestamp": delivery_timestamp,
                    "carrier": carrier,
                    "shipping_cost": final_shipping_cost,
                }
            )
            shipment_counter += 1

        # Generate returns only for delivered/fulfilled orders
        if pd.notna(delivery_timestamp):
            for item_id, prod, quantity, unit_price in item_ids_for_return_consideration:
                base_rr = prod["base_return_rate"]

                # Adjust return probability
                rr = base_rr
                if marketing_channel == "social":
                    rr += 0.01
                if device_type == "mobile":
                    rr += 0.005
                if prod["category"] == "fashion":
                    rr += 0.03
                rr = clamp(rr, 0.01, 0.35)

                if random.random() < rr:
                    return_qty = random.randint(1, quantity)
                    refund_amount = round(return_qty * unit_price, 2)
                    return_timestamp = delivery_timestamp + pd.Timedelta(days=random.randint(1, 30))

                    if prod["category"] == "fashion":
                        return_reason = random.choices(
                            ["size_issue", "changed_mind", "not_as_described", "damaged"],
                            weights=[0.45, 0.20, 0.20, 0.15],
                            k=1,
                        )[0]
                    else:
                        return_reason = weighted_choice(RETURN_REASONS)

                    returns_rows.append(
                        {
                            "return_id": make_id("ret", return_counter),
                            "order_item_id": item_id,
                            "return_timestamp": return_timestamp,
                            "return_reason": return_reason,
                            "refund_amount": refund_amount,
                            "return_quantity": return_qty,
                        }
                    )
                    return_counter += 1

        orders_rows.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_timestamp": order_timestamp,
                "order_status": order_status,
                "payment_method": payment_method,
                "country": country,
                "device_type": device_type,
                "marketing_channel": marketing_channel,
                "subtotal_amount": round(order_subtotal, 2),
                "shipping_amount": shipping_cost,
                "total_amount": total_amount,
            }
        )

        if order_num % 10_000 == 0:
            print(f"Generated {order_num:,} / {n_orders:,} orders...")

    orders_df = pd.DataFrame(orders_rows)
    order_items_df = pd.DataFrame(order_items_rows)
    payments_df = pd.DataFrame(payments_rows)
    shipments_df = pd.DataFrame(shipments_rows)
    returns_df = pd.DataFrame(returns_rows)

    return orders_df, order_items_df, payments_df, shipments_df, returns_df


def generate_marketing_spend(start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    rows = []
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    base_spend_by_channel = {
        "organic": 250,
        "paid_search": 2200,
        "email": 550,
        "social": 1400,
        "referral": 300,
        "affiliate": 450,
    }

    for d in dates:
        seasonal = month_growth_factor(d)
        weekend_boost = 1.08 if d.weekday() in (5, 6) else 1.0

        for channel, base_spend in base_spend_by_channel.items():
            noise = np.random.normal(1.0, 0.18)

            # Stronger spend around Nov/Dec for paid channels
            holiday_boost = 1.0
            if channel in {"paid_search", "social", "affiliate"} and d.month in (11, 12):
                holiday_boost = 1.20

            spend = max(0, base_spend * seasonal * weekend_boost * holiday_boost * noise)

            # Approximate funnel signals
            if channel == "organic":
                impressions = int(spend * np.random.uniform(40, 90))
                clicks = int(impressions * np.random.uniform(0.03, 0.08))
            elif channel == "email":
                impressions = int(spend * np.random.uniform(25, 60))
                clicks = int(impressions * np.random.uniform(0.06, 0.14))
            else:
                impressions = int(spend * np.random.uniform(18, 55))
                clicks = int(impressions * np.random.uniform(0.02, 0.07))

            rows.append(
                {
                    "date": d.normalize(),
                    "channel": channel,
                    "spend": round(float(spend), 2),
                    "impressions": impressions,
                    "clicks": clicks,
                }
            )

    return pd.DataFrame(rows)


# ============================================================
# QUALITY CHECKS
# ============================================================

def run_basic_checks(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    payments: pd.DataFrame,
    shipments: pd.DataFrame,
    returns: pd.DataFrame,
    marketing_spend: pd.DataFrame,
) -> None:
    print("\nRunning basic checks...")

    assert customers["customer_id"].is_unique
    assert products["product_id"].is_unique
    assert orders["order_id"].is_unique
    assert order_items["order_item_id"].is_unique
    assert payments["payment_id"].is_unique
    assert shipments["shipment_id"].is_unique
    assert returns["return_id"].is_unique

    assert order_items["order_id"].isin(orders["order_id"]).all()
    assert order_items["product_id"].isin(products["product_id"]).all()
    assert payments["order_id"].isin(orders["order_id"]).all()
    assert shipments["order_id"].isin(orders["order_id"]).all()
    assert returns["order_item_id"].isin(order_items["order_item_id"]).all()

    if not payments.empty:
        payments_join = payments.merge(
            orders[["order_id", "order_timestamp"]],
            on="order_id",
            how="left"
        )
        assert (payments_join["payment_timestamp"] >= payments_join["order_timestamp"]).all()

    if not shipments.empty:
        shipments_join = shipments.merge(
            payments[["order_id", "payment_timestamp"]],
            on="order_id",
            how="left"
        )
        assert (shipments_join["shipment_timestamp"] >= shipments_join["payment_timestamp"]).all()
        assert (shipments_join["delivery_timestamp"] >= shipments_join["shipment_timestamp"]).all()

    if not returns.empty:
        returns_join = returns.merge(
            order_items[["order_item_id", "line_amount"]],
            on="order_item_id",
            how="left"
        )
        assert (returns_join["refund_amount"] <= returns_join["line_amount"] + 1e-9).all()

    assert (marketing_spend["spend"] >= 0).all()
    assert (order_items["quantity"] >= 1).all()
    assert (order_items["unit_price"] > 0).all()

    print("All basic checks passed.")


def print_summary(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    payments: pd.DataFrame,
    shipments: pd.DataFrame,
    returns: pd.DataFrame,
    marketing_spend: pd.DataFrame,
) -> None:
    print("\n================ DATASET SUMMARY ================")
    print(f"Customers:        {len(customers):,}")
    print(f"Products:         {len(products):,}")
    print(f"Orders:           {len(orders):,}")
    print(f"Order items:      {len(order_items):,}")
    print(f"Payments:         {len(payments):,}")
    print(f"Shipments:        {len(shipments):,}")
    print(f"Returns:          {len(returns):,}")
    print(f"Marketing rows:   {len(marketing_spend):,}")

    revenue = orders["total_amount"].sum()
    avg_order_value = orders.loc[orders["order_status"] != "cancelled", "total_amount"].mean()
    return_rate = len(returns) / max(len(order_items), 1)
    failed_payment_rate = (payments["payment_status"] == "failed").mean()

    print(f"\nTotal gross order value: {revenue:,.2f}")
    print(f"Average order value:     {avg_order_value:,.2f}")
    print(f"Item-level return rate:  {return_rate:.2%}")
    print(f"Failed payment rate:     {failed_payment_rate:.2%}")

    print("\nTop 5 categories by products:")
    print(products["category"].value_counts().head(5).to_string())

    print("\nOrder status distribution:")
    print(orders["order_status"].value_counts(normalize=True).mul(100).round(2).astype(str) + "%")

    print("\n=================================================\n")


# ============================================================
# SAVE
# ============================================================

def save_csvs(output_dir: Path, tables: dict[str, pd.DataFrame]) -> None:
    ensure_dir(output_dir)
    for name, df in tables.items():
        out_path = output_dir / f"{name}.csv"
        df.to_csv(out_path, index=False)
        print(f"Saved {out_path}")


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    set_seed(SEED)

    print("Generating customers...")
    customers = generate_customers(N_CUSTOMERS)

    print("Generating products...")
    products = generate_products(N_PRODUCTS)

    print("Generating orders + related tables...")
    orders, order_items, payments, shipments, returns = generate_orders_and_related(
        customers=customers,
        products=products,
        n_orders=N_ORDERS,
    )

    print("Generating marketing spend...")
    marketing_spend = generate_marketing_spend(START_DATE, END_DATE)

    run_basic_checks(
        customers=customers,
        products=products,
        orders=orders,
        order_items=order_items,
        payments=payments,
        shipments=shipments,
        returns=returns,
        marketing_spend=marketing_spend,
    )

    print_summary(
        customers=customers,
        products=products,
        orders=orders,
        order_items=order_items,
        payments=payments,
        shipments=shipments,
        returns=returns,
        marketing_spend=marketing_spend,
    )

    save_csvs(
        OUTPUT_DIR,
        {
            "customers": customers,
            "products": products,
            "orders": orders,
            "order_items": order_items,
            "payments": payments,
            "shipments": shipments,
            "returns": returns,
            "marketing_spend": marketing_spend,
        },
    )

    print("Done.")


if __name__ == "__main__":
    main()
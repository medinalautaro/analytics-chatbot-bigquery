from __future__ import annotations

from pathlib import Path
import pandas as pd


DATA_DIR = Path("data/generated")


def load_data():
    customers = pd.read_csv(DATA_DIR / "customers.csv", parse_dates=["signup_date"])
    products = pd.read_csv(DATA_DIR / "products.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv", parse_dates=["order_timestamp"])
    order_items = pd.read_csv(DATA_DIR / "order_items.csv")
    payments = pd.read_csv(DATA_DIR / "payments.csv", parse_dates=["payment_timestamp"])
    shipments = pd.read_csv(
        DATA_DIR / "shipments.csv",
        parse_dates=["shipment_timestamp", "delivery_timestamp"]
    )
    returns = pd.read_csv(DATA_DIR / "returns.csv", parse_dates=["return_timestamp"])
    marketing = pd.read_csv(DATA_DIR / "marketing_spend.csv", parse_dates=["date"])

    return customers, products, orders, order_items, payments, shipments, returns, marketing


def check(condition: bool, message: str):
    if condition:
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")


def main():
    customers, products, orders, order_items, payments, shipments, returns, marketing = load_data()

    print("=== RELATIONAL INTEGRITY ===")
    check(customers["customer_id"].is_unique, "customer_id is unique")
    check(products["product_id"].is_unique, "product_id is unique")
    check(orders["order_id"].is_unique, "order_id is unique")
    check(order_items["order_item_id"].is_unique, "order_item_id is unique")
    check(payments["payment_id"].is_unique, "payment_id is unique")
    check(shipments["shipment_id"].is_unique, "shipment_id is unique")
    check(returns["return_id"].is_unique, "return_id is unique")

    check(orders["customer_id"].isin(customers["customer_id"]).all(), "all orders reference valid customers")
    check(order_items["order_id"].isin(orders["order_id"]).all(), "all order_items reference valid orders")
    check(order_items["product_id"].isin(products["product_id"]).all(), "all order_items reference valid products")
    check(payments["order_id"].isin(orders["order_id"]).all(), "all payments reference valid orders")
    check(shipments["order_id"].isin(orders["order_id"]).all(), "all shipments reference valid orders")
    check(returns["order_item_id"].isin(order_items["order_item_id"]).all(), "all returns reference valid order items")

    print("\n=== BUSINESS RULES ===")
    op = orders.merge(payments[["order_id", "payment_timestamp", "payment_status", "amount"]], on="order_id", how="left")
    check((op["payment_timestamp"] >= op["order_timestamp"]).all(), "payments happen after orders")

    ps = payments.merge(shipments[["order_id", "shipment_timestamp", "delivery_timestamp"]], on="order_id", how="left")
    shipped = ps["shipment_timestamp"].notna()
    delivered = ps["delivery_timestamp"].notna()

    check((ps.loc[shipped, "shipment_timestamp"] >= ps.loc[shipped, "payment_timestamp"]).all(),
          "shipments happen after payments")
    check((ps.loc[delivered, "delivery_timestamp"] >= ps.loc[delivered, "shipment_timestamp"]).all(),
          "deliveries happen after shipments")

    ri = returns.merge(order_items[["order_item_id", "line_amount"]], on="order_item_id", how="left")
    check((ri["refund_amount"] <= ri["line_amount"]).all(), "refund amount does not exceed line amount")

    cancelled_orders = orders.loc[orders["order_status"] == "cancelled", "order_id"]
    check(~shipments["order_id"].isin(cancelled_orders).any(), "cancelled orders have no shipments")

    failed_payment_orders = payments.loc[payments["payment_status"] == "failed", "order_id"]
    failed_paid_amounts = payments.loc[payments["payment_status"] == "failed", "amount"]
    check((failed_paid_amounts == 0).all(), "failed payments have zero paid amount")

    print("\n=== REALISM CHECKS ===")

    # Long-tail customer behavior
    orders_per_customer = orders.groupby("customer_id").size()
    p50 = orders_per_customer.quantile(0.50)
    p90 = orders_per_customer.quantile(0.90)
    p99 = orders_per_customer.quantile(0.99)
    print(f"Orders per customer percentiles: p50={p50:.1f}, p90={p90:.1f}, p99={p99:.1f}")
    check(p99 > p90 > p50, "customer order distribution is long-tailed")

    # Evening vs overnight activity
    hour_counts = orders["order_timestamp"].dt.hour.value_counts()
    overnight = hour_counts.loc[[0, 1, 2, 3, 4, 5]].sum() if set([0,1,2,3,4,5]).issubset(hour_counts.index) else hour_counts[hour_counts.index.isin([0,1,2,3,4,5])].sum()
    evening = hour_counts.loc[[18, 19, 20, 21, 22]].sum() if set([18,19,20,21,22]).issubset(hour_counts.index) else hour_counts[hour_counts.index.isin([18,19,20,21,22])].sum()
    print(f"Overnight orders: {overnight:,}")
    print(f"Evening orders:   {evening:,}")
    check(evening > overnight, "more orders occur in the evening than overnight")

    # Seasonality
    monthly_orders = orders.assign(month=orders["order_timestamp"].dt.month).groupby("month").size()
    nov_dec = monthly_orders.loc[[11, 12]].mean()
    jan_feb = monthly_orders.loc[[1, 2]].mean()
    print(f"Avg monthly orders Nov-Dec: {nov_dec:,.0f}")
    print(f"Avg monthly orders Jan-Feb: {jan_feb:,.0f}")
    check(nov_dec > jan_feb, "holiday season has more orders than early-year months")

    # Return rates by category
    returns_by_cat = (
        returns.merge(order_items[["order_item_id", "product_id"]], on="order_item_id", how="left")
               .merge(products[["product_id", "category"]], on="product_id", how="left")
               .groupby("category")
               .size()
    )
    items_by_cat = (
        order_items.merge(products[["product_id", "category"]], on="product_id", how="left")
                   .groupby("category")
                   .size()
    )
    return_rate_by_cat = (returns_by_cat / items_by_cat).fillna(0).sort_values(ascending=False)
    print("\nReturn rate by category:")
    print((return_rate_by_cat * 100).round(2).astype(str) + "%")

    if "fashion" in return_rate_by_cat.index and "books" in return_rate_by_cat.index:
        check(return_rate_by_cat["fashion"] > return_rate_by_cat["books"],
              "fashion return rate is higher than books")

    # Missingness
    device_null_rate = customers["device_type"].isna().mean()
    channel_null_rate = customers["marketing_channel"].isna().mean()
    print(f"\nMissing device_type rate: {device_null_rate:.2%}")
    print(f"Missing marketing_channel rate: {channel_null_rate:.2%}")
    check(device_null_rate < 0.02, "device_type missingness is small")
    check(channel_null_rate < 0.02, "marketing_channel missingness is small")

    print("\n=== SUMMARY ===")
    print(f"Customers:     {len(customers):,}")
    print(f"Orders:        {len(orders):,}")
    print(f"Order items:   {len(order_items):,}")
    print(f"Payments:      {len(payments):,}")
    print(f"Shipments:     {len(shipments):,}")
    print(f"Returns:       {len(returns):,}")
    print(f"Marketing rows:{len(marketing):,}")


if __name__ == "__main__":
    main()
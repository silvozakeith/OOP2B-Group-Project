import json
import os

ORDERS_FILE = "orders.json"
PRICES_FILE = "prices.json"

DEFAULT_PRICES = {
    'paper': 2.0,
    'legal': 2.5,
    'photo_paper': 25.0,
    'bw': 2.0,
    'color': 5.0,
    'binding': 30.0,
    'lamination': 15.0,
}


def load_prices() -> dict:
    if os.path.exists(PRICES_FILE):
        try:
            with open(PRICES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    save_prices(DEFAULT_PRICES)
    return DEFAULT_PRICES.copy()


def save_prices(prices: dict):
    with open(PRICES_FILE, 'w', encoding='utf-8') as f:
        json.dump(prices, f, indent=4)


def load_orders() -> list:
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_orders(orders: list):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=4)


def add_order(order: dict):
    orders = load_orders()
    orders.append(order)
    save_orders(orders)


def update_order_status(order_id: str, new_status: str):
    orders = load_orders()
    for order in orders:
        if order["id"] == order_id:
            order["status"] = new_status
            break
    save_orders(orders)
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
PRODUCTS_PATH = BASE / "products.xlsx"
ORDERS_PATH = BASE / "orders.xlsx"
FAQ_PATH = BASE / "faq.xlsx"

app = Flask(__name__)
CORS(app)

# Load data
products_df = pd.read_excel(PRODUCTS_PATH)
orders_df = pd.read_excel(ORDERS_PATH)
faq_df = pd.read_excel(FAQ_PATH)

# Simple helper logic (mirrors chatbot_logic.py functions)
def extract_order_id(text):
    m = re.search(r"(O\d{4})", text, flags=re.IGNORECASE)
    return m.group(1) if m else None

def handle_order_status(text):
    oid = extract_order_id(text)
    if not oid:
        return "Please provide an order ID (e.g., O1001)."
    row = orders_df[orders_df['order_id'].astype(str).str.upper() == oid.upper()]
    if row.empty:
        return f"Sorry, order ID {oid} was not found."
    status = row.iloc[0]['status']
    expected = row.iloc[0]['expected_delivery_date']
    return f"Order {oid} is {status} and expected to arrive on {expected}."

def handle_return_policy(_text):
    ans = faq_df[faq_df['question'].str.contains('return', case=False, na=False)]
    if not ans.empty:
        return ans.iloc[0]['answer']
    return "You can return any unused item within 14 days of delivery for a full refund."

def handle_delivery_time(_text):
    ans = faq_df[faq_df['question'].str.contains('delivery', case=False, na=False)]
    if not ans.empty:
        return ans.iloc[0]['answer']
    return "Delivery typically takes 3-5 working days."

def handle_payment_methods(_text):
    ans = faq_df[faq_df['question'].str.contains('payment', case=False, na=False)]
    if not ans.empty:
        return ans.iloc[0]['answer']
    return "We accept Visa, MasterCard, debit cards, and cash on delivery."

def handle_order_cancellation(_text):
    ans = faq_df[faq_df['question'].str.contains('cancel', case=False, na=False)]
    if not ans.empty:
        return ans.iloc[0]['answer']
    return "Orders can be cancelled before they are shipped."

def handle_warranty_info(_text):
    ans = faq_df[faq_df['question'].str.contains('warranty', case=False, na=False)]
    if not ans.empty:
        return ans.iloc[0]['answer']
    return "Electronics items come with a 6-month warranty."

def handle_exchange_policy(_text):
    ans = faq_df[faq_df['question'].str.contains('exchange', case=False, na=False)]
    if not ans.empty:
        return ans.iloc[0]['answer']
    return "You may exchange items for size or color within 7 days of delivery."

def handle_product_recommendation(text):
    categories = products_df['category'].str.lower().unique().tolist()
    text_low = text.lower()
    matched = [c for c in categories if c in text_low]
    if matched:
        cat = matched[0]
        matches = products_df[products_df['category'].str.lower() == cat]
        if matches.empty:
            return f"No products found in category '{cat}'. Please try another category."
        in_stock = matches[matches['stock_status'] == 'in_stock']
        pick = in_stock.head(2) if not in_stock.empty else matches.head(2)
        lines = []
        for _, r in pick.iterrows():
            lines.append(f"{r['name']} ({r['product_id']}) - {r['description']} - LKR {r['price']}")
        return "You may like:\n" + "\n".join(lines)
    else:
        return "Please specify a category (e.g., electronics, fitness, clothing)."

def handle_track_order(text):
    oid = extract_order_id(text)
    if not oid:
        return "Please provide an order ID to track (e.g., O1001)."
    row = orders_df[orders_df['order_id'].astype(str).str.upper() == oid.upper()]
    if row.empty:
        return f"Order {oid} not found."
    status = row.iloc[0]['status']
    return f"Order {oid} is currently {status}."

def fallback(_text):
    return "Sorry, I didn't understand that. Could you rephrase your question or ask about orders, returns, delivery, or product recommendations?"

# Intent detection simple
INTENT_KEYWORDS = {
    "order_status": ["order", "order id", "my order", "status", "where is", "delivery date", "orderid"],
    "return_policy": ["return", "refund", "send back", "return policy", "money back"],
    "delivery_time": ["delivery time", "how long", "when will it arrive", "shipping time", "time to deliver"],
    "payment_methods": ["payment", "payment methods", "pay", "card", "cash on delivery", "visa", "mastercard", "debit"],
    "order_cancellation": ["cancel", "cancel order", "stop order", "undo order"],
    "warranty_info": ["warranty", "guarantee", "product warranty", "how long warranty"],
    "exchange_policy": ["exchange", "replace", "swap", "exchange policy", "change size"],
    "product_recommendation": ["recommend", "suggest", "advice", "good product", "suggestion", "recommendation"],
    "track_order": ["track", "tracking", "follow order", "locate order", "track my order"]
}

INTENT_HANDLERS = {
    "order_status": handle_order_status,
    "return_policy": handle_return_policy,
    "delivery_time": handle_delivery_time,
    "payment_methods": handle_payment_methods,
    "order_cancellation": handle_order_cancellation,
    "warranty_info": handle_warranty_info,
    "exchange_policy": handle_exchange_policy,
    "product_recommendation": handle_product_recommendation,
    "track_order": handle_track_order
}

def detect_intent(text):
    text_low = text.lower()
    if extract_order_id(text_low):
        return "order_status"
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text_low:
                return intent
    return "fallback"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    message = data['message']
    intent = detect_intent(message)
    handler = INTENT_HANDLERS.get(intent, fallback)
    reply = handler(message)
    return jsonify({"reply": reply, "intent": intent})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

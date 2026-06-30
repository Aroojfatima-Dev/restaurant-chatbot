"""
Restaurant AI Chatbot - Flask Backend
Author: Arooj Fatima
A rule-based + intent-matching chatbot for restaurant customer support.
Handles: menu queries, reservations, delivery info, store hours, and FAQs.
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# RESTAURANT DATA (in a real project this would come from a database)
# ─────────────────────────────────────────────────────────────

RESTAURANT_INFO = {
    "name": "Lahori Bites",
    "hours": {
        "weekday": "Monday – Saturday: 11:00 AM – 11:00 PM",
        "weekend": "Sunday: 12:00 PM – 10:00 PM"
    },
    "delivery": {
        "available": True,
        "radius_km": 10,
        "free_delivery_above": 1500,
        "delivery_fee": 150
    },
    "phone": "0300-1234567",
    "address": "MM Alam Road, Gulberg III, Lahore"
}

MENU = {
    "starters": [
        {"name": "Chicken Seekh Kebab", "price": 450},
        {"name": "Vegetable Spring Rolls", "price": 350},
        {"name": "Chicken Wings", "price": 550},
    ],
    "main_course": [
        {"name": "Chicken Karahi", "price": 1200},
        {"name": "Beef Biryani", "price": 650},
        {"name": "Daal Makhani", "price": 450},
        {"name": "Butter Chicken", "price": 950},
    ],
    "desserts": [
        {"name": "Gulab Jamun", "price": 250},
        {"name": "Kheer", "price": 300},
    ],
    "beverages": [
        {"name": "Fresh Lime", "price": 150},
        {"name": "Mango Lassi", "price": 250},
        {"name": "Soft Drink", "price": 120},
    ]
}

# ─────────────────────────────────────────────────────────────
# INTENT DEFINITIONS
# Each intent has a list of trigger keywords/phrases and a handler function.
# This is a simple rule-based NLP approach — no external ML library needed,
# which keeps the bot fast, free to run, and easy to extend.
# ─────────────────────────────────────────────────────────────

def handle_greeting(message):
    return (f"Hi there! 👋 Welcome to {RESTAURANT_INFO['name']}. "
            f"I can help you with our menu, store hours, delivery, or reservations. "
            f"What would you like to know?")

def handle_hours(message):
    return (f"Our store hours are:\n"
            f"📅 {RESTAURANT_INFO['hours']['weekday']}\n"
            f"📅 {RESTAURANT_INFO['hours']['weekend']}")

def handle_menu(message):
    # Detect if a specific category was asked
    categories = {
        "starter": "starters", "appetizer": "starters",
        "main": "main_course", "course": "main_course",
        "dessert": "desserts", "sweet": "desserts",
        "drink": "beverages", "beverage": "beverages"
    }
    msg_lower = message.lower()
    for keyword, category in categories.items():
        if keyword in msg_lower:
            items = MENU[category]
            item_list = "\n".join([f"• {i['name']} — Rs. {i['price']}" for i in items])
            return f"Here's our {category.replace('_', ' ')} menu:\n\n{item_list}"

    # Otherwise return full menu summary
    response = "Here's a quick look at our menu:\n\n"
    for category, items in MENU.items():
        response += f"**{category.replace('_', ' ').title()}**\n"
        for item in items[:2]:
            response += f"• {item['name']} — Rs. {item['price']}\n"
        response += "\n"
    response += "Ask me about a specific category for the full list!"
    return response

def handle_delivery(message):
    info = RESTAURANT_INFO['delivery']
    if not info['available']:
        return "Sorry, we currently don't offer delivery. Dine-in and takeaway are available!"
    return (f"Yes, we deliver! 🚚\n"
            f"• Delivery radius: {info['radius_km']} km\n"
            f"• Free delivery on orders above Rs. {info['free_delivery_above']}\n"
            f"• Delivery fee: Rs. {info['delivery_fee']} (below free threshold)\n\n"
            f"Want to place an order?")

def handle_reservation(message):
    return (f"I'd love to help you book a table! 🍽️\n"
            f"Please call us at {RESTAURANT_INFO['phone']} or reply with your preferred "
            f"date, time, and number of guests, and I'll note it down.")

def handle_location(message):
    return f"📍 We're located at {RESTAURANT_INFO['address']}.\nCall us: {RESTAURANT_INFO['phone']}"

def handle_human(message):
    return f"No problem! You can reach our team directly at {RESTAURANT_INFO['phone']}. They're available during store hours. 📞"

def handle_thanks(message):
    return "You're welcome! 😊 Anything else I can help you with?"

def handle_fallback(message):
    return ("I'm not sure I understood that. I can help with:\n"
            "• Menu & prices\n• Store hours\n• Delivery info\n"
            "• Table reservations\n• Location\n\nWhat would you like to know?")

# ─────────────────────────────────────────────────────────────
# INTENT MATCHING ENGINE
# Maps keyword patterns to handler functions.
# ─────────────────────────────────────────────────────────────

INTENTS = [
    {"name": "greeting", "patterns": [r"\b(hi|hello|hey|salam|assalam)\b"], "handler": handle_greeting},
    {"name": "hours", "patterns": [r"\b(hours?|timing|open|close|when.*open)\b"], "handler": handle_hours},
    {"name": "menu", "patterns": [r"\b(menu|food|dish|eat|order|starter|main course|dessert|drink|price)\b"], "handler": handle_menu},
    {"name": "delivery", "patterns": [r"\b(deliver|delivery|home delivery|order online)\b"], "handler": handle_delivery},
    {"name": "reservation", "patterns": [r"\b(reserv|book.*table|table for)\b"], "handler": handle_reservation},
    {"name": "location", "patterns": [r"\b(location|address|where.*you|find you)\b"], "handler": handle_location},
    {"name": "human", "patterns": [r"\b(human|agent|representative|talk to someone|call)\b"], "handler": handle_human},
    {"name": "thanks", "patterns": [r"\b(thanks|thank you|shukriya)\b"], "handler": handle_thanks},
]

def match_intent(message):
    """
    Scans the user message against all known intent patterns.
    Returns the response from the first matching intent, or a fallback response.
    This is a lightweight alternative to a full ML/NLP pipeline —
    fast, free, and predictable for a defined business domain like a restaurant.
    """
    msg_lower = message.lower()
    for intent in INTENTS:
        for pattern in intent["patterns"]:
            if re.search(pattern, msg_lower):
                return intent["handler"](message)
    return handle_fallback(message)

# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", restaurant=RESTAURANT_INFO)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please type a message!"})

    bot_response = match_intent(user_message)

    return jsonify({
        "response": bot_response,
        "timestamp": datetime.now().strftime("%I:%M %p")
    })

@app.route("/menu", methods=["GET"])
def get_menu():
    """API endpoint returning full menu as JSON — useful for a frontend menu page."""
    return jsonify(MENU)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

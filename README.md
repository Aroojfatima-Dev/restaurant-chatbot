# 🍽️ Restaurant AI Chatbot (Flask + Python)

A rule-based, intent-matching AI chatbot built for restaurants — handles menu queries, store hours, delivery information, and table reservations automatically.

Built as a portfolio project to demonstrate backend chatbot logic using **Python** and **Flask**, without relying on paid AI APIs.

---

## ✨ Features

- 🍴 **Menu browsing** — full menu or category-specific (starters, main course, desserts, beverages)
- 🕘 **Store hours** — instant answers on weekday/weekend timing
- 🚚 **Delivery info** — radius, fees, and free delivery threshold
- 📅 **Table reservations** — captures booking requests
- 📍 **Location & contact** — address and phone number
- 💬 **8 intent categories** with keyword/regex pattern matching
- 🎨 **Clean chat UI** — typing-style interface with quick reply buttons

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (vanilla, no frameworks)
- **NLP Approach:** Rule-based intent matching using regex patterns

---

## 📂 Project Structure

```
restaurant-chatbot/
├── app.py                 # Flask backend + intent matching engine
├── templates/
│   └── index.html         # Chat UI
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🚀 How to Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/Aroojfatima-Dev/restaurant-chatbot.git
cd restaurant-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Flask app**
```bash
python app.py
```

4. **Open in browser**
```
http://localhost:5000
```

---

## 🧠 How the Intent Matching Works

Instead of using a paid LLM API for every message, this bot uses a lightweight **regex-based intent matcher**:

```python
INTENTS = [
    {"name": "menu", "patterns": [r"\b(menu|food|dish|order)\b"], "handler": handle_menu},
    {"name": "hours", "patterns": [r"\b(hours?|timing|open)\b"], "handler": handle_hours},
    # ...
]
```

Each incoming message is scanned against these patterns. The first match triggers its handler function, which returns a relevant, pre-written response. This approach is:

- ✅ **Free** — no API costs
- ✅ **Fast** — no network latency
- ✅ **Predictable** — reliable for a well-defined business domain
- ✅ **Easy to extend** — add a new intent in a few lines

---

## 💡 Use Case

This architecture is ideal for small businesses (restaurants, salons, clinics) that need a **reliable FAQ + order-taking bot** without ongoing AI API costs. It can be customized per client by editing the `RESTAURANT_INFO` and `MENU` dictionaries.

---

## 👩‍💻 About

Built by **Arooj Fatima** — AI Chatbot Developer & Graphic Designer, BSCS student at University of South Asia, Lahore.

- 🔗 [Fiverr](https://www.fiverr.com/s/42EPdgm)
- 🔗 [LinkedIn](https://www.linkedin.com/in/arooj-fatima-7b78aa379)

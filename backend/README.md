Backend (Flask)
---------------

Requirements:
- Python 3.8+
- Install packages: pip install -r requirements.txt

Run locally:
1. cd backend
2. pip install -r requirements.txt
3. python app.py
The API will run at http://localhost:5000

Endpoint:
POST /chat
Body: { "message": "Where is order O1001?" }
Response: { "reply": "...", "intent": "order_status" }

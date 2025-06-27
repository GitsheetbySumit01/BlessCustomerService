# utils/ticket_manager.py

tickets = {}

def create_ticket(user_id, user_name, message):
    tickets[user_id] = {
        "user_name": user_name,
        "message": message,
        "status": "pending",
        "reply": None
    }

def mark_resolved(user_id):
    if user_id in tickets:
        tickets[user_id]["status"] = "resolved"

def store_reply(user_id, reply_text):
    if user_id in tickets:
        tickets[user_id]["reply"] = reply_text

def get_status(user_id):
    return tickets.get(user_id, {}).get("status", "unknown")

def get_all_tickets():
    return tickets

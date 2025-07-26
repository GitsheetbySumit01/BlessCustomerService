from datetime import datetime

tickets = {}

def create_ticket(user_id, user_name, message, language="en"):
    tickets[user_id] = {
        "user_name": user_name,
        "message": message,
        "status": "pending",
        "reply": None,
        "created_at": datetime.now(),
        "resolved_at": None,
        "language": language,
        "admin_messages": {},
        "created_at": datetime.now()  # ✅ Timestamp for PDF filtering
    }

def mark_resolved(user_id):
    if user_id in tickets:
        tickets[user_id]["status"] = "resolved"
        tickets[user_id]["resolved_at"] = datetime.now()

def store_reply(user_id, reply_text):
    if user_id in tickets:
        tickets[user_id]["reply"] = reply_text

def store_admin_message_id(user_id, admin_chat_id, message_id):
    if user_id in tickets:
        tickets[user_id]["admin_messages"][admin_chat_id] = message_id

def get_admin_message_ids(user_id):
    return tickets.get(user_id, {}).get("admin_messages", {})

def get_ticket(user_id):
    return tickets.get(user_id)

def get_all_tickets():
    return tickets


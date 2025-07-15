tickets = {}

def create_ticket(user_id, user_name, message):
    tickets[user_id] = {
        "user_name": user_name,
        "message": message,
        "status": "pending",
        "reply": None,
        "admin_messages": {}
    }

def mark_resolved(user_id):
    if user_id in tickets:
        tickets[user_id]["status"] = "resolved"

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

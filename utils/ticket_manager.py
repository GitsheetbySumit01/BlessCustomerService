import json
import os
from datetime import datetime

TICKET_FILE = "data/tickets.json"
tickets = {}

def _load_tickets():
    global tickets
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            for uid, data in raw_data.items():
                data["created_at"] = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
                data["resolved_at"] = datetime.fromisoformat(data["resolved_at"]) if data.get("resolved_at") else None
                tickets[uid] = data

def _save_tickets():
    data_to_save = {}
    for uid, data in tickets.items():
        data_to_save[uid] = {
            **data,
            "created_at": data["created_at"].isoformat() if data.get("created_at") else None,
            "resolved_at": data["resolved_at"].isoformat() if data.get("resolved_at") else None
        }
    os.makedirs(os.path.dirname(TICKET_FILE), exist_ok=True)
    with open(TICKET_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=2)

def create_ticket(user_id, user_name, message, language="en"):
    tickets[user_id] = {
        "user_name": user_name,
        "message": message,
        "status": "pending",
        "reply": None,
        "created_at": datetime.now(),
        "resolved_at": None,
        "language": language,
        "admin_messages": {}
    }
    _save_tickets()

def mark_resolved(user_id):
    if user_id in tickets:
        tickets[user_id]["status"] = "resolved"
        tickets[user_id]["resolved_at"] = datetime.now()
        _save_tickets()

def store_reply(user_id, reply_text):
    if user_id in tickets:
        tickets[user_id]["reply"] = reply_text
        _save_tickets()

def store_admin_message_id(user_id, admin_chat_id, message_id):
    if user_id in tickets:
        tickets[user_id]["admin_messages"][admin_chat_id] = message_id
        _save_tickets()

def get_admin_message_ids(user_id):
    return tickets.get(user_id, {}).get("admin_messages", {})

def get_ticket(user_id):
    return tickets.get(user_id)

def get_all_tickets():
    return tickets

_load_tickets()

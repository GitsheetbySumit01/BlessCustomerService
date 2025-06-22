# supportbox/ticket_queue.py

import json
import os

QUEUE_FILE = "supportbox/ticket_queue.json"

def add_to_queue(user_id, message):
    if not os.path.exists(QUEUE_FILE):
        queue = []
    else:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
    queue.append({"user_id": user_id, "message": message})
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

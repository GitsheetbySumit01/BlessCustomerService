import json
import os

USERS_FILE = "data/users.json"

def track_user(user_id, username):
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    users[str(user_id)] = {"username": username}
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}
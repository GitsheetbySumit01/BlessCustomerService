# utils/localization.py

import json
import os

LANG_FILE = "data/user_languages.json"

def get_user_language(user_id):
    if not os.path.exists(LANG_FILE):
        return None
    with open(LANG_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(user_id))

def set_user_language(user_id, lang_code):
    data = {}
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, "r") as f:
            data = json.load(f)
    data[str(user_id)] = lang_code
    with open(LANG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_message(user_id, key):
    lang_code = get_user_language(user_id) or "en"
    file_path = f"messages/{lang_code}.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(key, "⚠️ Message not found.")
    except FileNotFoundError:
        return "⚠️ Language file missing."

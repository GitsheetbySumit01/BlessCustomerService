# config.py
import os

BOT_TOKEN =os.environ.get("BOT_TOKEN")
ADMIN_CHAT_IDS = [
    1746690976,   # Your first admin Telegram ID
    5092181510] # Replace with actual Telegram user ID
LANGUAGES = ["English", "Hindi", "Tamil"]

LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta"
}

WELCOME_IMAGE_URL = "https://example.com/welcome-image.jpg"  # Placeholder

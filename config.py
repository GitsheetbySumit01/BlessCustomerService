# config.py
import os

<<<<<<< HEAD

BOT_TOKEN ="8205849457:AAEGih4KdUDKVHGIszjTMkH2U-IBpLfMsXo"
=======
BOT_TOKEN =os.environ.get("BOT_TOKEN")
>>>>>>> 1edc7263d53dd5ebe116fbfbe717daf4a409a94f
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

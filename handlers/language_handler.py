# handlers/language_handler.py

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import LANG_CODES, LANGUAGES
from utils.localization import get_message, set_user_language
from handlers.menu_handler import send_main_menu
import json

# Always ask for language selection on /start
async def ask_for_language(update, context, user_id):
    buttons = [[KeyboardButton(lang)] for lang in LANGUAGES]
    await update.message.reply_text(
        "🌐 Please select your preferred language:",
        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    )

# Once language is selected, show confirmation + menu
async def handle_language_choice(update, context, user_id, language):
    lang_code = LANG_CODES.get(language, "en")
    set_user_language(user_id, lang_code)

    # Load message file for selected language
    with open(f"messages/{lang_code}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1️⃣ Confirm language selection
    await update.message.reply_text(data.get("language_selected", "✅ Language selected."))

    # 2️⃣ Prompt for menu interaction
    

    # 3️⃣ Show menu
    await send_main_menu(update, context, user_id)

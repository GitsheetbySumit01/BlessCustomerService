# handlers/language_handler.py

from telegram import ReplyKeyboardMarkup, KeyboardButton
from config import LANG_CODES, LANGUAGES
from utils.localization import get_message, set_user_language
from handlers.menu_handler import send_main_menu

# Always ask for language selection on /start
async def ask_for_language(update, context, user_id):
    buttons = [[KeyboardButton(lang)] for lang in LANGUAGES]
    await update.message.reply_text(
        "🌐 Please select your preferred language:",
        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    )

# Once language is selected, welcome and show menu
async def handle_language_choice(update, context, user_id, language):
    lang_code = LANG_CODES.get(language, "en")
    set_user_language(user_id, lang_code)
    welcome_msg = get_message(user_id, "welcome")
    await update.message.reply_text(welcome_msg)
    await send_main_menu(update, context, user_id)

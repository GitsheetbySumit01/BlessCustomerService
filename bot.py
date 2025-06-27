import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters, CallbackQueryHandler
)

from config import BOT_TOKEN
from handlers.language_handler import ask_for_language, handle_language_choice
from handlers.menu_handler import send_main_menu, handle_menu_selection
from handlers.support_handler import handle_support_response, process_support_message
from handlers.admin_handler import handle_admin_callback, handle_admin_reply

logging.basicConfig(level=logging.INFO)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await ask_for_language(update, context, user_id)

# universal text handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text

    # language selection
    if text in ["English", "Hindi", "Tamil"]:
        await handle_language_choice(update, context, user_id, text)

    # support request
    elif text in [
        "📞 Contact Customer Service",
        "📞 ग्राहक सेवा से संपर्क करें",
        "📞 வாடிக்கையாளர் சேவையை தொடர்புகொள்ளவும்"
    ]:
        await handle_support_response(update, context)

    # support reply
    elif context.user_data.get("awaiting_support"):
        await process_support_message(update, context)

    # admin reply to user
    elif context.user_data.get("reply_user_id"):  # ✅ Fixed key check
        await handle_admin_reply(update, context)

    # normal menu
    else:
        await handle_menu_selection(update, context, user_id, text)

# app init
app = ApplicationBuilder().token(BOT_TOKEN).connect_timeout(10).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_admin_callback))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

print("🚀 Bless Exchange Bot is running...")
app.run_polling()


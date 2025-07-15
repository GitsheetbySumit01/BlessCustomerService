import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)

from config import BOT_TOKEN, ADMIN_CHAT_IDS
from handlers.language_handler import ask_for_language, handle_language_choice
from handlers.menu_handler import send_main_menu, handle_menu_selection
from handlers.support_handler import handle_support_response, process_support_message
from handlers.admin_handler import handle_admin_callback, handle_admin_reply
from utils.user_tracker import track_user, load_users
from utils.localization import get_user_language
import json

logging.basicConfig(level=logging.INFO)

WELCOME_IMAGE_ID = "WhatsApp Image 2025-07-02 at 09.41.38.jpeg"  # Update if needed

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    track_user(user_id, update.effective_user.username)

    lang = get_user_language(user_id) or "en"
    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Send welcome image + caption
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=WELCOME_IMAGE_ID,
        caption=data["welcome"],
        parse_mode="Markdown"
    )

    await ask_for_language(update, context, user_id)

# Handles all incoming text messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    track_user(user_id, update.effective_user.username)

    if text in ["English", "Hindi", "Tamil"]:
        await handle_language_choice(update, context, user_id, text)
        return

    if text in [
        "📞 Contact Customer Service",
        "📞 ग्राहक सेवा से संपर्क करें",
        "📞 வாடிக்கையாளர் சேவையை தொடர்புகொள்ளவும்"
    ]:
        await handle_support_response(update, context)
        return

    lang = get_user_language(user_id) or "en"
    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    menu_texts = [
        data["btn_download_app"], data["btn_recharge"], data["btn_invite"],
        data["btn_buy_spot"], data["btn_perpetual"], data["btn_delivery"],
        data["btn_investment"], data["btn_sgd"]
    ]

    if text in menu_texts:
        await handle_menu_selection(update, context, user_id, text)
        return

    # If user was asked to describe their issue
    if context.user_data.get("awaiting_support"):
        if int(user_id) not in ADMIN_CHAT_IDS:
            await process_support_message(update, context)
        else:
            # Prevent admin text being treated as support
            context.user_data["awaiting_support"] = False
            await update.message.reply_text("⚠️ Admins can't submit tickets.")
        return

    # Admin reply
    if context.user_data.get("reply_user_id"):
        await handle_admin_reply(update, context)
        return

    await handle_menu_selection(update, context, user_id, text)

# /broadcast command for admin
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if int(user_id) not in ADMIN_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Please provide the broadcast message.")
        return

    broadcast_text = "📢 *Broadcast Message:*\n\n" + " ".join(context.args)
    users = load_users()
    if not users:
        await update.message.reply_text("⚠️ No users found.")
        return

    photo = None
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        photo = update.message.reply_to_message.photo[-1].file_id

    success, failed = 0, 0
    for uid, info in users.items():
        try:
            if photo:
                await context.bot.send_photo(
                    chat_id=int(uid),
                    photo=photo,
                    caption=broadcast_text[:1024],
                    parse_mode="Markdown"
                )
            else:
                await context.bot.send_message(
                    chat_id=int(uid),
                    text=broadcast_text[:4096],
                    parse_mode="Markdown"
                )
            success += 1
        except Exception as e:
            logging.warning(f"❌ Failed to send to {uid}: {e}")
            failed += 1

    await update.message.reply_text(
        f"✅ Broadcast completed.\n\nSent: {success} | Failed: {failed}"
    )

# Initialize bot
app = ApplicationBuilder().token(BOT_TOKEN).connect_timeout(10).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CallbackQueryHandler(handle_admin_callback))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

print("🚀 Bless Exchange Bot is running...")
app.run_polling()

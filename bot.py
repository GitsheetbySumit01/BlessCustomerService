import sys
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import BOT_TOKEN, ADMIN_CHAT_IDS
from handlers.language_handler import ask_for_language, handle_language_choice
from handlers.menu_handler import send_main_menu, handle_menu_selection
from handlers.support_handler import handle_support_response, process_support_message
from handlers.admin_handler import handle_admin_reply
from handlers.admin_menu_handler import show_admin_menu, handle_admin_pdf_callback
from utils.user_tracker import track_user, load_users
from utils.localization import get_user_language
from utils.ticket_manager import get_admin_message_ids, mark_resolved

import json

logging.basicConfig(level=logging.INFO)

WELCOME_IMAGE_ID = "image.png"

# Memory storage for ticket tracking
TICKET_MESSAGES = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    track_user(user_id, update.effective_user.username)

    lang = get_user_language(user_id) or "en"
    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=WELCOME_IMAGE_ID,
        caption=data["welcome"],
        parse_mode="Markdown"
    )

    await ask_for_language(update, context, user_id)

# Handle all text inputs
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    track_user(user_id, update.effective_user.username)

    # Language selection
    if text in ["English", "Hindi", "Tamil"]:
        await handle_language_choice(update, context, user_id, text)
        return

    # Contact Customer Service
    if text in [
        "📞 Contact Customer Service",
        "📞 ग्राहक सेवा से संपर्क करें",
        "📞 வாடிக்கையாளர் சேவையை தொடர்புகொள்ளவும்"
    ]:
        await handle_support_response(update, context)
        return

    # Get language data
    lang = get_user_language(user_id) or "en"
    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check if text matches a menu option
    menu_texts = [
        data["btn_download_app"],
        data["btn_invite"],
        data["btn_buy_spot"],
        data["btn_perpetual"],
        data["btn_investment"],
        data["btn_contact"]
    ]
    if text in menu_texts:
        await handle_menu_selection(update, context, user_id, text)
        return

    # If user is sending a support message
    if context.user_data.get("awaiting_support"):
        if int(user_id) not in ADMIN_CHAT_IDS:
            msg = await process_support_message(update, context)
            if msg:
                bless_uid = update.message.text.split(" ")[0]
                TICKET_MESSAGES[bless_uid] = {
                    admin_id: msg.message_id for admin_id in ADMIN_CHAT_IDS
                }
        else:
            context.user_data["awaiting_support"] = False
            await update.message.reply_text("⚠️ Admins can't submit tickets.")
        return

    # Admin reply
    if context.user_data.get("reply_user_id"):
        await handle_admin_reply(update, context)
        return

    # Invalid input fallback
    await update.message.reply_text(
        "⚠️ Invalid action.\n\nPlease use /start to begin, select from the main menu, or click 📞 Contact Customer Service to send a message to our team."
    )

# Broadcast command
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
    for uid in users:
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

# /admin command
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if int(user_id) in ADMIN_CHAT_IDS:
        await show_admin_menu(update, context)
    else:
        await update.message.reply_text("❌ You are not authorized to use this command.")

# Callback handler with ticket sync delete and resolve notice to all admins
async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("resolve_"):
        bless_uid = data.split("_", 1)[1]
        mark_resolved(bless_uid)

        for admin_id in ADMIN_CHAT_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"✅ Ticket from user `{bless_uid}` has been marked as resolved.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                logging.warning(f"Failed to notify admin {admin_id}: {e}")

        message_ids = get_admin_message_ids(bless_uid)
        for admin_id, msg_id in message_ids.items():
            try:
                await context.bot.delete_message(chat_id=admin_id, message_id=msg_id)
            except Exception as e:
                logging.warning(f"Failed to delete message for admin {admin_id}: {e}")

    elif data.startswith("reply_"):
        bless_uid = data.split("_", 1)[1]
        context.user_data["reply_user_id"] = bless_uid
        await query.message.reply_text(f"✏️ Please type your reply to user `{bless_uid}`.", parse_mode="Markdown")

# ✅ Bot Init
app = ApplicationBuilder().token(BOT_TOKEN).connect_timeout(120).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(handle_admin_pdf_callback, pattern="^pdf_"))
app.add_handler(CallbackQueryHandler(handle_admin_callback))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

print("🚀 Bless Exchange Bot is running...")
app.run_polling()   

# handlers/support_handler.py

from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from utils.notify_admin import notify_admin
from utils.localization import get_user_language
import json

async def handle_support_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    lang = get_user_language(user_id) or "en"

    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    await update.message.reply_text(
        data.get("support_prompt", "🆘 Please describe your issue below."),
        reply_markup=ForceReply(selective=True)
    )
    context.user_data["awaiting_support"] = True


async def process_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    message = update.message.text

    # 🔐 Only act if user was asked to provide a message
    if context.user_data.get("awaiting_support"):
        # 🚀 Notify all admins
        await notify_admin(context.bot, user, message)

        # 📩 Send confirmation to user
        lang = get_user_language(user_id) or "en"
        with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        await update.message.reply_text(
            data.get("support_ack", "✅ Thank you! Your message has been received. Our support team will contact you soon.")
        )

        # ❌ Clear the flag
        context.user_data["awaiting_support"] = False


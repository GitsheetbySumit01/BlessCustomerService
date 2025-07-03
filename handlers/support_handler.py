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
        data["support_prompt"],
        reply_markup=ForceReply(selective=True)
    )
    context.user_data['awaiting_support'] = True

async def process_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message = update.message.text

    # ✅ Always notify admin when user sends a support message
    await notify_admin(context.bot, update.effective_user, message)

    # Send confirmation to the user
    lang = get_user_language(user_id) or "en"
    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    confirmation_text = data.get(
        "support_ack",
        "✅ Thank you for contacting us! Your message has been received. Our support team will contact you soon."
    )
    await update.message.reply_text(confirmation_text)

    # Clear awaiting_support state
    context.user_data['awaiting_support'] = False

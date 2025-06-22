from telegram import ForceReply
from utils.notify_admin import notify_admin
from supportbox.ticket_queue import add_to_queue
from utils.localization import get_user_language
import json

async def handle_support_response(update, context):
    user_id = str(update.effective_user.id)
    lang = get_user_language(user_id) or "en"

    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    await update.message.reply_text(
        data["support_prompt"],
        reply_markup=ForceReply(selective=True)
    )
    context.user_data['awaiting_support'] = True

async def process_support_message(update, context):
    if context.user_data.get('awaiting_support'):
        user_id = str(update.effective_user.id)
        message = update.message.text

        add_to_queue(user_id, message)
        await notify_admin(context.bot, update.effective_user, message)

        lang = get_user_language(user_id) or "en"
        with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # ✅ Send confirmation message to the user
        confirmation_text = data.get(
            "support_ack",
            "✅ Thank you! Your message has been received. Our support team will contact you soon."
        )
        await update.message.reply_text(confirmation_text)

        context.user_data['awaiting_support'] = False

# handlers/admin_handler.py

from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from utils.ticket_manager import mark_resolved, store_reply
from utils.localization import get_message

# Handles the two buttons: Mark Resolved & Send Reply
async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("resolve_"):
        user_id = data.split("_")[1]
        mark_resolved(user_id)

        await query.edit_message_text(
            text=f"✅ Ticket marked as *Resolved* for user `{user_id}`",
            parse_mode="Markdown"
        )

    elif data.startswith("reply_"):
        user_id = data.split("_")[1]
        context.user_data["reply_user_id"] = user_id

        await query.message.reply_text(
            f"💬 Please type your reply for user ID `{user_id}`:",
            reply_markup=ForceReply(selective=True)
        )

# Handle admin reply message
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "reply_user_id" in context.user_data:
        target_user_id = context.user_data.pop("reply_user_id")
        reply_message = update.message.text

        store_reply(target_user_id, reply_message)

        try:
            await context.bot.send_message(
                chat_id=int(target_user_id),
                text=f"💬 *Reply from Customer Support:*\n\n{reply_message}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("✅ Your reply has been sent to the user.")
        except Exception as e:
            await update.message.reply_text("⚠️ Failed to send reply to user.")
            print(f"Error sending reply: {e}")

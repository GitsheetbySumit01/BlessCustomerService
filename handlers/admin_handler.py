from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from utils.ticket_manager import mark_resolved, store_reply, get_ticket, get_admin_message_ids
from config import ADMIN_CHAT_IDS

# ✅ Handles button clicks
async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = data.split("_")[1]

    if data.startswith("resolve_"):
        mark_resolved(user_id)

        # ✅ Delete ticket message from all admins
        admin_message_ids = get_admin_message_ids(user_id)
        for admin_chat_id, message_id in admin_message_ids.items():
            try:
                await context.bot.delete_message(chat_id=int(admin_chat_id), message_id=message_id)
            except Exception as e:
                print(f"Failed to delete ticket message for admin {admin_chat_id}: {e}")

        # ✅ Notify all admins
        ticket = get_ticket(user_id)
        if ticket:
            if ticket.get("username"):
                username_link = f"[{ticket['user_name']}](https://t.me/{ticket['username']})"
            else:
                username_link = f"{ticket['user_name']}"
        else:
            username_link = f"user ID `{user_id}`"

        for admin_chat_id in ADMIN_CHAT_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_chat_id,
                    text=f"✅ Ticket for {username_link} has been *marked as resolved*.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Failed to notify admin {admin_chat_id}: {e}")

    elif data.startswith("reply_"):
        context.user_data["reply_user_id"] = user_id
        await query.message.reply_text(
            f"💬 Please type your reply for user ID `{user_id}`:",
            reply_markup=ForceReply(selective=True)
        )

# ✅ Handle the admin reply message
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
            print(f"Error sending to user: {e}")

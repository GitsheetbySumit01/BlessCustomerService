from config import ADMIN_CHAT_IDS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.ticket_manager import create_ticket, store_admin_message_id
import re

# Escape MarkdownV2 characters
def escape_markdown_v2(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r'\\\1', text)

# Notify all admins with a ticket
async def notify_admin(bot, user, message):
    user_id = str(user.id)
    username = user.username
    safe_message = escape_markdown_v2(message)
    safe_name = escape_markdown_v2(user.full_name)
    username_link = f"[@{username}](https://t.me/{username})" if username else "*Not Available*"

    # Create a ticket entry
    create_ticket(user_id, user.full_name, message)

    text = (
        f"📩 *New Support Ticket Received\\!*\n\n"
        f"👤 *User:* {safe_name}\n"
        f"🆔 *Username:* {username_link}\n"
        f"📌 *Status:* Pending\n\n"
        f"📝 *Message:*\n{safe_message}"
    )

    # Ticket action buttons
    keyboard = [
        [
            InlineKeyboardButton("✅ Mark as Resolved", callback_data=f"resolve_{user_id}"),
            InlineKeyboardButton("💬 Send Reply", callback_data=f"reply_{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send to all admins
    for admin_chat_id in ADMIN_CHAT_IDS:
        try:
            sent_msg = await bot.send_message(
                chat_id=admin_chat_id,
                text=text,
                parse_mode="MarkdownV2",
                reply_markup=reply_markup
            )
            store_admin_message_id(user_id, admin_chat_id, sent_msg.message_id)
        except Exception as e:
            print(f"❌ Failed to notify admin {admin_chat_id}: {e}")

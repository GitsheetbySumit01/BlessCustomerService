from config import ADMIN_CHAT_IDS
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re
from utils.ticket_manager import create_ticket, store_admin_message_id

def escape_markdown_v2(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r'\\\1', text)

async def notify_admin(bot, user, message):
    safe_message = escape_markdown_v2(message)
    safe_name = escape_markdown_v2(user.full_name)
    username = user.username

    username_link = f"[@{username}](https://t.me/{username})" if username else "*Not Available*"

    create_ticket(str(user.id), user.full_name, message)

    text = (
        f"📩 *New Support Ticket Received\\!*\n\n"
        f"👤 *User:* {safe_name}\n"
        f"🆔 *Username:* {username_link}\n"
        f"📌 *Status:* Pending\n\n"
        f"📝 *Message:*\n{safe_message}"
    )

    keyboard = [
        [
            InlineKeyboardButton("✅ Mark as Resolved", callback_data=f"resolve_{user.id}"),
            InlineKeyboardButton("💬 Send Reply", callback_data=f"reply_{user.id}")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send ticket message to all admins and save message IDs
    for admin_chat_id in ADMIN_CHAT_IDS:
        sent = await bot.send_message(
            chat_id=admin_chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="MarkdownV2"
        )
        # Save the admin's message ID for later deletion
        store_admin_message_id(str(user.id), admin_chat_id, sent.message_id)

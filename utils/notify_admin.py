from config import ADMIN_CHAT_ID
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re
from utils.ticket_manager import create_ticket

def escape_markdown_v2(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r'\\\1', text)

async def notify_admin(bot, user, message):
    safe_message = escape_markdown_v2(message)
    safe_name = escape_markdown_v2(user.full_name)
    username = user.username

    if username:
        username_link = f"[@{username}](https://t.me/{username})"
    else:
        username_link = "*Not Available*"

    # Store using user ID to ensure uniqueness
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

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )

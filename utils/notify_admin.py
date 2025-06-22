# utils/notify_admin.py

from config import ADMIN_CHAT_ID
import re

def escape_markdown_v2(text):
    # Escape all special characters used in MarkdownV2
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r'\\\1', text)

async def notify_admin(bot, user, message):
    safe_message = escape_markdown_v2(message)
    safe_name = escape_markdown_v2(user.full_name)

    text = (
     f"📩 *New Support Ticket Received\\!*\n\n"
    f"👤 *User:* {safe_name}\n"
    f"🆔 *User ID:* `{user.id}`\n\n"
    f"📝 *Message:*\n{safe_message}"
    )

    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=text,
        parse_mode="MarkdownV2"
    )

# handlers/admin_menu_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from utils.pdf_generator import generate_pdf
from config import ADMIN_CHAT_IDS

async def show_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if int(update.effective_user.id) not in ADMIN_CHAT_IDS:
        await update.message.reply_text("❌ You are not authorized to use this.")
        return

    keyboard = [
        [
            InlineKeyboardButton("📄 PDF (24h History)", callback_data="pdf_24h"),
            InlineKeyboardButton("📄 PDF (All Tickets)", callback_data="pdf_all")
        ]
    ]
    await update.message.reply_text(
        "🛠️ *Admin Tools Menu*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def handle_admin_pdf_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if int(user_id) not in ADMIN_CHAT_IDS:
        await query.message.reply_text("❌ You are not authorized.")
        return

    mode = "24h" if query.data == "pdf_24h" else "all"
    caption = "📄 Tickets from the past 24 hours" if mode == "24h" else "📄 All support tickets"
    file_path = generate_pdf(mode)

    await context.bot.send_document(
        chat_id=user_id,
        document=InputFile(file_path),
        filename=file_path.split("/")[-1],
        caption=caption
    )


from telegram import ReplyKeyboardMarkup
from utils.localization import get_user_language
import json

async def send_main_menu(update, context, user_id):
    lang = get_user_language(user_id) or "en"
    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    buttons = [
        [data["btn_download_app"]],
        [data["btn_buy_spot"], data["btn_perpetual"]],
        [data["btn_invite"], data["btn_investment"]],
        [data["btn_contact"]]
    ]

    await update.message.reply_text(
        data["menu_header"],
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

async def handle_menu_selection(update, context, user_id, text):
    lang = get_user_language(user_id) or "en"
    with open(f"messages/{lang}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    option_map = {
        data["btn_download_app"]: "download_app",
        data["btn_invite"]: "gift_invite",
        data["btn_buy_spot"]: "buy_spot",
        data["btn_perpetual"]: "perpetual_contract",
        data["btn_investment"]: "investment"
    }

    msg_key = option_map.get(text)

    if msg_key:
        await update.message.reply_text(data[msg_key])
        await update.message.reply_text(data["support_prompt"])
        context.user_data['awaiting_support'] = True

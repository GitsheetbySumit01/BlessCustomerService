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
        data["btn_download_app"]: ("download_app", "apps.png"),
        data["btn_invite"]: ("gift_invite", "reward.png"),  # Invite image
        data["btn_buy_spot"]: ("buy_spot", None),
        data["btn_perpetual"]: ("perpetual_contract", None),
        data["btn_investment"]: ("investment", "financial.png"),  # Financial image
        data["btn_contact"]: ("support_prompt", None)
    }

    msg_key, image_file = option_map.get(text, (None, None))

    if msg_key:
        caption = data[msg_key]

        if image_file:
            try:
                with open(image_file, "rb") as img:
                    # Telegram caption limit is 1024 chars — split if needed
                    if len(caption) <= 1024:
                        await context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=img,
                            caption=caption,
                            parse_mode="Markdown"
                        )
                    else:
                        await context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=img,
                            caption=caption[:1020] + "...",
                            parse_mode="Markdown"
                        )
                        await update.message.reply_text(caption[1020:], parse_mode="Markdown")
            except FileNotFoundError:
                await update.message.reply_text(caption, parse_mode="Markdown")
        else:
            await update.message.reply_text(caption, parse_mode="Markdown")

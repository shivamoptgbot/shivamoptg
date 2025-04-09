import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
)

# Environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://shivamoptg.onrender.com")
WEBHOOK_PATH = f"/{BOT_TOKEN}"

# Media IDs
VIDEO_FILE_ID = "BAACAgUAAxkBAAMCZ_YxdwYO4SPNqtkQpf-9dIof9O4AAoYbAAMdsVeYmQfRwScYBDYE"
PHOTO_FILE_IDS = [
    "AgACAgUAAxkBAAMEZ_Yx4h-AMENk81uk0E7821CL6w8AAp7FMRsAAR2xVwP9JAABJt8GEQEAAwIAA3kAAzYE",
    "AgACAgUAAxkBAAMGZ_Yx-VMCQnZ4bwRbN_Oh_qXAoL4AAp_FMRsAAR2xVwyqSC5kKbcvAQADAgADeQADNgQ",
    "AgACAgUAAxkBAAMIZ_YyDg4F6VwCOrEamp2cnPRJfq8AAqDFMRsAAR2xV4lAKY1q3AsAAQEAAwIAA3kAAzYE",
]

# Buttons
VIP_BUTTON = InlineKeyboardMarkup([[
    InlineKeyboardButton(
        "✅ Join VIP",
        url="https://t.me/WayneAdmin11?text=Hello%20Wayne%20%F0%9F%91%8B%20I%20Want%20To%20Join%20Your%20VIP%20Group%20Please%20Guide%20Me"
    )
]])
FREE_CHANNEL_BUTTON = InlineKeyboardMarkup([[
    InlineKeyboardButton("⭐️ Free Channel", url="https://t.me/+y5wIPOzIY6M5ZDk1")
]])

# Flask app
app = Flask(__name__)
telegram_app = None  # Will be initialized below


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.first_name or user.username or "there"

    await context.bot.send_video(chat_id=update.effective_chat.id, video=VIDEO_FILE_ID)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)

    welcome_text = (
        f"👋 Hello {username}!\n\n"
        "📈 Join my *FREE VIP Channel* and start earning *$300/day or more* by following my real-time trading signals.\n\n"
        "⏳ Hurry — seats are limited!"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_text,
        reply_markup=VIP_BUTTON,
        parse_mode="Markdown"
    )

    await asyncio.sleep(7)

    for photo_id in PHOTO_FILE_IDS:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        await asyncio.sleep(1)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_id,
            reply_markup=FREE_CHANNEL_BUTTON
        )

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(2.5)

    results_text = (
        "📸 These are the results from our trading session shared by community members on Telegram!\n\n"
        "🎉 Congratulations to everyone who traded 📊 with me today and earned!\n\n"
        "If you're not making money with us yet, subscribe to my Telegram channel and start earning with me 💵"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=results_text,
        reply_markup=VIP_BUTTON
    )


@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return "OK"


async def set_webhook():
    url = f"{BASE_URL}{WEBHOOK_PATH}"
    await telegram_app.bot.set_webhook(url)
    print(f"✅ Webhook set to: {url}")


if __name__ == "__main__":
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))

    # Start Flask app in thread
    from threading import Thread
    port = int(os.environ.get("PORT", 5000))
    Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()

    # Wait and then set webhook
    import time
    time.sleep(5)
    asyncio.run(set_webhook())

    print("🚀 Bot deployed and running on Render!")

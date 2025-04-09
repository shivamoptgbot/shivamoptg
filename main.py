import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Webhook URL path
WEBHOOK_PATH = f"/{os.environ.get('BOT_TOKEN')}"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = os.environ.get("BASE_URL")  # e.g., https://your-app.onrender.com

# Media
VIDEO_FILE_ID = "BAACAgUAAxkBAAMCZ_YxdwYO4SPNqtkQpf-9dIof9O4AAoYbAAMdsVeYmQfRwScYBDYE"
PHOTO_FILE_IDS = [
    "AgACAgUAAxkBAAMEZ_Yx4h-AMENk81uk0E7821CL6w8AAp7FMRsAAR2xVwP9JAABJt8GEQEAAwIAA3kAAzYE",
    "AgACAgUAAxkBAAMGZ_Yx-VMCQnZ4bwRbN_Oh_qXAoL4AAp_FMRsAAR2xVwyqSC5kKbcvAQADAgADeQADNgQ",
    "AgACAgUAAxkBAAMIZ_YyDg4F6VwCOrEamp2cnPRJfq8AAqDFMRsAAR2xV4lAKY1q3AsAAQEAAwIAA3kAAzYE",
]

VIP_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        "✅ Join VIP",
        url="https://t.me/WayneAdmin11?text=Hello%20Wayne%20%F0%9F%91%8B%20I%20Want%20To%20Join%20Your%20VIP%20Group%20Please%20Guide%20Me"
    )]
])

FREE_CHANNEL_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⭐️ Free Channel", url="https://t.me/+y5wIPOzIY6M5ZDk1")]]
)

# Flask App
app = Flask(__name__)

# Telegram Bot Application
telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.first_name or user.username or "there"

    await update.message.reply_video(video=VIDEO_FILE_ID)

    welcome_text = (
        f"👋 Hello {username}!\n\n"
        "📈 Join my *FREE VIP Channel* and start earning *$300/day or more* by following my real-time trading signals.\n\n"
        "⏳ Hurry — seats are limited!"
    )
    await update.message.reply_text(welcome_text, reply_markup=VIP_BUTTON, parse_mode="Markdown")

    for photo_id in PHOTO_FILE_IDS:
        await update.message.reply_photo(photo=photo_id, reply_markup=FREE_CHANNEL_BUTTON)

    results_text = (
        "📸 These are the results from our trading session shared by community members on Telegram!\n\n"
        "🎉 Congratulations to everyone who traded 📊 with me today and earned!\n\n"
        "If you're not making money with us yet, subscribe to my Telegram channel and start earning with me 💵"
    )
    await update.message.reply_text(results_text, reply_markup=VIP_BUTTON)


# Register command
telegram_app.add_handler(CommandHandler("start", start))


@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok"


@app.route("/")
def index():
    return "Bot is alive!"


# Set webhook on start
async def set_webhook():
    await telegram_app.bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")


if __name__ == "__main__":
    import asyncio

    # Set webhook before running Flask
    asyncio.run(set_webhook())

    # Start Flask app (Render expects port from $PORT)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

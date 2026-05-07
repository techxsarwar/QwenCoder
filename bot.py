import os
import requests
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.constants import ChatAction

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

MODEL = "qwen/qwen-2.5-coder-32b-instruct"

SYSTEM_PROMPT = """
You are Qwen Coder Bot.

You are an advanced AI coding assistant.

Help users with:
- Python
- JavaScript
- HTML/CSS
- APIs
- Telegram Bots
- AI Apps
- Websites
- Debugging

Always provide clean and complete code.
"""


# =========================
# AI REQUEST
# =========================

def ask_qwen(prompt):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000,
            "stream": False
        },
        timeout=180,
    )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]

    except:
        return str(data)


# =========================
# LONG MESSAGE SENDER
# =========================

async def send_long_message(update, text):

    chunk_size = 3500

    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    for chunk in chunks:

        await update.message.reply_text(
            chunk
        )


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "👨‍💻 Help",
                callback_data="help"
            ),

            InlineKeyboardButton(
                "🔥 Features",
                callback_data="features"
            )
        ],

        [
            InlineKeyboardButton(
                "📡 Status",
                callback_data="status"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = """
👋 Welcome to Qwen Coder Bot

🚀 Your AI Coding Assistant

💡 Ask me:
• Build websites
• Fix errors
• Create APIs
• Make Telegram bots
• Generate HTML/CSS/JS
• Python help
"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )


# =========================
# BUTTONS
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "help":

        await query.message.reply_text(
            """
💡 HOW TO USE

Just send your coding question directly.

Examples:
• Build a login page
• Create weather API
• Fix Python error
• Make Telegram bot
• Generate portfolio website
"""
        )

    elif query.data == "features":

        await query.message.reply_text(
            """
🔥 FEATURES

✅ Coding Assistant
✅ Website Generator
✅ API Builder
✅ Telegram Bot Maker
✅ AI App Creator
✅ Debugging
✅ Long Response Support
✅ Multi-language Coding
"""
        )

    elif query.data == "status":

        await query.message.reply_text(
            "✅ Bot Status: ONLINE"
        )


# =========================
# MESSAGE HANDLER
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        answer = ask_qwen(user_text)

        if not answer:

            await update.message.reply_text(
                "❌ Empty response from AI."
            )

            return

        await send_long_message(update, answer)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{str(e)}"
        )


# =========================
# ERROR HANDLER
# =========================

async def error_handler(update, context):

    print(f"Error: {context.error}")


# =========================
# MAIN
# =========================

async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_error_handler(error_handler)

    print("✅ Qwen Coder Bot Running...")

    await app.initialize()

    await app.start()

    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())

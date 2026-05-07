import os
import requests
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

MODEL = "qwen/qwen-2.5-coder-32b-instruct"

SYSTEM_PROMPT = """
You are Qwen Coder Bot.
You are an expert coding assistant.
Help users with coding, websites, APIs, debugging and AI.
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
            "max_tokens": 2000,
        },
        timeout=120,
    )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except:
        return str(data)


# =========================
# MESSAGE SPLITTER
# =========================

async def send_long_message(update, text):

    chunk_size = 3500

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]

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
                "🧠 Features",
                callback_data="features"
            )
        ],

        [
            InlineKeyboardButton(
                "🚀 Status",
                callback_data="status"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome to Qwen Coder Bot!\n\nSend me any coding question.",
        reply_markup=reply_markup
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "help":

        await query.message.reply_text(
            "💡 Just send coding questions directly.\n\nExamples:\n- Build a login page\n- Fix Python error\n- Create API"
        )

    elif query.data == "features":

        await query.message.reply_text(
            "🔥 Features:\n\n• Coding Help\n• Debugging\n• API Building\n• Website Generation\n• AI Assistance"
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

    thinking = await update.message.reply_text(
        "⚡ Thinking..."
    )

    try:

        answer = ask_qwen(user_text)

        await thinking.delete()

        await send_long_message(update, answer)

    except Exception as e:

        await thinking.edit_text(
            f"❌ Error:\n{str(e)}"
        )


# =========================
# MAIN
# =========================

async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("✅ Bot running...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())

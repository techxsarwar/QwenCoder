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

# =========================================
# CONFIG
# =========================================

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

Always provide clean, modern and complete code.
"""

# =========================================
# MEMORY
# =========================================

user_memory = {}

# =========================================
# AI REQUEST
# =========================================

def ask_qwen(user_id, prompt):

    if user_id not in user_memory:

        user_memory[user_id] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    # Add user message
    user_memory[user_id].append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": user_memory[user_id],
            "temperature": 0.7,
            "max_tokens": 4000,
            "stream": False
        },
        timeout=180,
    )

    data = response.json()

    try:

        ai_reply = data["choices"][0]["message"]["content"]

        # Save AI response
        user_memory[user_id].append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

        # Keep memory optimized
        if len(user_memory[user_id]) > 20:

            user_memory[user_id] = (
                [user_memory[user_id][0]] +
                user_memory[user_id][-19:]
            )

        return ai_reply

    except:

        return str(data)


# =========================================
# LONG MESSAGE HANDLER
# =========================================

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


# =========================================
# START COMMAND
# =========================================

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
                "🧹 Clear Memory",
                callback_data="clear"
            ),

            InlineKeyboardButton(
                "📡 Status",
                callback_data="status"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
👋 Welcome to Qwen Coder Bot

🚀 Advanced AI Coding Assistant

💡 Ask me anything:
• Build websites
• Create APIs
• Make Telegram bots
• Fix coding bugs
• Generate HTML/CSS/JS
• Python & AI help
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


# =========================================
# BUTTONS
# =========================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

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

✅ AI Memory
✅ Coding Assistant
✅ Website Generator
✅ API Builder
✅ Telegram Bot Maker
✅ Debugging
✅ Long Response Support
✅ Multi-language Coding
"""
        )

    elif query.data == "status":

        await query.message.reply_text(
            "✅ Bot Status: ONLINE"
        )

    elif query.data == "clear":

        if user_id in user_memory:

            del user_memory[user_id]

        await query.message.reply_text(
            "🧹 Memory Cleared Successfully!"
        )


# =========================================
# MESSAGE HANDLER
# =========================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    user_id = update.effective_user.id

    try:

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        answer = ask_qwen(user_id, user_text)

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


# =========================================
# ERROR HANDLER
# =========================================

async def error_handler(update, context):

    print(f"Error: {context.error}")


# =========================================
# MAIN
# =========================================

async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

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

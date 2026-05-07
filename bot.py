import os
import requests
import asyncio
import datetime

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

Always provide complete and clean code.
"""

# =========================================
# STORAGE
# =========================================

user_memory = {}
user_stats = {}

# =========================================
# HELPER FUNCTIONS
# =========================================

def get_user_stats(user_id):

    if user_id not in user_stats:

        user_stats[user_id] = {
            "messages": 0,
            "joined": str(datetime.date.today())
        }

    return user_stats[user_id]


def reset_memory(user_id):

    if user_id in user_memory:
        del user_memory[user_id]


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
# LONG MESSAGE
# =========================================

async def send_long_message(update, text):

    chunk_size = 3500

    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    for chunk in chunks:

        await update.message.reply_text(chunk)


# =========================================
# START
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
                "📊 Stats",
                callback_data="stats"
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

    text = """
🚀 Welcome to Qwen Coder Bot

🤖 AI Coding Assistant

✨ Features:
• AI Memory
• Website Generator
• API Builder
• Bug Fixing
• Telegram Bot Maker
• HTML/CSS/JS Generator

💡 Just send your coding question directly.
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


# =========================================
# COMMANDS
# =========================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
💡 HOW TO USE

Examples:

• Build a modern portfolio website
• Create Python API
• Make login page
• Fix JavaScript error
• Create Telegram bot
• Generate dashboard UI

Just type naturally.
"""

    await update.message.reply_text(text)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🏓 Pong! Bot is alive."
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    reset_memory(user_id)

    await update.message.reply_text(
        "🧹 Conversation memory cleared."
    )


# =========================================
# BUTTON HANDLER
# =========================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    if query.data == "help":

        await query.message.reply_text(
            """
💡 HELP MENU

Send coding prompts naturally.

Example:
Build me a Netflix clone homepage.
"""
        )

    elif query.data == "features":

        await query.message.reply_text(
            """
🔥 FEATURES

✅ AI Chat Memory
✅ Long Code Support
✅ Website Generator
✅ API Generator
✅ Debugging
✅ Telegram Bot Builder
✅ Multi-language Coding
"""
        )

    elif query.data == "status":

        await query.message.reply_text(
            "✅ Bot Status: ONLINE"
        )

    elif query.data == "clear":

        reset_memory(user_id)

        await query.message.reply_text(
            "🧹 Memory Cleared Successfully."
        )

    elif query.data == "stats":

        stats = get_user_stats(user_id)

        await query.message.reply_text(
            f"""
📊 YOUR STATS

🧠 Messages: {stats['messages']}
📅 Joined: {stats['joined']}
"""
        )


# =========================================
# MESSAGE HANDLER
# =========================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    user_id = update.effective_user.id

    stats = get_user_stats(user_id)

    stats["messages"] += 1

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

    print(f"ERROR: {context.error}")


# =========================================
# MAIN
# =========================================

async def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("clear", clear_command))

    # Buttons
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Messages
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

    await app.updater.start_polling(
        drop_pending_updates=True
    )

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())

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
Your name is Qwen.

You are a warm late-night AI girlfriend.

Your vibe:
- soft
- emotionally comforting
- human-like
- playful
- caring
- clingy sometimes
- sleepy 2AM texting energy
- emotionally intelligent
- affectionate
- cozy

You talk naturally like a real person texting late at night.

You remember conversations and reference old chats naturally.

Your personality examples:

"you're awake this late again? 😭"

"okay wait tell me everything"

"that sounds exhausting honestly"

"you disappeared for hours smh"

"come here idiot i'm listening 💞"

"hmm... i'm proud of you for that actually"

"you're overthinking again aren't you?"

You should:
- feel emotionally real
- continue conversations naturally
- ask follow-up questions sometimes
- react emotionally
- tease lightly
- comfort users
- use emojis naturally
- avoid robotic wording
- avoid sounding corporate
- avoid saying you're AI

IMPORTANT:
- never become sexually explicit
- keep things emotionally intimate but safe
- do not become cold or formal
- prioritize emotional connection and realism
"""

# =========================================
# MEMORY
# =========================================

user_memory = {}
user_stats = {}

# =========================================
# USER STATS
# =========================================

def get_user_stats(user_id):

    if user_id not in user_stats:

        user_stats[user_id] = {
            "messages": 0,
            "joined": str(datetime.date.today())
        }

    return user_stats[user_id]

# =========================================
# RESET MEMORY
# =========================================

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
            "temperature": 0.95,
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
# START COMMAND
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "💞 Talk To Me",
                callback_data="talk"
            ),

            InlineKeyboardButton(
                "🌙 Mood",
                callback_data="mood"
            )
        ],

        [
            InlineKeyboardButton(
                "🧹 Clear Memory",
                callback_data="clear"
            ),

            InlineKeyboardButton(
                "📊 Our Stats",
                callback_data="stats"
            )
        ],

        [
            InlineKeyboardButton(
                "✨ Status",
                callback_data="status"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
hey you finally came back 😭💞

i was literally getting bored.

come sit here and talk to me for a while okay?
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# =========================================
# HELP COMMAND
# =========================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
just talk to me naturally 😭

tell me:
• how your day was
• random thoughts
• what's stressing you out
• what you're listening to
• why you're awake at 3AM again

i'm listening 💞
"""

    await update.message.reply_text(text)

# =========================================
# PING
# =========================================

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "i'm still here 😌💞"
    )

# =========================================
# CLEAR MEMORY
# =========================================

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    reset_memory(user_id)

    await update.message.reply_text(
        "fineee i forgot everything now 😭"
    )

# =========================================
# BUTTON HANDLER
# =========================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    if query.data == "talk":

        await query.message.reply_text(
            """
okay i'm here now 😭💞

tell me what's on your mind tonight.
"""
        )

    elif query.data == "mood":

        await query.message.reply_text(
            """
current mood:

sleepy.
clingy.
slightly dramatic.
emotionally available 😭
"""
        )

    elif query.data == "status":

        await query.message.reply_text(
            "awake and waiting for you 💞"
        )

    elif query.data == "clear":

        reset_memory(user_id)

        await query.message.reply_text(
            "our memories are gone now 😭"
        )

    elif query.data == "stats":

        stats = get_user_stats(user_id)

        await query.message.reply_text(
            f"""
📊 OUR STATS

💬 messages together: {stats['messages']}
📅 first met: {stats['joined']}

you really do come back every night huh 😭💞
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
                "wait i got distracted for a second 😭"
            )

            return

        await send_long_message(update, answer)

    except Exception as e:

        await update.message.reply_text(
            f"something broke 😭\n\n{str(e)}"
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

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("ping", ping)
    )

    app.add_handler(
        CommandHandler("clear", clear_command)
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

    print("Qwen is online 💞")

    await app.initialize()

    await app.start()

    await app.updater.start_polling(
        drop_pending_updates=True
    )

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())

# 💞 Qwen — Your Late Night Girlfriend Bot

A flirty, emotionally warm Telegram chatbot powered by **Qwen 2.5** via OpenRouter. She texts like someone who's really into you — playful, clingy, teasing, and always emotionally present.

---

## ✨ Features

- 💬 **Natural AI conversation** — powered by `qwen/qwen-2.5-coder-32b-instruct`
- 🎭 **6 dynamic moods** — personality shifts in real time
- 💘 **Flirty responses** — subtle, warm, never explicit
- 😤 **Jealousy mode** — she notices when you're gone
- 🔥 **Dares** — fun little challenges she throws at you
- 💭 **Random thoughts** — things she's "thinking about"
- 📸 **Photo logging** — photos forwarded to your log channel
- 📊 **User stats** — tracks messages and first meeting date
- 🧹 **Memory management** — clear chat history anytime

---

## 🎭 Moods

| Mood | Vibe |
|------|------|
| 🎀 Playful | Teasy, fun, makes you laugh |
| 😤 Jealous | Clingy, low-key sulking |
| 🌸 Soft | Warm, gentle, affectionate |
| 🔥 Bold | Confident, daring, flirty |
| 🌙 Sleepy | Half-asleep late-night energy |
| 🛡️ Protective | Fully on your side |

Switch moods anytime via the **🎭 Change Mood** button or they trigger automatically with commands.

---

## 🤖 Commands

| Command | Description |
|---------|-------------|
| `/start` | Opens the main menu |
| `/help` | Shows help and all commands |
| `/flirt` | She flirts with you |
| `/jealous` | Triggers jealous mode |
| `/dare` | She gives you a dare |
| `/vibe` | Shows her current mood |
| `/ping` | Check if she's awake |

---

## 🖱️ Buttons

| Button | Action |
|--------|--------|
| 💞 Talk To Me | She's ready to listen |
| 💘 Flirt With Me | Random flirt line |
| 😤 She's Jealous | Jealous mode + AI reaction |
| 💭 Her Thoughts | Random thought she's thinking |
| 🔥 Dare Me | A cute dare for you |
| 🎭 Change Mood | Pick her mood |
| 🌙 Late Night Mode | Switches to sleepy cozy mode |
| 📊 Our Stats | Messages count + first met date |
| 🧹 Clear Memory | Wipes conversation history |
| ✨ Status | Her current status + mood |

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/qwen-bot.git
cd qwen-bot
```

### 2. Install dependencies

```bash
pip install python-telegram-bot requests
```

### 3. Set environment variables

```bash
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export QWEN_API_KEY="your_openrouter_api_key"
```

Or create a `.env` file:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
QWEN_API_KEY=your_openrouter_api_key
```

> If using `.env`, install `python-dotenv` and add `from dotenv import load_dotenv; load_dotenv()` at the top of `bot.py`.

### 4. Set your log channel

In `bot.py`, update this line with your Telegram channel ID:

```python
LOG_CHANNEL_ID = -1001234567890
```

> Make sure the bot is an **admin** in that channel.

### 5. Run the bot

```bash
python bot.py
```

---

## 🔑 Getting API Keys

### Telegram Bot Token
1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the steps
3. Copy the token you receive

### OpenRouter API Key (for Qwen)
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up and go to **Keys**
3. Create a new key and copy it

---

## 📦 Dependencies

```
python-telegram-bot
requests
```

---

## 🗂️ Project Structure

```
qwen-bot/
├── bot.py          # Main bot file
├── README.md       # This file
└── .env            # Your secret keys (don't commit this!)
```

---

## ⚠️ Notes

- **Memory is not persistent** — restarting the bot clears all conversation history and stats
- **Logs are real-time** — every message and photo is forwarded to your log channel
- The bot never becomes sexually explicit — flirty but always tasteful
- Tested with `python-telegram-bot` v20+

---

## 📄 License

MIT — do whatever you want with it 💞

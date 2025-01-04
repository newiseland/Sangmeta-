from pyrogram import Client
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.handlers import tracker, commands

app = Client("SangMataBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Import handlers
tracker.register_handlers(app)
commands.register_handlers(app)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()

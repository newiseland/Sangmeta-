import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN  # Import from config

# Set up logging to debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the bot using the values loaded from config.py
app = Client("SangMetaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Track user history (In-memory dictionary or DB)
user_data = {}

# Command: /start
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("Hello! I track Telegram user history. Send any message and I'll track you.")

# Track all messages and save user history
@app.on_message(filters.text & ~filters.command("start"))
async def track_user(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"
    
    # If user is not in the dictionary, initialize their data
    if user_id not in user_data:
        user_data[user_id] = {
            "messages": 0,
            "username": username,
            "name": message.from_user.first_name,
            "chat_ids": set()
        }
    
    # Update message count and store chat info
    user_data[user_id]["messages"] += 1
    user_data[user_id]["chat_ids"].add(message.chat.id)

    # Logging user message history
    logger.info(f"User: {user_data[user_id]['name']} (ID: {user_id}), Messages: {user_data[user_id]['messages']}")

# Command: /history <user_id>
@app.on_message(filters.command("history"))
async def get_user_history(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: /history <user_id>")
        return

    try:
        user_id = int(message.command[1])
        if user_id in user_data:
            user_info = user_data[user_id]
            history = (
                f"User: {user_info['name']} ({user_info['username']})\n"
                f"Messages Sent: {user_info['messages']}\n"
                f"Chats Participated: {len(user_info['chat_ids'])}\n"
            )
            await message.reply(history)
        else:
            await message.reply("No history found for this user.")
    except ValueError:
        await message.reply("Invalid user ID.")

# Command: /join_channel
@app.on_message(filters.command("join_channel"))
async def join_channel(client: Client, message: Message):
    channel_link = "https://t.me/your_channel"  # Replace with your channel link
    try:
        await message.reply(
            text=f"Join our channel to track more user history!\n{channel_link}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Channel", url=channel_link)]
            ])
        )
    except Exception as e:
        logger.error(f"Error sending join message: {e}")
        await message.reply("Could not send the join message, please try again later.")

# Function to track new users joining the bot
@app.on_message(filters.new_chat_members)
async def new_user(client: Client, message: Message):
    for new_user in message.new_chat_members:
        user_data[new_user.id] = {
            "messages": 0,
            "username": new_user.username or "No Username",
            "name": new_user.first_name,
            "chat_ids": {message.chat.id}
        }
        await message.reply(f"Welcome {new_user.first_name}! I will track your messages here.")

# Run the bot
if __name__ == "__main__":
    app.run()

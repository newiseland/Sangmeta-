from pyrogram import Client, filters
import sqlite3

# Bot Configuration
API_ID = "your_api_id"  # Get from my.telegram.org
API_HASH = "your_api_hash"  # Get from my.telegram.org
BOT_TOKEN = "your_bot_token"  # Get from BotFather

# Initialize Bot
app = Client("SangMataClone", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize Database
conn = sqlite3.connect("user_changes.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS user_changes (user_id INTEGER, username TEXT, name TEXT, date TEXT)")

# Track User Changes
@app.on_message(filters.group & filters.new_chat_members)
async def track_new_members(client, message):
    for member in message.new_chat_members:
        user_id = member.id
        username = member.username or "No Username"
        name = member.first_name
        cursor.execute("INSERT INTO user_changes VALUES (?, ?, ?, datetime('now'))", (user_id, username, name))
        conn.commit()
        await message.reply(f"Tracking {name} (@{username}) for changes!")

@app.on_message(filters.group & filters.command("history"))
async def get_user_history(client, message):
    if not message.reply_to_message:
        await message.reply("Reply to a user's message to get their history!")
        return

    user_id = message.reply_to_message.from_user.id
    cursor.execute("SELECT * FROM user_changes WHERE user_id = ?", (user_id,))
    records = cursor.fetchall()

    if not records:
        await message.reply("No history found for this user.")
        return

    history = "\n".join(
        [f"Name: {rec[2]}, Username: @{rec[1]} (Logged: {rec[3]})" for rec in records]
    )
    await message.reply(f"Change History for {message.reply_to_message.from_user.first_name}:\n\n{history}")

# Start Bot
app.run()

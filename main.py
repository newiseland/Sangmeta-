from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import sqlite3
import os
from datetime import datetime

# Configuration
API_ID = int(os.getenv("API_ID", "24912072"))  # Replace YOUR_API_ID
API_HASH = os.getenv("API_HASH", "1a9c568007ef51bed8fd2357947e5cb3")  # Replace YOUR_API_HASH
BOT_TOKEN = os.getenv("BOT_TOKEN", "7727337046:AAFURd1egV8eNUuVF9s39Bn7OI7ox5ykPBg")  # Replace YOUR_BOT_TOKEN

# Initialize bot
app = Client("sangmata_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Database setup
if not os.path.exists("history.db"):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_history (
            user_id INTEGER,
            name TEXT,
            username TEXT,
            change_time TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Middleware: Track user data changes
@app.on_message(filters.private | filters.group)
async def track_user_changes(client: Client, message: Message):
    user = message.from_user
    if not user:
        return

    user_id = user.id
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = user.username or "None"

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, username FROM user_history WHERE user_id = ? ORDER BY change_time DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()

    if result:
        last_name, last_username = result
        if full_name != last_name or username != last_username:
            cursor.execute("""
                INSERT INTO user_history (user_id, name, username, change_time)
                VALUES (?, ?, ?, ?)
            """, (user_id, full_name, username, datetime.now()))
    else:
        # New user
        cursor.execute("""
            INSERT INTO user_history (user_id, name, username, change_time)
            VALUES (?, ?, ?, ?)
        """, (user_id, full_name, username, datetime.now()))

    conn.commit()
    conn.close()

# /start command
@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "👋 Welcome to the SangMata Bot!\n\n"
        "This bot tracks username and name changes of Telegram users. Use `/history` to view your history, or `/find <user_id>` to find history of other users.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Source Code", url="https://github.com/YourRepo")]
        ])
    )

# /history command: View personal history
@app.on_message(filters.command("history"))
async def view_history(client: Client, message: Message):
    user_id = message.from_user.id

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, username, change_time
        FROM user_history
        WHERE user_id = ?
        ORDER BY change_time DESC
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()

    if records:
        history = f"📜 **History of Changes for {message.from_user.first_name}:**\n\n"
        for name, username, time in records:
            history += f"• Name: `{name}`\n  Username: `{username}`\n  Time: {time}\n\n"
        await message.reply_text(history)
    else:
        await message.reply_text("No history found for your account.")

# /find command: View history of other users
@app.on_message(filters.command("find"))
async def find_user_history(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a user ID. Usage: `/find <user_id>`")
        return

    user_id = int(message.command[1])

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, username, change_time
        FROM user_history
        WHERE user_id = ?
        ORDER BY change_time DESC
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()

    if records:
        history = f"📜 **History of Changes for User {user_id}:**\n\n"
        for name, username, time in records:
            history += f"• Name: `{name}`\n  Username: `{username}`\n  Time: {time}\n\n"
        await message.reply_text(history)
    else:
        await message.reply_text(f"No history found for user ID `{user_id}`.")

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()

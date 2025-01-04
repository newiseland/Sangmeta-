from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import os
import sqlite3

# Configuration: Replace these values with your own
API_ID = int(os.getenv("API_ID", "24912072")  # Replace YOUR_API_ID with your Telegram API ID
API_HASH = os.getenv("API_HASH", "1a9c568007ef51bed8fd2357947e5cb3")  # Replace YOUR_API_HASH with your Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "7727337046:AAFURd1egV8eNUuVF9s39Bn7OI7ox5ykPBg")  # Replace YOUR_BOT_TOKEN with your Bot Token

# Initialize the bot
app = Client("SangMetaBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Database setup
if not os.path.exists("history.db"):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            last_seen TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE username_changes (
            user_id INTEGER,
            old_username TEXT,
            new_username TEXT,
            change_time TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)
    conn.commit()
    conn.close()

# Function to log changes in the database
def log_change(user_id, old_username, new_username):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO username_changes (user_id, old_username, new_username, change_time)
        VALUES (?, ?, ?, ?)
    """, (user_id, old_username, new_username, datetime.now()))
    conn.commit()
    conn.close()

# Middleware to track changes
@app.on_message(filters.private & ~filters.service)
async def track_user_changes(client: Client, message: Message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    username = user.username

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()

    if data:
        # Check for username changes
        old_username = data[0]
        if old_username != username:
            log_change(user_id, old_username, username)
            cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
    else:
        # New user
        cursor.execute("INSERT INTO users (user_id, first_name, username, last_seen) VALUES (?, ?, ?, ?)",
                       (user_id, first_name, username, datetime.now()))

    conn.commit()
    conn.close()

# Command to display username history
@app.on_message(filters.command("history") & filters.private)
async def show_history(client: Client, message: Message):
    user_id = message.from_user.id

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT old_username, new_username, change_time FROM username_changes
        WHERE user_id = ? ORDER BY change_time DESC
    """, (user_id,))
    changes = cursor.fetchall()
    conn.close()

    if changes:
        history_text = "📜 **Username History:**\n\n"
        for old_username, new_username, change_time in changes:
            history_text += f"• `{old_username or 'None'}` → `{new_username or 'None'}` at {change_time}\n"
        await message.reply_text(history_text)
    else:
        await message.reply_text("No username changes found for your account.")

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    await message.reply_text(
        text="👋 Welcome to SangMata Bot!\n\n"
             "This bot tracks your username changes and displays them using the /history command.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Developer", url="https://t.me/YourUsername")]]
        )
    )

# Run the bot
if __name__ == "__main__":
    print("Bot is starting...")
    app.run()

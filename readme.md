# SangMata-BOT

SangMata-BOT is a Telegram bot that tracks username and profile changes in groups.

## Deploy to Heroku

Click the button below to deploy this bot to Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/newiseland/Sangmeta-)

---

### How to Use

1. **Get Telegram API Credentials**:
   - Go to [my.telegram.org](https://my.telegram.org) and create an application to get your `API_ID` and `API_HASH`.

2. **Get Bot Token**:
   - Use [BotFather](https://t.me/BotFather) on Telegram to create a bot and obtain the `BOT_TOKEN`.

3. **Deploy on Heroku**:
   - Click the "Deploy to Heroku" button above.
   - Fill in the required environment variables.

4. **Run Locally**:
   ```bash
   git clone https://github.com/yourusername/sangmata-bot.git
   cd sangmata-bot
   pip install -r requirements.txt
   python bot/main.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Read environment variables
API_ID = os.getenv("8048988286")
API_HASH = os.getenv("b35b715fe8dc0a58e8048988286fc5b6")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("mongodb+srv://BADMUNDA:BADMYDAD@badhacker.i5nw9na.mongodb.net/")  # Optional, if you are using a database

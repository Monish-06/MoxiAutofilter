import os
from dotenv import load_dotenv
from pyrogram import Client
from keep_alive import keep_alive

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins={"root": "handlers"})

if __name__ == "__main__":
    keep_alive()
    app.run()

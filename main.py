import threading
from pyrogram import Client
from keep_alive import keep_alive
from dotenv import load_dotenv
from handlers.index_handler import register_handlers
from handlers.filter_handler import *
import os

load_dotenv()

app = Client("MoxiBot", api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"),
             bot_token=os.getenv("BOT_TOKEN"))

register_handlers(app)

if __name__ == "__main__":
    keep_alive()
    app.run()

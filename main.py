import threading
from pyrogram import Client
from keep_alive import keep_alive
from handlers.index_handler import *
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file


app = Client("MoxiBot", api_id=int(os.environ["API_ID"]),
             api_hash=os.environ["API_HASH"],
             bot_token=os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    keep_alive()  # Start Flask keep-alive
    app.run()

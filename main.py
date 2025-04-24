import asyncio
import os
from pyrogram import Client
from dotenv import load_dotenv
import threading
import requests
import time

# Load environment variables
load_dotenv()

# === Keep-Alive Function ===
def keep_alive():
    while True:
        try:
            requests.get("https://scornful-andreana-moxi35-c66f799a.koyeb.app/")
        except:
            pass
        time.sleep(90)

# Start keep-alive in background thread
threading.Thread(target=keep_alive, daemon=True).start()

# === Bot Setup ===
bot = Client(
    "MoxiFilterBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH")),
    bot_token=os.getenv("BOT_TOKEN"),
    plugins={"root": "handlers"},
)

if __name__ == "__main__":
    print("Starting MoxiFilterBot...")
    bot.run()

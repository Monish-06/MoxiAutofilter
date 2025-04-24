import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

plugins = dict(root="handlers")

app = Client(
    "MoxiBot",
    bot_token=os.getenv("BOT_TOKEN"),
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    plugins=plugins
)

if __name__ == "__main__":
    from keep_alive import keep_alive
    keep_alive()
    print("Bot is running...")
    app.run()

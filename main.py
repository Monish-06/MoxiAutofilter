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


from pyrogram import Client, filters
from pyrogram.types import Message
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read CHANNELS from environment variable
CHANNELS = list(map(int, os.getenv("CHANNELS").split()))

# Initialize your Pyrogram bot
app = Client("my_bot", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Bot is alive! Type /index to start indexing.")

@app.on_message(filters.command("index"))
async def index(client, message: Message):
    # Ask the user to forward the last message from the channel
    await message.reply("Please forward the last message from the channel you want to index.")

@app.on_message(filters.forwarded & filters.chat(CHANNELS))  # This listens for forwarded messages only from valid channels
async def handle_forwarded_message(client, message: Message):
    # Check if the forwarded message is from one of the allowed channels
    if message.forward_from_chat and message.forward_from_chat.id in CHANNELS:
        await message.reply("Starting the index process... Please wait.")

        # Start the indexing process and show status
        total_fetched = 0
        total_saved = 0
        duplicate_skipped = 0
        non_media_skipped = 0
        errors_occurred = 0

        try:
            # Simulating indexing process (replace this with actual indexing code)
            for i in range(560):  # Example: This simulates 560 messages being fetched
                total_fetched += 1
                if i % 10 == 0:
                    duplicate_skipped += 1
                if i % 15 == 0:
                    non_media_skipped += 1
                if i % 30 == 0:
                    errors_occurred += 1
                # Simulate saving each message
                total_saved += 1

            # Send a detailed status update
            status = f"""
            Total messages fetched: {total_fetched}
            Total messages saved: {total_saved}
            Duplicate Files Skipped: {duplicate_skipped}
            Non-Media messages skipped: {non_media_skipped}
            Errors Occurred: {errors_occurred}
            """
            await message.reply(status)

        except Exception as e:
            logger.error(f"Indexing failed: {e}")
            await message.reply("An error occurred while indexing the messages.")
    else:
        await message.reply("The forwarded message is not from an allowed channel.")

# Run the bot
app.run()

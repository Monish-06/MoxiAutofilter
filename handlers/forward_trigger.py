from pyrogram import Client, filters
from pyrogram.types import Message
from modules.file_indexer import index_existing_files
import os

CHANNELS = list(map(int, os.getenv("CHANNELS").split()))
ADMINS = list(map(int, os.getenv("ADMINS").split()))

@Client.on_message(filters.forwarded & filters.private & filters.user(ADMINS))
async def start_indexing(client: Client, message: Message):
    if message.forward_from_chat and message.forward_from_chat.id in CHANNELS:
        await message.reply_text("Started indexing files from the channel. This may take a while...")

        try:
            await index_existing_files(client, message.forward_from_chat.id)
            await message.reply_text("✅ Indexing complete!")
        except Exception as e:
            await message.reply_text(f"❌ Indexing failed!\n`{e}`")
    else:
        await message.reply_text("Please forward a message from one of the allowed file channels.")

from pyrogram import Client, filters
from pyrogram.types import Message
import os
from pymongo import MongoClient

CHANNELS = list(map(int, os.getenv("CHANNELS").split()))
MONGO_URI = os.getenv("MONGO_URI")
DB = MongoClient(MONGO_URI).filesbot
FILES = DB.files

indexing_state = {}

@Client.on_message(filters.command("start") & filters.private)
async def start(_, msg):
    await msg.reply("Hello! I'm alive and ready.")

@Client.on_message(filters.command("index") & filters.private)
async def ask_forward(_, msg):
    indexing_state[msg.from_user.id] = {"awaiting_forward": True}
    await msg.reply("Please forward the last message from the channel you want to index.")

@Client.on_message(filters.forwarded & filters.private)
async def handle_forwarded(_, msg: Message):
    user_id = msg.from_user.id

    if not indexing_state.get(user_id, {}).get("awaiting_forward"):
        return

    channel_id = msg.forward_from_chat.id if msg.forward_from_chat else None

    if channel_id not in CHANNELS:
        await msg.reply("This channel is not in the allowed list.")
        return

    await msg.reply("Starting indexing... This may take time.")

    indexing_state[user_id]["awaiting_forward"] = False

    stats = {
        "total": 0,
        "saved": 0,
        "duplicates": 0,
        "deleted": 0,
        "unsupported": 0,
        "non_media": 0,
        "errors": 0,
    }

    async for message in _.iter_history(channel_id, offset_id=msg.forward_from_message_id):
        stats["total"] += 1

        if message.empty or message.service:
            stats["deleted"] += 1
            continue

        if not message.media:
            stats["non_media"] += 1
            continue

        file_id = (
            str(message.document.file_id) if message.document else
            str(message.video.file_id) if message.video else
            str(message.audio.file_id) if message.audio else
            str(message.photo.file_id) if message.photo else None
        )

        if not file_id:
            stats["unsupported"] += 1
            continue

        exists = FILES.find_one({"file_id": file_id})
        if exists:
            stats["duplicates"] += 1
            continue

        try:
            FILES.insert_one({
                "file_id": file_id,
                "caption": message.caption,
                "chat_id": message.chat.id,
                "message_id": message.message_id,
                "type": message.media,
            })
            stats["saved"] += 1
        except Exception as e:
            stats["errors"] += 1

        if stats["total"] % 100 == 0:
            await msg.reply_text(f"Fetched: {stats['total']} | Saved: {stats['saved']}...")

    await msg.reply_text(f"""
<b>Indexing Complete</b>
Total messages fetched: <code>{stats['total']}</code>
Total messages saved: <code>{stats['saved']}</code>
Duplicate Files Skipped: <code>{stats['duplicates']}</code>
Deleted Messages Skipped: <code>{stats['deleted']}</code>
Non-Media Messages Skipped: <code>{stats['non_media']}</code> (Unsupported Media: <code>{stats['unsupported']}</code>)
Errors Occurred: <code>{stats['errors']}</code>
""", parse_mode="html")

from pyrogram import Client, filters
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

# MongoDB setup
mongo = MongoClient(os.getenv("MONGO_URI"))
db = mongo[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

# Allowed channels
ALLOWED_CHANNELS = list(map(int, os.getenv("CHANNELS").split()))
user_indexing_state = {}

def register_handlers(app: Client):
    @app.on_message(filters.command("start"))
    async def start_cmd(_, msg):
        await msg.reply("Hey! Bot is alive and ready.")

    @app.on_message(filters.command("index"))
    async def index_cmd(_, msg):
        user_indexing_state[msg.from_user.id] = {"status": "waiting_for_forward"}
        await msg.reply("Now please forward the **last message** from the channel you want to index.")

    @app.on_message(filters.forwarded & filters.private)
    async def handle_forwarded_message(bot, msg):
        user_id = msg.from_user.id
        state = user_indexing_state.get(user_id, {})

        if state.get("status") != "waiting_for_forward":
            return

        forwarded_chat_id = msg.forward_from_chat.id

        if forwarded_chat_id not in ALLOWED_CHANNELS:
            await msg.reply("This channel is not allowed.")
            user_indexing_state.pop(user_id, None)
            return

        await msg.reply("Starting indexing...")

        total = saved = skipped = errors = 0
        messages = []

        try:
            async for m in bot.get_chat_history(forwarded_chat_id, limit=100, offset_id=msg.forward_from_message_id - 1):
                messages.append(m)
        except Exception as e:
            await msg.reply(f"Error while fetching messages: {e}")
            return

        messages.reverse()

        for m in messages:
            total += 1
            try:
                if m.media:
                    file_id = None
                    file_name = None

                    if m.document:
                        file_id = m.document.file_id
                        file_name = m.document.file_name
                    elif m.video:
                        file_id = m.video.file_id
                        file_name = m.video.file_name or "video.mp4"
                    elif m.audio:
                        file_id = m.audio.file_id
                        file_name = m.audio.file_name or "audio.mp3"
                    elif m.photo:
                        file_id = m.photo.file_id
                        file_name = "photo.jpg"
                    else:
                        skipped += 1
                        continue

                    if collection.find_one({"file_id": file_id}):
                        skipped += 1
                        continue

                    collection.insert_one({
                        "file_id": file_id,
                        "file_name": file_name,
                        "caption": m.caption or "",
                        "chat_id": forwarded_chat_id,
                        "message_id": m.message_id
                    })
                    saved += 1
                else:
                    skipped += 1

            except Exception as e:
                print("Error:", e)
                errors += 1

        user_indexing_state.pop(user_id, None)

        await msg.reply(
            f"**Indexing Complete**\n\n"
            f"Total messages fetched: {total}\n"
            f"Saved: {saved}\n"
            f"Skipped (duplicates/unsupported): {skipped}\n"
            f"Errors: {errors}"
        )

from pymongo import MongoClient
import os

# Connect using your existing DB and collection from .env
client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["DB_NAME"]]
files_collection = db[os.environ["COLLECTION_NAME"]]

index_router = Client("indexer")

@filters.command("start") & filters.private
async def start_handler(client, message):
    await message.reply("Hey! I'm alive and ready to index your channels.")

@filters.command("index") & filters.private
async def index_command(client, message):
    await message.reply("Please forward the last message of the channel you want to index.")

@filters.forwarded & filters.private
async def handle_forwarded(client, message: Message):
    fwd = message.forward_from_chat
    if not fwd:
        return await message.reply("That's not a forwarded message.")

    if str(fwd.id) not in os.environ["CHANNELS"]:
        return await message.reply("This channel is not allowed for indexing.")

    await message.reply("Starting to index... Please wait.")

    saved, skipped, errors = 0, 0, 0
    async for msg in client.get_chat_history(fwd.id, reverse=True):
        if msg.media:
            file_id = getattr(msg, msg.media.value).file_id
            data = {
                "file_id": file_id,
                "caption": msg.caption,
                "channel_id": fwd.id,
                "message_id": msg.message_id,
                "media_type": msg.media.value
            }
            try:
                if not files_collection.find_one({"file_id": file_id}):
                    files_collection.insert_one(data)
                    saved += 1
                else:
                    skipped += 1
            except:
                errors += 1
        else:
            skipped += 1

    await message.reply_text(f"""**Indexing Complete**

Total Messages Fetched: {saved + skipped + errors}
Total Files Saved: {saved}
Duplicates Skipped: {skipped}
Errors: {errors}
""")

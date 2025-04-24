import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("DATABASE_URI")
DB_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def save_file(message):
    if not message.document:
        return

    file_info = {
        "_id": str(message.document.file_id),
        "file_name": message.document.file_name,
        "file_size": message.document.file_size,
        "mime_type": message.document.mime_type,
        "caption": message.caption,
        "chat_id": message.chat.id,
        "message_id": message.id
    }
    await collection.update_one(
        {"_id": file_info["_id"]},
        {"$set": file_info},
        upsert=True
    )

async def index_existing_files(client, channel_id):
    async for msg in client.get_chat_history(channel_id, limit=None):
        if msg.document:
            await save_file(msg)

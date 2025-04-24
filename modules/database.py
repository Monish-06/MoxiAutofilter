import os
import motor.motor_asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB URI and DB Name
DATABASE_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Establish MongoDB client connection
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

async def store_file_metadata(file_id, file_name, file_size, file_type, mime_type, caption=None, file_ref=None):
    """ Store file metadata in MongoDB """
    try:
        file_data = {
            "file_id": file_id,
            "file_name": file_name,
            "file_size": file_size,
            "file_type": file_type,
            "mime_type": mime_type,
            "caption": caption,
            "file_ref": file_ref,
        }
        # Insert the file metadata into the collection
        await collection.insert_one(file_data)
        return True
    except Exception as e:
        print(f"Error storing file metadata: {e}")
        return False

async def get_file_metadata(file_id):
    """ Retrieve file metadata by file_id """
    try:
        file_data = await collection.find_one({"file_id": file_id})
        return file_data
    except Exception as e:
        print(f"Error retrieving file metadata: {e}")
        return None

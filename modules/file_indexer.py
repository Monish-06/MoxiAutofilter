import logging
from pyrogram import Client, filters
from .database import store_file_metadata, get_file_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This function will handle storing the metadata of each file
async def handle_new_file(client: Client, message):
    """ Store file metadata when a new file is posted or forwarded. """
    try:
        if message.document:
            file_id = message.document.file_id
            file_name = message.document.file_name
            file_size = message.document.file_size
            file_type = message.document.mime_type
            mime_type = message.document.mime_type
            caption = message.caption
            file_ref = message.forward_from.id if message.forward_from else None

            # Check if file already exists in the database
            existing_file = await get_file_metadata(file_id)
            if not existing_file:
                # Store the file metadata in the database
                await store_file_metadata(file_id, file_name, file_size, file_type, mime_type, caption, file_ref)
                logger.info(f"Stored file metadata for: {file_name}")
            else:
                logger.info(f"File {file_name} already exists in the database.")
    except Exception as e:
        logger.error(f"Error while handling new file: {e}")

# Function to start the file indexing from the last message
async def start_indexing(client: Client, message):
    """ Start indexing files from the last forwarded message """
    try:
        if message.document:
            # Get the last message's document and start indexing
            logger.info("Starting to index files.")
            await handle_new_file(client, message)

        # Set the bot to listen to future messages
        await client.add_handler(filters.document, handle_new_file)
    except Exception as e:
        logger.error(f"Error starting file indexing: {e}")

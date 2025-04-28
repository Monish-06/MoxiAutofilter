from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from dotenv import load_dotenv
import os
from database import find_files  # You already have this function to search files in MongoDB
from helpers.shortlink import get_shortlink  # Your safelink function
import asyncio
import re

GROUP = os.getenv('GROUP')
CHANNEL = os.getenv('CHANNEL')

# Your group username without @
GROUP_LINK = f"https://t.me/{GROUP}"

# Set of trigger words to ignore in PM
GROUP_ONLY = filters.group

# Function to guess language, season, episode
def extract_filters(filename):
    filters = {}
    filename_lower = filename.lower()

    # Language
    if "tam" in filename_lower:
        filters["language"] = "tam"
    elif "mal" in filename_lower:
        filters["language"] = "mal"
    elif "hin" in filename_lower:
        filters["language"] = "hin"

    # Season
    season_match = re.search(r'(s\d{1,2})', filename_lower)
    if season_match:
        filters["season"] = season_match.group(1)

    # Episode
    episode_match = re.search(r'(e\d{1,2})', filename_lower)
    if episode_match:
        filters["episode"] = episode_match.group(1)

    return filters

# Main search handler
@Client.on_message(GROUP_ONLY & filters.text)
async def search_handler(client, message: Message):
    query = message.text
    print(f"Received query: {query}")  # Log the incoming message

    results = await find_files(query)
    if not results:
        print("No results found.")
        return

    print(f"Found results: {results}")  # Log the results

    buttons = []
    for file in results:
        filters_detected = extract_filters(file["file_name"])
        file_id = file["file_id"]

        start_payload = f"files_{file_id}"
        telegram_link = f"https://telegram.dog/{client.me.username}?start={start_payload}"
        safe_link = await get_shortlink(telegram_link)

        btn_text = file["file_name"][:50]
        buttons.append([InlineKeyboardButton(text=btn_text, url=safe_link)])

    buttons.insert(0, [InlineKeyboardButton("How to Download?", url="https://t.me/your_download_tutorial_link")])

    if len(buttons) > 10:
        buttons = buttons[:10]

    reply_markup = InlineKeyboardMarkup(buttons)
    sent = await message.reply(
        "**Here are your search results!**",
        reply_markup=reply_markup,
        quote=True
    )

    await asyncio.sleep(300)
    try:
        await sent.edit(
            "**Oops, search expired!\nSend again to get fresh links!**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Group", url=GROUP_LINK)]]
            )
        )
    except Exception as e:
        print(e)



# Handle start command from link
@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Hello! Please search files in group.")
        return

    payload = message.command[1]

    if payload.startswith("files_"):
        file_id = payload.split("_", 1)[1]

        try:
            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_id
            )
            sent = await message.reply("**Here’s your file!**", quote=True)

            # Delete after 20 minutes
            await asyncio.sleep(1200)
            await sent.delete()
            await message.reply(
                "**File deleted!\nRequest again in group!**",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Group", url=GROUP_LINK)]]
                )
            )
        except Exception as e:
            await message.reply("**Failed to send file. Try again!**")

from flask import Flask
import threading
from pyrogram import Client
import os
from keep_alive import keep_alive  # Import the keep_alive function from keep_alive.py

# Initialize Flask app
app = Flask(__name__)

# Define a health check route
@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200  # Koyeb will check this endpoint

# Run Flask server in a separate thread to keep it running alongside the bot
def run_flask():
    app.run(host="0.0.0.0", port=8080)  # Ensure Flask listens on port 8080

# Initialize your Pyrogram bot
def run_bot():
    bot = Client("my_bot", api_id="your_api_id", api_hash="your_api_hash", bot_token="your_bot_token")
    bot.run()  # Start the bot

if __name__ == "__main__":
    # Start Flask server in the background
    threading.Thread(target=run_flask, daemon=True).start()

    # Start keep_alive in a separate thread
    threading.Thread(target=keep_alive, daemon=True).start()

    # Start the bot
    run_bot()

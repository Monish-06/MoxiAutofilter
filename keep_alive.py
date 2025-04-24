import threading
import requests
import time
from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Koyeb will use this to check if your app is alive
@app.route("/", methods=["GET"])
def home():
    return "Bot is alive!", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

def ping_self():
    while True:
        try:
            requests.get("https://scornful-andreana-moxi35-c66f799a.koyeb.app/")
        except:
            pass
        time.sleep(90)

def keep_alive():
    # Run Flask server (for Koyeb port check)
    threading.Thread(target=run_flask, daemon=True).start()
    # Ping your own URL every 90 seconds (prevents idle timeout)
    threading.Thread(target=ping_self, daemon=True).start()
